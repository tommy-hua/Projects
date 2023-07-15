# https://docs.python.org/3/library/abc.html
from abc import ABC, abstractmethod
import os
import sys

sys.path.append(".")
from common.trie import Trie

class WordList(ABC):
    """
    An abstract implementation of a word list. This generally means any type of collection 
        (trie, list, set, etc.) of words that can be used in game. The primary functionality 
        involved here surrounds checking membership of a word. Since lists can vary in size 
        and complexity, different implementations of the collection of words, and thus different
        algorithms, or STRATEGIES, might be useful.
        
    Because of the multiplicity of membership strategies, this is our implementation of the 
        STRATEGY PATTERN, used to check membership of a query/word in a given collection of words.
    """
    def __init__(self, collection: any):
        self.collection = collection # any collection type

    @abstractmethod
    def check_membership(self):
        """
        The abstract membership checking method.
        """
        ...

class TotalWordList(WordList):
    """
    A given implementation of the WordList abstract class, geared towards checking validity of
        words prior to a client's submission of a wordlist. Each client has and needs only one 
        of these, aligning with a SINGLETON PATTERN, but the important thing to note here is an 
        implementation of the STRATEGY PATTERN, with this WordList's strategy being geared to 
        quickly search large lists, making use of a trie.

    This way, we can quickly check if a word is valid, even with a massive list.
    """
    def __init__(self, words_path):
        """
        An initializer for this list, taking as an argument a path to a file of words, and then
            constructing from entries in that file a trie consisting of the 5-letter entries for 
            quick lookups and membership verification. 
        """
        if os.path.isfile(words_path):
            # make trie
            t = Trie()
            
            # open file
            with open(words_path, 'r') as f:
                for line in f:
                    line = line.rstrip().lstrip()
                    # write each line to the trie if len = 5
                    if len(line) == 5:
                        t.insert(line)

            # then say super().__init__(t)
            super().__init__(t)

        else:
            print("Invalid filename passed.")
            return None

    def check_membership(self, word):
        """
        Membership checking implementation, which checks first guess word size, followed by checking
            membership in the trie following a trie-oriented algorithm.

        This is the meat of the STRATEGY PATTERN, as it makes use of our generic collection allowed by
            the abstract WordList class to perform a generic form of lookup, which here is implemented
            as a specific, trie-oriented algorithm.
        """
        if len(word) != 5:
            return False
        return len(self.collection.query(word)) >= 1
        

class OpponentWordList(WordList):
    """
    A given implementation of the WordList abstract class, geared towards checking whether a word 
        guessed by a client belongs in a list. Each player has one and performs lookups, geared 
        towards this class' implementation of the WordList (centered on an actual list).

    As a result, we have here an implementation of the STRATEGY PATTERN, with this WordList's 
        strategy being geared to search a small, bounded list.
    """
    def __init__(self, words):
        """
        An initializer for this list, taking as an argument a list of of words.
        This initializer verifies all words are 5 letters long and that there are 5 supplied. 
        """
        # ensure we are passed a list with 5, 5-letter words
        if type(words) == list and len(words) == 5 and set([len(x) for x in words]) == {5}: # a rudimentary list or set suffices
            super().__init__(words)
        else:
            print("Opponent list of words must be of type list with 5 members")
            return None 

    def check_membership(self, word):
        """
        Membership checking implementation, following a list-oriented algorithm (linear search).

        This is the meat of the STRATEGY PATTERN, as it makes use of our generic collection allowed by
            the abstract WordList class to perform a generic form of lookup, which here is implemented
            as a specific, list-oriented algorithm.
        """
        return word in self.collection 
    
    def get_as_iterable(self):
        """
        Iteration of this list can be useful, so an iterable type (the list itself) is made 
            returnable to needing users.
        """
        return self.collection

if __name__ == "__main__":
    t = TotalWordList("common/mit_10000.txt")
    print(t.check_membership('youth'))
    print(t.check_membership('yacht'))
    print(t.check_membership('yahoo'))
    print(t.check_membership('wives'))
    print(t.check_membership('waste'))
    print(t.check_membership('wasted'))
    b = OpponentWordList(['watch', 'water', 'wants', 'walls', 'filme'])
    print(b.check_membership('beary'))