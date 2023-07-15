# have all shapes
# tetromino is a letter, shape, index tuple
# have a generate random method.

import numpy as np
import random

LETTERS = ['s', 'z', 'i', 't', 'j', 'l', 'o']

class Tetromino:
    def __init__(self, letter):
        if letter not in LETTERS:
            return None
        self.letter = letter
        self.tetromino_arrays = self.get_tetromino_arrays(letter)

    @staticmethod
    def get_tetromino_arrays(letter):
        if letter == 's':
            return [np.array([[1, 1, 0],
                              [0, 1, 1]]),
                    np.array([[0, 1],
                              [1, 1],
                              [1, 0]])]
        elif letter == 'z':
            return [np.array([[0, 2, 2],
                              [2, 2, 0]]),
                    np.array([[2, 0],
                              [2, 2],
                              [0, 2]])]
        elif letter == 'i':
            return [np.array([[3, 3, 3, 3]]),
                    np.array([[3],
                              [3],
                              [3],
                              [3]])]
        elif letter == 't':
            return [np.array([[0, 4, 0],
                              [4, 4, 4]]),
                    np.array([[4, 0],
                              [4, 4],
                              [4, 0]]),
                    np.array([[4, 4, 4],
                              [0, 4, 0]]),
                    np.array([[0, 4],
                              [4, 4],
                              [0, 4]])]
        elif letter == 'j':
            return [np.array([[0, 0, 5],
                              [5, 5, 5]]),
                    np.array([[5, 0],
                              [5, 0],
                              [5, 5]]),
                    np.array([[5, 5, 5],
                              [5, 0, 0]]),
                    np.array([[5, 5],
                              [0, 5],
                              [0, 5]])]
        elif letter == 'l':
            return [np.array([[6, 0, 0],
                              [6, 6, 6]]),
                    np.array([[6, 6],
                              [6, 0],
                              [6, 0]]),
                    np.array([[6, 6, 6],
                              [0, 0, 6]]),
                    np.array([[0, 6],
                              [0, 6],
                              [1, 6]])]
        elif letter == 'o':
            return [np.array([[7, 7],
                              [7, 7]])]
        else:
            return None
        
    @staticmethod
    def generate_random_tetromino():
        return Tetromino(random.choice(LETTERS))