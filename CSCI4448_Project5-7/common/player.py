from common.wordlist import OpponentWordList

class Player:
    """
    An object that holds the state of a player. GameState objects hold replicas of these for each player,
        synchronizing with each other via message passing (Command passing) to update and synchronize each other's 
        states.

    A player has a reference to its observer, the words it needs to guess, the words it sent, and
        then means by which any and all of these can be updated and/or accessed.
    """
    def __init__(self, name, observer_host, observer_port):
        """
        An initializer for this class, storing the name, observer information, lists, and victory status.
        """
        # save player name
        self.name = name

        # the index in the opponent list that I am at
        self.progress = 0

        # and finally the means by which the server can communicate,
        #   we include the associated Observer address for this player.
        self.observer_host = observer_host
        self.observer_port = observer_port

        # set None lists
        self.my_sent_list = None
        self.opponent_sent_list = None

        self.winner = False

    def get_observer(self):
        """
        A getter for observer information.
        """
        return (self.observer_host, self.observer_port)
    
    def get_my_list(self):
        """
        A getter for the list of words that this player sent to its opponent.
        """
        # the list of words I sent (useful to have)
        return self.my_sent_list

    def set_my_list(self, my_sent_list):
        """
        A setter for the list of words that this player sent to its opponent.
        """
        # the list of words I sent (useful to have)
        self.my_sent_list = my_sent_list

    def get_opponent_list(self):
        """
        A getter for the list of words that this player must guess, sent by the opponent.
        """
        # the list of words I need to guess
        return self.opponent_sent_list
    
    def set_opponent_list(self, opponent_sent_list: OpponentWordList):
        """
        A setter for the list of words that this player must guess, sent by the opponent.
        """
        # the list of words I need to guess
        self.opponent_sent_list = opponent_sent_list

        # store guesses as a map of (expected -> [guess1, guess2, ...])
        self.guesses = {x: [] for x in opponent_sent_list.get_as_iterable()}

    def get_guesses(self):
        """
        A getter for mappings between words to guess and actual guesses by this player.
        """
        # get dict of guesses (expected -> [guess1, guess2, ...])
        return self.guesses