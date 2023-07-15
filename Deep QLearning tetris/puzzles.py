import random
import numpy as np
import random

class pz:
    def __init__(self, blocks, board):
        self.blocks = blocks
        self.board = board
    
    def n_blocks(self, n=3):
        x = np.random.choice(self.blocks, n)
        return x

    def single(self):
        pass

    def double(self):
        pass

    def triple(self):
        pass

    def tetris(self):
        b = self.n_blocks(n=2)
        np.append(b,self.blocks[0])    #tetris only achievable with I piece

        n_spins = random.randint(0, 3)
        col = random.randint(0, 9)

        rotated_b1 = np.rot90(b[0], n_spins)
        rotated_b2 = np.rot90(b[1], n_spins)

        ans_board = self.board
        
        for i in range(4):
            for j in range(4):
                ans_board[i][col] = 1
        
        print(ans_board)


    def tspin(self):
        pass

    def gen_puz(self):
        b = self.n_blocks()
        rand = np.random.choice([0, 1, 2, 3, 4], 5)
        col = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 10)

        ans_board = self.board
        ans_board[0] = np.zeros(10)

        j = 0
        for i in range(0, len(col)-1):
            while rand[j] >= 0:
                ans_board[rand[j]][col[i]] = 0
                rand[j] -= 1
            if i % 2 == 0: j += 1
        

        for i in range(len(b)):
            for row in range(len(ans_board) - len(b[0]) + 1):
                for col in range(len(ans_board[0]) - len(b[0]) + 1):
                    for rot in range(4):
                        rotated_b = np.rot90(b[i], rot)
                        # if np.array_equal(ans_board[row:row+len(b[0]), col:col+len(b[0])], rotated_b):
                        #     ans_board[row:row+len(b[0]), col:col+len(b[0])] = 0
                        #     break
                        for i in range(len(rotated_b)):
                            for j in range(len(rotated_b[0])):
                                if ans_board[row + i][col + j] == 0 and rotated_b[i][j] == 1:
                                    ans_board[row + i][col + j] = 1
                                else:
                                    ans_board[row + i][col + j] = 0

                    # if ans_board[row][col] == 0:
                    #     ans_board[row][col] = "#"
                    # else:
                    #     ans_board[row][col] = " "

        print(ans_board)
        #40 squares in board, 4 squares in block, 7 blocks take up 28 squares, 12 squares i.e. 3 blocks left




