from common.player import Player
from abc import ABC, abstractmethod # https://docs.python.org/3/library/abc.html
# from common.valid_words import valid_words
import string
import random

class Guess:
    """
    A class encapsulating guesses (containing the guess, and the index of the guess).
    """
    def __init__(self, word, guess_count):
        self.__word = word
        self.__guess = guess_count

    def word(self):
        return self.__word
    
    def guess(self):
        return self.__guess

class GameState:
    """
    An object that holds the state of the game. The server and client hold replicas of these,
        and seek, via message passing (Command passing) to update and synchronize each other's 
        states.
    
    A client will only ever have one of these, so its instantiation and usage of this follows 
        the SINGLETON PATTERN, with lazy instantiation, as instantiation is done when the client
        needs it, at a particular point (surrounding the start of a new game).

    Contains methods to update state, either via guess, or via explicit setting of instance 
        variables, as needed by the client and server.
    """
    def __init__(self):
        """
        Construct the state, which consists of the player (which contains aspects of the game state
            as well), as well as the stage in which the game is at, which starts at the lobby stage.
        """
        self.__state = {
            "player_a": None,
            "player_b": None, 
            "stage": "lobby"
        }

    def reset(self):
        """
        As clients make use of the GameState class following the SINGLETON PATTERN, we only create 
            one instance and reset it for each game, so this method resets the GameState instance 
            object for a new game as the players and stage will be different.
        """
        self.__state = {
            "player_a": None,
            "player_b": None,  
            "stage": "lobby"
        }

    def set_player_a(self, player_a: Player):
        """
        A setter for the first player in the game.
        """
        self.__state["player_a"] = player_a

    def get_player_a(self):
        """
        A getter for the first player in the game.
        """
        return self.__state["player_a"]

    def set_player_b(self, player_b: Player):
        """
        A setter for the second player in the game.
        """
        self.__state["player_b"] = player_b
        
    def get_player_b(self):
        """
        A getter for the second player in the game.
        """
        return self.__state["player_b"]
    
    def get_stage(self):
        """
        A getter for the stage of the game.
        """
        return self.__state["stage"]

    def set_stage(self, stage: str):
        """
        A getter for the stage of the game.
        """
        if stage in ['lobby', 'wordpick', 'game', 'end']:
            self.__state["stage"] = stage

    def get_state(self):
        """
        A getter for the overall state.
        """
        return self.__state

    def set_state(self, new_state):
        """
        A setter for the overall state.
        Handles verification of state, ensuring the correct keys are present.
        """
        if list(sorted(new_state.keys())) == ["player_a", "player_b", "stage"]:
            self.__state = new_state
        else:
            unex_keys = [f for f in list(sorted(new_state.keys())) if f not in ["current_player", "player_a", "player_b", "valid"]]
            print(f"Unexpected keys {unex_keys} in state.")


    def update(self, lobby_id: str, player: Player, g: Guess):
        """
        A means to update state not by setters, but instead by checking a guess
            and verifying if it is correct (in the opponent's list of words). If 
            so, the player state is updated, and subsequently the game state. 
        
        A Command that can be sent to the server when this method is invoked by 
            the client is returned. It will be either a Command for the game ending,
            a correct guess, or an incorrect guess.

        By returning and forwarding commands here, we make use of the COMMAND PATTERN,
            with execution of these commands at the relevant host/recipient and general
            command execution being abstracted by a general "execute" method being 
            crucial components of our implementation of the COMMAND PATTERN.
        """
        # get the current word of the player
        current_word = player.get_opponent_list().get_as_iterable()[player.progress]

        print(player.name,"to guess:",player.get_opponent_list().get_as_iterable())
        print(player.name,"i sent:",player.get_my_list().get_as_iterable())

        # set the guess index correctly here
        g.__guess = len(player.guesses[current_word])

        # add guess to list of guesses player has made
        player.guesses[current_word].append(g)

        # compare the guess to this word
        success = False
        if current_word == g.word():
            # success!
            success = True
            player.progress += 1

        print(player.name, "guess list:", player.guesses)
        
        # return a command for the client to forward to the server
        # this return value is only used if the update is to the local, non-opponent player
        if player.progress == 5: # completed
            self.set_stage('end')
            player.winner = True
            return GameEndCommand(lobby_id, player, g)
        else:
            print(success, g.word(), current_word)
            if success:
                return CorrectGuessCommand(lobby_id, player, g)
            else:
                return StateUpdateCommand(lobby_id, player, g)
        
    def __str__(self):
        """
        A toString method for the state. Used in debugging.
        """
        if self.get_player_b() != None:
            return f"Player A: {self.get_player_a().name}, Player B: {self.get_player_b().name}"
        else:
            return f"Player A: {self.get_player_a().name}, Player B: (NONE)"

    def __repr__(self):
        """
        A string representation method for the state. Used in debugging.
        """
        if self.get_player_b() != None:
            return f"Player A: {self.get_player_a().name}, Player B: {self.get_player_b().name}"
        else:
            return f"Player A: {self.get_player_a().name}, Player B: (NONE)"

class Command(ABC):
    """
    An abstract class abstracting general command functionality. The implementors
        follow below. This is our implementation of the COMMAND PATTERN, where these 
        commands are the primary means of messaging between hosts, entities, and
        with execution being abstracted to a generic "execute" method, with actual
        implementations being relevant to the command and host it would likely land
        on. 
    """
    def __init__(self, game_state):
        """
        An initializer for the command. Tracks gamestate which is generally not
            passed with each command, for concise updates. However, it retains the
            option for this to be done.
        """
        if game_state == None or type(game_state) ==  GameState:
            self.game_state = game_state # any collection type
        else:
            print("Incorrect type for game_state...")
            return None

    # only called on server
    @abstractmethod
    def execute(self):
        """
        Abstract execution method for our COMMAND PATTERN implementation.
        """
        ...


class CreateLobbyCommand(Command):
    """
    A command bearing relevant information to create a lobby.
    """
    def __init__(self, player: Player): # have listening address for observer
        """
        The initializer for the creation of a lobby.
        Takes only a player, as when creating a lobby only this player exists and
            a new lobby ID shall be generated (and returned to the user/revealed
            upon execution).
        """
        if type(player) == Player:
            super().__init__(None)
            # https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
            self.lobby_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            self.player = player
        else:
            print("Lobby ID must be a string, states must be a Server.")
            return None

    def execute(self): # store listening address for observer in player
        """
        The execution of creating a new lobby. This is what the server will ultimately
            invoke upon receipt. A new GameState with the original player's information
            is generated and returned.
        """
        # create a new gamestate for the new lobby
        gs = GameState()

        # set the first player
        gs.set_player_a(self.player)

        # return the resultant lobby_id -> gamestate pairing to the caller
        return (self.lobby_id, gs)
 

class JoinLobbyCommand(Command):
    """
    A command bearing the relevant information to join a lobby.
    """
    def __init__(self, player: Player, lobby_id: str):
        """
        The initializer for a command to join a lobby.
        Takes the second player to join, as well as the lobby ID, so that the game state
            can be updated on the executor accurately.
        """
        if type(lobby_id) == str and type(player) == Player:
            super().__init__(None)
            self.lobby_id = lobby_id
            self.player = player
        else:
            print("Lobby ID must be a string, states must be a Server.")
            return None

    def execute(self):
        """
        Execute the command itself, returning relevant information (the lobby id and new 
            player) to the executor (the server).
        """
        # return the resultant lobby_id -> player pairing to the caller to add to gamestate.
        #   server will use this.
        return (self.lobby_id, self.player)


class GameStartedCommand(Command):
    """
    A class bearing the relevant information to notify clients of the server that a
        new game has been started.
    """
    def __init__(self, player_a: Player, player_b: Player): 
        """
        An initializer for this command, taking (from the server) both the players, so that
            Clients can update their local gamestate accordingly.
        """
        super().__init__(None)
        self.player_a = player_a
        self.player_b = player_b

    def execute(self): 
        """
        Execute the command itself, returning relevant information (the two different players) 
            to the executor (the Client).
        """
        return (self.player_a, self.player_b)
    

class GameRunningCommand(Command):
    """
    A class bearing the relevant information to notify clients of the server that a
        game will start running, as the lists of words for opponents to guess have been
        submitted by both players a and b.
    """
    def __init__(self, player_a_list: list, player_b_list: list): 
        """
        An initializer for this command, taking (from the server) both the players' lists, 
            so that Clients can update their local gamestate accordingly.
        """
        super().__init__(None)
        self.a_list = player_a_list
        self.b_list = player_b_list

    def execute(self): 
        """
        Execute the command itself, returning relevant information (the two different players' 
            lists) to the executor (the Client).
        """
        return (self.a_list, self.b_list)


class NewWordListCommand(Command):
    """
    A class bearing the relevant information to provide the server with a player's list 
        of words they wish their opponent to play against. This list would have been verified
        locally, for simplicity of implementation, as opposed to verifying against the server
        repeatedly.
    """
    def __init__(self, lobby_id: str, player: Player, wordlist: list): 
        """
        An initializer for this command, taking (from the Client) the player's list.
        """
        if type(wordlist) == list and len(wordlist) == 5 and type(wordlist[0]) == str \
            and type(lobby_id) == str and type(player) == Player:
            super().__init__(None)
            self.lobby_id = lobby_id
            self.player = player
            self.wordlist = wordlist
        else:
            print("Invalid wordlist - length must be 5, must have strings. LobbyID possibly invalid or player not a Player.")
            return None

    def execute(self):
        """
        Execute the command itself, returning relevant information (the lobby id, the player who
            sent the list, and the list in question) to the executor (the server).
        """
        # server will use this.
        return (self.lobby_id, self.player, self.wordlist)


class CorrectGuessCommand(Command):
    """
    A command bearing the relevant information to notify a GameState maintainer of a correct guess
        having been made by a given player. This involves passing the lobby_id, the player who made 
        this correct guess, and the guess itself, with correctness being verified locally at the 
        Client to reduce message passing and complexity.
    """
    def __init__(self, lobby_id: str, player: Player, g: Guess):
        """
        An initializer for this command, taking (from the Client) the lobby id, player, and guess.
        """
        if type(g) == Guess and type(lobby_id) == str and type(player) == Player:
            super().__init__(None)
            self.lobby_id = lobby_id
            self.player = player
            self.guess = g
        else:
            print("Invalid wordlist - length must be 5, must have strings. LobbyID possibly invalid or player not a Player.")
            return None

    def execute(self):
        """
        Execute the command itself, returning relevant information (the lobby id, the player who
            sent the list, and the guess in question) to the executor (the server).
        """
        # server will use this.
        return (self.lobby_id, self.player, self.guess)


class StateUpdateCommand(Command):
    """
    A command bearing the relevant information to notify a GameState maintainer of an incorrect guess
        having been made by a given player. This involves passing the lobby_id, the player who made 
        this correct guess, and the guess itself, with (in)correctness being verified locally at the 
        Client to reduce message passing and complexity.
    """
    def __init__(self, lobby_id: str, player: Player, g: Guess):
        """
        An initializer for this command, taking (from the Client) the lobby id, player, and guess.
        """
        if type(g) == Guess and type(lobby_id) == str and type(player) == Player:
            super().__init__(None)
            self.lobby_id = lobby_id
            self.player = player
            self.guess = g
        else:
            print("Invalid wordlist - length must be 5, must have strings. LobbyID possibly invalid or player not a Player.")
            return None

    def execute(self):
        """
        Execute the command itself, returning relevant information (the lobby id, the player who
            sent the list, and the guess in question) to the executor (the server).
        """
        # server will use this.
        return (self.lobby_id, self.player, self.guess)


class GameEndCommand(Command):
    """
    A command bearing the relevant information to notify a GameState maintainer of a final, correct 
        guess having been made by a given player. This involves passing the lobby_id, the player who made 
        this correct guess, and the guess itself, with (in)correctness being verified locally at the 
        Client to reduce message passing and complexity.
    
    Reciept of this means that a game has now ended as a player has guessed the final word.
    """
    def __init__(self, lobby_id: str, player: Player, g: Guess):
        """
        An initializer for this command, taking (from the Client) the lobby id, player, and guess.
        """
        if type(g) == Guess and type(lobby_id) == str and type(player) == Player:
            super().__init__(None)
            self.lobby_id = lobby_id
            self.player = player
            self.guess = g
        else:
            print("Invalid wordlist - length must be 5, must have strings. LobbyID possibly invalid or player not a Player.")
            return None

    def execute(self):
        """
        Execute the command itself, returning relevant information (the lobby id, the player who
            sent the list, and the guess in question) to the executor (the server).
        """
        # server will use this.
        return (self.lobby_id, self.player, self.guess)


class DumpCommand(Command):
    """
    A command representing a query to dump gamestates from a server. No information is passed.
    """
    def __init__(self):
        """
        A basic (trivial) initializer.
        """
        super().__init__(None)

    def execute(self):
        """
        A trivial execution (as this command has no information to be returned to recipients).
        """
        return None


# this is used in transmission
class Message:
    """
    An encapsulator for commands, containing also the sender of the message, should it be useful
        for further communication or logging purposes.
    """
    def __init__(self, sender: str, command: Command):
        """
        A basic initializer, storing the sender (string of form "<ip>:<port>") and the Command.
        """
        self.sender = sender
        self.command = command


if __name__ == "__main__":
    import pickle

    p_msg = pickle.dumps(Message("127.0.0.1:8001", CreateLobbyCommand("a123")))
    print(pickle.loads(p_msg).command.lobby_id)
    