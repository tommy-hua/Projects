from agent import *
from game import *

# runs and shows the game after every agent created move
if __name__ == "__main__":
    # create game
    g = Game()

    # load agent or create new one
    a = Agent()
    a.load_model('/tmp/2023-05-06 21:43:15.165342-dqn_weights')

    # keep getting next move :3
    done = False
    g.state.show()
    while not done:
        os.system('clear')

        # get next move
        state, reward, done = a.get_move(g.state)

        # update state
        g.step(reward, done, state)
        g.state.show()

        # repeat
        if not done:
            input("Press key to continue")