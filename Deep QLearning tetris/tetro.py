import numpy as np
import puzzles

# I = {
#     0: np.array([[1, 1, 1, 1]]),

#     1: np.array([[1],
#                  [1],
#                  [1],
#                  [1]]),
    
#     2: np.array([[1, 1, 1, 1]]),

#     3: np.array([[1],
#                  [1],
#                  [1],
#                  [1]])
# }

# O = {
#     0: np.array([[1, 1],
#                  [1, 1]]),

#     1: np.array([[1, 1],
#                  [1, 1]]),

#     2: np.array([[1, 1],
#                  [1, 1]]),

#     3: np.array([[1, 1],
#                  [1, 1]])
# }

# J = {
#     0: np.array([[1, 0, 0],
#                  [1, 1, 1]]),

#     1: np.array([[1, 1],
#                  [1, 0],
#                  [1, 0]]),

#     2: np.array([[1, 1, 1],
#                  [0, 0, 1]]),

#     3: np.array([[0, 1],
#                  [0, 1],
#                  [1, 1]])
# }

# L = {
#     0: np.array([[0, 0, 1],
#                  [1, 1, 1]]),

#     1: np.array([[1, 0],
#                  [1, 0],
#                  [1, 1]]),

#     2: np.array([[1, 1, 1],
#                  [1, 0, 0],]),

#     3: np.array([[1, 1],
#                  [0, 1],
#                  [0, 1]])
# }

# S = {
#     0: np.array([[0, 1, 1],
#                  [1, 1, 0]]),

#     1: np.array([[1, 0],
#                  [1, 1],
#                  [0, 1]]),

#     2: np.array([[0, 1, 1],
#                  [1, 1, 0]]),

#     3: np.array([[1, 0],
#                  [1, 1],
#                  [0, 1]])
# }

# Z = {
#     0: np.array([[1, 1, 0],
#                  [0, 1, 1]]),

#     1: np.array([[0, 1],
#                  [1, 1],
#                  [1, 0]]),

#     2: np.array([[1, 1, 0],
#                  [0, 1, 1]]),

#     3: np.array([[0, 1],
#                  [1, 1],
#                  [1, 0]])
# }

# T = {
#     0: np.array([[0, 1, 0],
#                  [1, 1, 1]]),

#     1: np.array([[1, 0],
#                  [1, 1],
#                  [1, 0]]),

#     2: np.array([[1, 1, 1],
#                  [0, 1, 0]]),

#     3: np.array([[0, 1],
#                  [1, 1],
#                  [0, 1]])
# }

I = np.array([[1, 1, 1, 1]])

O = np.array([[1, 1],
             [1, 1]])

J = np.array([[1, 0, 0],
              [1, 1, 1]])

L = np.array([[0, 0, 1],
              [1, 1, 1]])

S = np.array([[0, 1, 1],
              [1, 1, 0]])

Z = np.array([[1, 1, 0],
              [0, 1, 1]])

T = np.array([[0, 1, 0],
              [1, 1, 1]])

blocks = [I, O, J, L, S, Z, T]

subboard = np.array([["#" for j in range(10)] for i in range(5)])

#print(subboard)
# print(subboard)
# print(subboard)
# print(subboard)

p = puzzles.pz(blocks, subboard)
p.gen_puz()

# test = np.array([[0, 1, 0],
#                  [1, 1, 1]])

# test2 = np.rot90(test, 1)

# print(test)
# print(test2)