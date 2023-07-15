import socket
import sys
import threading
import time
sys.path.append("..")
from common.gamestate import *
from common.wordlist import TotalWordList
import sys
import pickle

import socket
import sys
sys.path.append("..")
from common.gamestate import *
import sys
import pickle
import threading
from _thread import *
from typing import cast

class Client:
    """
    
    A class representing the client in our client-server game design/interface.

    This should be thought of as a Driver, as it is here that the UI is spawned and
        updates are forwarded, and it is through this class any updates from (and to)
        the server are handled (or sent). 

    This class has an instance of UI elements, as well as of the Observer, which listens
        to the server, and sends updates to subscribers (such as this class).
        (THIS IS AN IMPLEMENTATION OF THE OBSERVER PATTERN, within a client-server 
            context, as we have forwarding of external state updates to an in-house
            listener, with variability in our implementation should we seek logging!)
    
    This class also makes use of the SINGLETON PATTERN, as each client instance, per game,
        needs only 1 instance of the GameState object. It makes use of lazy instantiation,
        with instantiation being done within the game running context and only being done
        when needed (following the logic of creating a GameState object when the game
        is actually running). As one client has only one game, we only have one instantiated
        at a time, and the coupling between a Client and its GameState is high, so a
        SINGLETON PATTERN is useful here.

    authors: Pranav Subramanian and Tommy Hua
    
    """


    def __init__(self, observer_host: str, observer_port: int, server_host: str, server_port: int, my_name: str):
        """
        The client constructor. Creates the observer, the player instance representing this
            player in the GameState, and starts running the UI/user interface.
        """
        # save host and port
        self.observer_host = observer_host
        self.observer_port = observer_port
        self.server_host = server_host
        self.server_port = server_port

        # save name
        self.my_name = my_name

        # create an own observer here. as an observer only listens or forwards
        #   updates, we can just have one the entire time.
        self.observer = Observer(self, self.observer_host, self.observer_port, self.server_host, self.server_port, self.my_name)

        # create a singleton gamestate object here, which we will recycle with each
        #   game. Each game we will sync this with server by passing messages
        self.gamestate = GameState()

        # create a local wordlist. no longer verifying against server to reduce messages
        self.valid_words = TotalWordList("../common/mit_10000.txt")

        # spin this off in a new method.
        self.run_game()


    def run_game(self):
        """
        The method that actually runs the game. This would interface with the user interface.
            Create or join a lobby here, take guesses, and go through all stages of gameplay in
            this method.
        """
        in_lobby = False
        while True:
            if not in_lobby:
                c_or_j = input('CREATE or JOIN? \n')
                if c_or_j[0] == 'C':
                    # reset singleton gamestate object here
                    self.gamestate.reset()

                    # create player here
                    self.player = Player(self.my_name, self.observer_host, self.observer_port)
                    
                    # create the lobby from our end (send request)
                    self.create_lobby()

                    # update local state so we can switch screens/contexts
                    in_lobby = True

                elif c_or_j[0] == 'J':
                    # reset singleton gamestate object here
                    self.gamestate.reset()

                    # create player here
                    self.player = Player(self.my_name, self.observer_host, self.observer_port)

                    # join the lobby from our end (send request)
                    lobby_id = input('Provide a lobby id.\n')
                    self.join_lobby(lobby_id)

                    # update local state so we can switch screens/contexts
                    in_lobby = True

                elif c_or_j[0] == 'D':
                    self.dump()
            else:
                # get the stage so that we know what 'mode' to operate in
                stage = self.gamestate.get_stage()

                if stage == 'lobby':
                    print('Still waiting for others to join...')
                    time.sleep(2)

                # check now if game has started...
                elif stage == 'wordpick':
                    # if so, we want to create list, check validity locally
                    wordlist = []
                    while len(wordlist) < 5:
                        next_word = input("Enter a 5-letter word to challenge your opponent.\n")
                        if self.valid_words.check_membership(next_word) and next_word not in wordlist:
                            print("Great choice.")
                            wordlist.append(next_word)
                            print(len(wordlist))
                        else:
                            print("That's not a real word.")
                    # if self.player.name == 'a':
                    #     wordlist = ['youth', 'yacht', 'yahoo', 'wives', 'waste']
                    # else:
                    #     wordlist = ['watch', 'water', 'wants', 'walls', 'filme']
                    # print(wordlist)

                    # forward to server
                    self.send_word_list(wordlist)

                    # wait until gametime
                    while self.gamestate.get_stage() != 'game':
                        print('Waiting for other to submit list...')
                        time.sleep(2)

                # then server sends message saying lists have been created, time to start playing
                elif stage == 'game':
                    # now loop to get guesses
                    while self.gamestate.get_stage() != 'end':
                        # get user input
                        word = ""
                        while len(word) != 5:
                            word = input("Enter a 5-letter word as a guess.\n")

                        # check gamestate again before wasting time sending update
                        if self.gamestate.get_stage() == 'end':
                            print('It appears your opponent has won, prior to last guess. Ignoring...')
                            break

                        # wrap as a Guess
                        guess = Guess(word, -1)

                        # get which player i am
                        a = self.gamestate.get_player_a()
                        b = self.gamestate.get_player_b()

                        if self.player.name == a.name:
                            self.player = a
                        elif self.player.name == b.name:
                            self.player = b

                        # check against local gamestate
                        result = self.gamestate.update(self.lobby_id, self.player, guess)

                        # # print our and their guesses as far as we know
                        # a = self.gamestate.get_player_a()
                        # b = self.gamestate.get_player_b()
                        # print(a.name, a.get_guesses())
                        # print(b.name, b.get_guesses())

                        # forward according update
                        self.send_game_update(result)

                # the gamestate has been updated to end
                elif stage == 'end':
                    # dump stats about game...
                    # player A
                    a = self.gamestate.get_player_a()
                    print(f"PLAYER A: {a.name}")
                    if a.winner == True:
                        print("-> WINNER.")
                    print("GUESSES PER WORD:")
                    guesses_a = a.get_guesses()
                    for word in guesses_a.keys():
                        print(f"Word: {word}")
                        for guess in guesses_a[word]:
                            print(f"-> {guess.word()}")


                    # player B
                    b = self.gamestate.get_player_b()
                    print(f"PLAYER B: {b.name}")
                    if b.winner == True:
                        print("-> WINNER.")
                    print("GUESSES PER WORD:")
                    guesses_b = b.get_guesses()
                    for word in guesses_b.keys():
                        print(f"Word: {word}")
                        if len(guesses_b) == 0:
                            print ("-> <unreached>")
                        else:
                            for guess in guesses_b[word]:
                                print(f"-> {guess.word()}")
                    
                    return

                # invalid state
                else: 
                    print('Invalid state reached. Exiting...')
                    return


    def create_lobby(self):
        """
        A simple method that forwards a request to create the lobby to the server, using the instance
            variables associated with this Client object. This is done for code readability.

        By forwarding commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command 
            execution being abstracted by a general "execute" method being crucial 
            components of our implementation of the COMMAND PATTERN.
        """
        # create message
        msg = CreateLobbyCommand(self.player)

        # send it using simple interface
        resp = self.observer.forward_update(msg)

        # print lobby to user
        print(f'{resp}')
        self.lobby_id = resp


    def join_lobby(self, lobby_id):
        """
        A simple method that forwards a request to join a lobby to the server, using the instance
            variables (and the user-provided lobby_id) associated with this Client object. 
            This is done for code readability.

        By forwarding commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command 
            execution being abstracted by a general "execute" method being crucial 
            components of our implementation of the COMMAND PATTERN.
        """
        # create message
        msg = JoinLobbyCommand(self.player, lobby_id)

        # send it using simple interface
        resp = self.observer.forward_update(msg)

        # handle result
        if resp == "INVALIDLOBBY":
            print('Invalid lobby ID provided. Try again...')
            exit(1)
        else:
            # print(resp)
            self.lobby_id = lobby_id
    

    def send_word_list(self, wordlist):
        """
        A simple method that forwards a request to submit a word list game state to the 
            server. Separating it out is done for code readability.

        By forwarding commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command 
            execution being abstracted by a general "execute" method being crucial 
            components of our implementation of the COMMAND PATTERN.
        """
        # create message
        msg = NewWordListCommand(self.lobby_id, self.player, wordlist)

        # send it using simple interface
        resp = self.observer.forward_update(msg)

        # # handle result
        # if resp == "LISTVALIDATED":
        #     print('List submitted')
        # else:
        #     print(resp)


    def send_game_update(self, msg: Command):
        """
        A simple method that forwards a request to update game state to the server. 
            Separating it out is done for code readability.

        By forwarding commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command 
            execution being abstracted by a general "execute" method being crucial 
            components of our implementation of the COMMAND PATTERN.
        """
        # send it using simple interface
        resp = self.observer.forward_update(msg)

        # handle result
        # if resp == "UPDATESENT":
        #     print('Update sent')
        # else:
        #     print(resp)


    def dump(self):
        """
        A simple method that forwards a request to dump game listings from the server. 
            Separating it out is done for code readability.

        By forwarding commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command 
            execution being abstracted by a general "execute" method being crucial 
            components of our implementation of the COMMAND PATTERN.
        """
        # create message
        msg = DumpCommand()

        # send it using simple interface
        resp = self.observer.forward_update(msg)

        # handle result
        print(resp)

# included here to prevent circular imports
class Observer:
    """
    
    A class representing the observer in our client-server game design/interface.

    This is the implementation of the OBSERVER pattern, as it is here that we get updates
        from the server but most importantly forward those as stateful updates to the 
        client (or any such subscribers). In this sense, this is the PUBLISHER class,
        and it propagates updates to a valid type/form of listener via dedicated 
        update methods (as each type of update requires unique functionality). 
        
    NOTE: The listener/subscriber is integrated with the Client for simplicity of 
        implementation and readability.

    authors: Pranav Subramanian and Tommy Hua
    
    """

    def __init__(self, client: Client, observer_host: str, observer_port: int, server_host: str, server_port: int, my_name: str): # observer_port number in the 9000s
        """
        The observer constructor. Creates a listener thread such that any updates from 
            the server can be caught and propagated to listeners. Also maintains functionality
            to propagate updates to the server (this isn't necessarily a part of the OBSERVER
            PATTERN, it was just useful to delegate server communication elsewhere).
        """
        # save client
        self.client = client
        
        # save hosts and ports
        self.observer_host = observer_host
        self.observer_port = observer_port
        self.server_host = server_host
        self.server_port = server_port

        # save name
        self.my_name = my_name

        # spawn thread to listen for updates
        start_new_thread(self.update_handler_thread, ())

    def update_handler_thread(self):
        """
        Handles updates received from the server, by creating a listener and spinning off a
            new thread to actually respond (see receive update).
        """
        # create a socket, bind to localhost:port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", self.observer_port))
    
        # listen for incoming connections
        s.listen()

        # print(f"Observer for client {self.my_name} is now accepting connections.")
    
        # keep accepting connections! This is structured much like a POSIX API C TCP server would be
        while True:
            # https://bugs.python.org/issue41437 -> cannot CTRL+C here
            conn, addr = s.accept()
            
            # log the connection
            # print('Connection from: ', addr[0], ':', addr[1])
    
            # and now spawn a thread to handle it
            start_new_thread(self.receive_update, (conn,))


    def receive_update(self, conn): # get something from server
        """
        Handles the logic of getting an update, and then pushing relevant information to 
            SUBSCRIBERS. This is the work of the PUBLISHER in our OBSERVER PATTERN.

        By handling commands here, we make use of the COMMAND PATTERN, with execution 
            of these commands at the relevant host/recipient and general command execution 
            being abstracted by a general "execute" method being crucial components of 
            our implementation of the COMMAND PATTERN.
        """
        # get header, encoded in 16 bytes
        header = conn.recv(16) 
        length = int.from_bytes(header, byteorder="big")

        # receive message in 1024 byte chunks
        data = b''
        for _ in range(0, int(length/1024) + 1):
            data += conn.recv(1024)

        # deserialize the message
        msg = pickle.loads(data)

        if type(msg.command) == GameStartedCommand:
            # print('GAME STARTED RECEIVED')
            # unwrap
            cmd = cast(GameStartedCommand, msg.command)
            player_a, player_b = cmd.execute()

            # update gamestate to have both players
            self.client.gamestate.set_player_a(player_a)
            self.client.gamestate.set_player_b(player_b)

            # simply update the stage of the game for this client
            self.client.gamestate.set_stage('wordpick')

        elif type(msg.command) == GameRunningCommand:
            # print('GAME RUNNING RECEIVED')
            # update the players with their lists
            cmd = cast(GameRunningCommand, msg.command)
            a_opponent_list, b_opponent_list = cmd.execute()

            # set them accordingly
            self.client.gamestate.get_player_a().set_opponent_list(a_opponent_list)
            self.client.gamestate.get_player_a().set_my_list(b_opponent_list)
            
            self.client.gamestate.get_player_b().set_opponent_list(b_opponent_list)
            self.client.gamestate.get_player_b().set_my_list(a_opponent_list)

            # update player on client
            if self.client.player.name == self.client.gamestate.get_player_a().name:
                self.client.player.set_opponent_list(a_opponent_list)
                self.client.player.set_my_list(b_opponent_list)
            elif self.client.player.name == self.client.gamestate.get_player_b().name:
                self.client.player.set_opponent_list(b_opponent_list)
                self.client.player.set_my_list(a_opponent_list)
            else:
                print("Invalid player configuration - you are neither a nor b")
                print(self.client.player.name)
                print(player_a.name)
                print(player_b.name)

            # update the stage of the game for this client
            self.client.gamestate.set_stage('game')

        elif type(msg.command) == CorrectGuessCommand: # other player got something right
            # unwrap
            cmd = cast(CorrectGuessCommand, msg.command)
            (_, player, _) = cmd.execute()

            # figure out which player sent the update
            a = self.client.gamestate.get_player_a()
            b = self.client.gamestate.get_player_b()

            if player.name == a.name:
                # update that player
                self.client.gamestate.set_player_a(player)
            elif player.name == b.name:
                # update that player
                self.client.gamestate.set_player_b(player)


        elif type(msg.command) == StateUpdateCommand: # other player got something wrong            
            # unwrap
            cmd = cast(StateUpdateCommand, msg.command)
            (_, player, _) = cmd.execute()

            # figure out which player sent the update
            a = self.client.gamestate.get_player_a()
            b = self.client.gamestate.get_player_b()

            if player.name == a.name:
                # update that player
                self.client.gamestate.set_player_a(player)
            elif player.name == b.name:
                # update that player
                self.client.gamestate.set_player_b(player)

        elif type(msg.command) == GameEndCommand:

            # unwrap
            cmd = cast(GameEndCommand, msg.command)
            (_, player, _) = cmd.execute()

            # figure out which player sent the update
            a = self.client.gamestate.get_player_a()
            b = self.client.gamestate.get_player_b()

            if player.name == a.name:
                # update that player
                self.client.gamestate.set_player_a(player)
            elif player.name == b.name:
                # update that player
                self.client.gamestate.set_player_b(player)

            # update state
            self.client.gamestate.set_stage('end')

        else:
            print("Default")
            conn.close()

        # elif type(msg.command) == CorrectGuessCommand:
        #     cmd = cast(CorrectGuessCommand, msg.command)

        # elif type(msg.command) == StateUpdateCommand:
        #     cmd = cast(StateUpdateCommand, msg.command)

        # else: #GameEndCommand
        #     cmd = cast(GameEndCommand, msg.command)

    def forward_update(self, update: Command): # send something to server. invoked by client
        """
        A method that forwards a Command as a message to the game server. This is delegated to
            the observer for readability and to reduce any code repetition involving communication
            and maintenance of a connection with a server.

        By returning and forwarding commands here, we make use of the COMMAND PATTERN,
            with execution of these commands at the relevant host/recipient and general
            command execution being abstracted by a general "execute" method being 
            crucial components of our implementation of the COMMAND PATTERN.
        """
        # create a socket and connect it
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.server_host,int(self.server_port)))

        # create cmd
        cmd = Message(f"{self.server_host}:{self.server_port}", update)

        # create message
        msg = pickle.dumps(cmd)

        # create header
        header = len(msg).to_bytes(16, byteorder='big')

        # send header
        s.send(header)

        # send data in 1024 byte chunks
        for i in range(0, int(len(msg)/1024) + 1):
            s.send(msg[i:i+1024])

        # # get the response
        # resp = s.recv(1024).decode('utf-8')
        
        # get header, encoded in 16 bytes
        header = s.recv(16) 
        length = int.from_bytes(header, byteorder="big")

        # receive message in 1024 byte chunks
        data = b''
        for _ in range(0, int(length/1024) + 1):
            data += s.recv(1024)

        # get the response
        resp = data.decode('utf-8')

        return resp


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Expected 5 arguments: observer_host, observer_port, server_host, server_port, and my_name")
    else:
        observer_host = sys.argv[1]
        observer_port = int(sys.argv[2])
        server_host = sys.argv[3]
        server_port = int(sys.argv[4])
        my_name = sys.argv[5]
        Client(observer_host, observer_port, server_host, server_port, my_name)