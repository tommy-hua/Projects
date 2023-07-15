import time
import numpy as np
from tetromino import *
import os
import itertools

WIDTH = 10
PADDED_WIDTH = WIDTH+3 # 3 on right to pad for largest sideways object (sideways i starting furthest right)
HEIGHT = 20
PADDED_HEIGHT = HEIGHT+4 # 4 on top to pad in case the lowest we can go in a given column is the very top

# https://www.geeksforgeeks.org/print-colors-python-terminal/
def prRed(skk): print("\033[91m{}\033[00m" .format(skk), end=' ')
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk), end=' ')

# def print_arr(arr):
#     for row in arr:
#         for col in row:
#             if col == 0:
#                 print('*', end=' ')
#             else:
#                 prRed(1)
#         print()

class State():
    def __init__(self, grid: np.ndarray, current: Tetromino, next_: list):
        # maintains state
        self.grid = grid
        self.current = current
        self.next_ = next_

    def get_next_possible_states(self):
        # set all current pieces to *'s
        self.grid[self.grid != 0] = 9

        # get the highest members of each column
        centers = [(self.get_highest_in_col(c), c) for c in range(0, WIDTH)]

        # get all orientations of the current tetromino
        tetrominoes = self.current.tetromino_arrays

        # test each center and orientation, generating a list of valid states
        valid_states = []
        for cen, tet in itertools.product(*[centers, tetrominoes]):
            # figure out how to place (make sure nothing exceeds 9, as 9 is taken, 
            #   0 is empty, 1-8 is letter), starting with lower right corner of 
            #   tet overlapping with center
            h, w = tet.shape
            r, c = cen
            found = False
            
            # if it doesn't fit raise the center by up to total height
            # print(r, cen, PADDED_HEIGHT)
            for i in reversed(range(3, r+1)):
                # extract tet.shape segment of self.grid from here
                grid_segment = self.grid[i-h+1:i+1,c:c+w]

                # add tet
                added = grid_segment + tet

                # print(tet, grid_segment, added)

                # check values
                if len(added[added > 9]) <= 0:
                    r = i
                    found = True
                    break
            
            # totally failed
            if not found:
                continue

            # check if in bounds - the whole of tet should be contained in working grid + 1 for height
            # don't check height actually, leave that to the reward system to determine game over.
            # print(tet, cen, c+w-1, WIDTH)
            if (c+w-1) < WIDTH: #(r-h+1) >= (PADDED_HEIGHT-HEIGHT-1) and (c+w-1) <= WIDTH:
                new_grid = self.grid.copy()
                new_grid[i-h+1:i+1,c:c+w] += tet
                valid_states.append(new_grid)

        # go through states and get associated score
        res = []
        for state_grid in valid_states:
            reward, done = State.get_reward(state_grid)
            state_oh = self.as_np()[1]
            res.append((state_grid, state_oh, reward, done))

        # return the next states, their rewards, and their dones
        return res

    def get_highest_in_col(self, c):
        # work way down from top until a '*' encountered
        for r in range(0, PADDED_HEIGHT):
            if self.grid[r][c] != 0:
                return r
        return r

    def as_np(self):
        # return the next as one-hots
        current_one_hot = np.zeros(7)
        current_one_hot[np.where(np.array(LETTERS) == self.current.letter)] = 1

        next1_one_hot = np.zeros(7)
        next1_one_hot[np.where(np.array(LETTERS) == self.next_[0].letter)] = 1

        next2_one_hot = np.zeros(7)
        next2_one_hot[np.where(np.array(LETTERS) == self.next_[1].letter)] = 1

        onehots = np.concatenate((current_one_hot, next1_one_hot, next2_one_hot))

        # return the array without the padding, and as ints
        padless = self.grid[PADDED_HEIGHT-HEIGHT:, 0:WIDTH]
        padless[padless != 0] = 1
        padless[padless == 0] = 0 

        return padless, onehots

    def show(self):
        # clear terminal
        # os.system('clear')

        # NOTE: most recent piece should have letters, others should be *'s
        # show only the 5x10, and next pieces
        to_print = self.grid[PADDED_HEIGHT-HEIGHT:, 0:WIDTH]

        for row in to_print:
            for col in row:
                if col == 0:
                    print('-', end=' ')
                elif col == 9:
                    prCyan('*')
                else:
                    # make letters red
                    prRed(LETTERS[int(col-1)])
            print()

    @staticmethod
    def check_tspin(state: np.ndarray):
        # find the t's
        ts = state[state == 4]

        # if no t's
        if len(ts) == 0: 
            return False
        # else
        else:
            # find center of t's
            x, y = np.where(state == 4)
            coords = list(sorted([coord for coord in zip(x,y)], key=lambda x: (x[0], x[1])))
            if len(coords) != 4:
                print("Invalid T's encountered")
                return False
            x_cen, y_cen = coords[2]

            # check corners
            try:
                if state[x_cen+1, y_cen-1] != 0 and state[x_cen-1, y_cen+1] != 0 and state[x_cen+1, y_cen+1] != 0:
                    return True
                elif state[x_cen-2, y_cen] != 0 and state[x_cen-2, y_cen+2] != 0 and state[x_cen, y_cen+2] != 0:
                    return True
                elif state[x_cen+1, y_cen+1] != 0 and state[x_cen-1, y_cen+1] != 0 and state[x_cen+1, y_cen+3]:
                    return True
            except:
                return False

            return False

    @staticmethod
    def check_cleared_lines(state: np.ndarray):
        lines_cleared = 0
        for row in range(4, PADDED_HEIGHT):
            r = state[row]
            if len(r[r != 0]) == WIDTH:
                lines_cleared+=1
        return lines_cleared

    @staticmethod
    def check_above_grid(state: np.ndarray):
        for row in range(0, 3):
            r = state[row]
            if len(r[r != 0]) > 0:
                return True
        return False

    @staticmethod
    def check_clear_board(state: np.ndarray):
        for row in range(4, PADDED_HEIGHT):
            r = state[row]
            if len(r[r != 0]) != WIDTH or len(r[r == 0]) != PADDED_WIDTH:
                return False
        return True

    @staticmethod
    def get_reward(state: np.ndarray):
        # check if t-spin
        t_spin = State.check_tspin(state)
        # check if above grid/in danger zone
        danger = State.check_above_grid(state)
        # check if any lines cleared
        lines_cleared = State.check_cleared_lines(state)
        # check if board cleared
        board_cleared = State.check_clear_board(state)

        # handle weighting based on lines sent
        lines_sent = -1
        if t_spin:
            lines_sent = 4
        elif lines_cleared == 1:
            lines_sent = 0
        elif lines_cleared == 2:
            lines_sent = 1
        elif lines_cleared == 3:
            lines_sent = 2
        elif lines_cleared == 4:
            lines_sent = 4
            
        # return reward
        if board_cleared:
            return 6, False
        elif danger:
            return -5, True
        elif lines_sent >= 0 and lines_cleared > 0:
            return lines_sent/lines_cleared, False
        else:
            return 0, False

class Game():
    def __init__(self):
        # create state (grid, current piece, next 2 pieces)
        current = Tetromino.generate_random_tetromino()
        next_ = [Tetromino.generate_random_tetromino(), Tetromino.generate_random_tetromino()]
        grid = np.zeros((PADDED_HEIGHT, PADDED_WIDTH))
        self.state = State(grid, current, next_)

        # keep a next up to feed to the new state object whenever a move made
        self.next_up = Tetromino.generate_random_tetromino()

    def reset(self):
        # create state (grid, current piece, next 2 pieces)
        current = Tetromino.generate_random_tetromino()
        next_ = [Tetromino.generate_random_tetromino(), Tetromino.generate_random_tetromino()]
        grid = np.zeros((PADDED_HEIGHT, PADDED_WIDTH))
        self.state = State(grid, current, next_)

        # keep a next up to feed to the new state object whenever a move made
        self.next_up = Tetromino.generate_random_tetromino()


    def step(self, reward, done, next_state): # typical tuple is (state, action, reward, next_state). 
                                        #   We don't care about action and store state, so just keep
                                        #   last 2. 
        # replaces the state with a more updated copy, generates the 
        #   next piece too. 
        # if the state, however, came with a reward of <0, then we are done.
        # otherwise, clear lines as needed and then replace
        if done:
            return None
        else:
            # clear lines
            next_state = np.delete(next_state, np.where(len(next_state[next_state != 0]) == WIDTH), axis=0)
            while len(next_state) < PADDED_HEIGHT:
                next_state = np.vstack((np.zeros(PADDED_WIDTH), next_state))
            
            # update tetromino lists
            current = self.state.next_[0]
            next_ = [self.state.next_[1], self.next_up]
            self.next_up = Tetromino.generate_random_tetromino()

            # set new state and return it
            self.state = State(next_state, current, next_)

    def user_play(self):
        done = False
        self.state.show()
        while not done:
            os.system('clear')

            # get all options
            all_states = self.state.get_next_possible_states()
            
            # pick random
            if len(all_states) == 0:
                break
            state_grids, _, reward, done = random.choice(all_states)

            # update state
            self.step(reward, done, state_grids)
            self.state.show()

            # repeat
            if not done:
                input("Press key to continue")


if __name__ == "__main__":
    os.system('clear')
    # a = np.zeros((5, 5))
    # pc = np.array([[1, 1, 0],
    #                [0, 1, 1]])
    # centers = [(4,0), (4,1), (4,2)]

    # g = np.array([
    #     [0, '*', '*', 'T'],
    #     ['T', '*', '*', 0]
    # ])

    # print(g, type(g[0][0]))

    # g[g != '0'] = 1
    # g[g == '0'] = 0
    # print(g.astype(np.uint8))

    # # print_arr(a)
    # # for y,x in centers:
    # #     time.sleep(1)
    # #     os.system('clear')
    # #     a[y-pc.shape[0]:y, x:x+pc.shape[1]] = pc
    # #     # print(f'\r{a}', end='')
    # #     print_arr(a)
    # #     a = np.zeros((5,5))

    g = Game()
    g.user_play()
