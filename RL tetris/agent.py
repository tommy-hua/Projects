from datetime import datetime
from game import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import random

class Experience():
    def __init__(self):
        self.experience = []
    
    def push(self, state, next_state, reward):
        if len(self.experience < 10000):
            state_grid, state_one_hot = state.as_np() # input
            next_state_grid, next_state_one_hot = state.as_np() # part of output, with reward
            self.experience.append((state_grid, state_one_hot, next_state_grid, next_state_one_hot, reward))
        else:
            self.experience = self.experience[1:]
            state_grid, state_one_hot = state.as_np() # input
            next_state_grid, next_state_one_hot = state.as_np() # part of output, with reward
            self.experience.append((state_grid, state_one_hot, next_state_grid, next_state_one_hot, reward))

    def sample(self, n=32):
        # heavily mirrors, in structure, sampling from https://markelsanz14.medium.com/introduction-to-reinforcement-learning-part-3-q-learning-with-neural-networks-algorithm-dqn-1e22ee928ecd
        state_grids, state_one_hots, next_state_grids, next_state_one_hots, rewards = [], [], [], [], []
        samples = random.choice(self.experience, n)
        for sample in samples:
            state_grids.append(sample[0])
            state_one_hots.append(sample[1])
            next_state_grids.append(sample[2])
            next_state_one_hots.append(sample[3])
            rewards.append(sample[4])
        
        # convert it all to a numpy array of multiple examples
        return np.array(state_grids), np.array(state_one_hots), np.array(next_state_grids), np.array(next_state_one_hots), np.array(rewards)


class Agent():
    def __init__(self):
        # initialize a game object
        self.game = Game()

        # create the network - only using 1 instead of 2 so that we just train 1, as actively and
        #   frequently updating it as possible, as opposed to using a different network for the 
        #   weights when estimating the value of a state
        self.main_net = self.make_DQN()
        self.optimizer = tf.keras.optimizers.Adam(1e-4)
        self.mse = tf.keras.losses.MeanSquaredError()

        # create the experience buffer, following https://markelsanz14.medium.com/introduction-to-reinforcement-learning-part-3-q-learning-with-neural-networks-algorithm-dqn-1e22ee928ecd
        self.buffer = Experience()
    
    def make_DQN(self):
        # idea for DQN structure borrowed largely from https://medium.com/mlearning-ai/reinforcement-learning-on-tetris-707f75716c37
        game_input = keras.Input(shape=(PADDED_HEIGHT, PADDED_WIDTH, 1))
        grid = layers.Conv2D(32, (3, 3), activation="relu", input_shape=(HEIGHT, WIDTH, 1))(game_input)
        grid = layers.MaxPool2D(pool_size=(2, 2))(grid)
        grid = layers.Conv2D(8, (3, 3), activation="relu")(grid)
        grid = layers.MaxPool2D(pool_size=(2, 2))(grid)
        grid = layers.Flatten()(grid)
        grid = layers.Dense(21, activation="relu")(grid)

        # the idea was to integrate this as a feed-forward layer after convolutions!
        one_hots = keras.Input(shape=(21))

        # put them together
        q = layers.concatenate([grid, one_hots])
        q = layers.Dense(64, activation="relu")(q)
        q = layers.Dense(16, activation="relu")(q)
        q = layers.Dense(1)(q) # no activation - this way we get a predicted value for our q-value! This is instead of outputting an action, as we work on a state-by-state basis.
        # that idea was from the first Medium article writer 

        # following second medium article
        model = keras.Model(inputs=[game_input, one_hots], outputs=q)
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss=tf.keras.losses.MeanSquaredError())

        return model


    def train_traditional(self):
        iters = 0

        # make each episode
        for episode in range(1000):
            
            # reset environment
            self.game.reset()
            
            # until episode finishes or we have taken enough steps
            num_steps = 0
            done = False
            while num_steps < 100 and not done:
                
                # get state, so we can hold it as an input
                current_state = self.game.state
                
                # get next state and rewards and whether they're done
                all_states = self.game.state.get_next_possible_states()
                grid_states = np.array([entry[0][PADDED_HEIGHT-HEIGHT:, 0:WIDTH] for entry in all_states])
                oh_states = np.array([entry[1] for entry in all_states])
                rewards = np.array([entry[2] for entry in all_states])
                dones = [entry[3] for entry in all_states]
                
                # calculate q for each of these states, much like in the first article
                q = rewards + self.main_net((grid_states, oh_states))

                # pick the best option
                b = np.argmax(q)
                next_state, next_reward, next_done = grid_states[b], rewards[b], dones[b]

                # step
                self.game.step(next_reward, next_done, next_state)

                # store as episode data this state, next state, q's -> put it in replay buffer
                self.buffer.push(current_state, next_state, next_reward)
                iters += 1
                
                # every something iterations, if buffer big enuff, train the network/fit it
                if iters%500 == 0:
                    state_grids, state_one_hots, next_state_grids, next_state_one_hots, rewards = self.experience.sample(128)
                    
                    # turn previous states' predictions + q's into goal values, seek to 
                    #   predict it with current state s
                    goal_values = self.main_net(next_state_grids, next_state_one_hots) + rewards

                    # fit data
                    self.main_net.fit((state_grids, state_one_hots), goal_values, batch_size=16, epochs=5)

                    # save progress
                    self.main_net.save(f'./{datetime.now()}-dqn')
                    self.main_net.save_weights(f'./{datetime.now()}-dqn_weights')

    def train_DQN(self, file):
        # get training data from our random data generation, as a file. 
        grids, pieces, rewards = np.load(file)

        # zip grids and pieces
        inp = zip(grids, pieces)
        out = rewards

        # and now train. as our data came preformatted we just need to call a fit on it
        self.main_net.fit(inp, out, batch_size=16, epochs=5)

        # save progress
        self.main_net.save(f'./{datetime.now()}-dqn')
        self.main_net.save_weights(f'./{datetime.now()}-dqn_weights')

    
    def load_model(self, file):
        # borrowed from https://medium.com/mlearning-ai/reinforcement-learning-on-tetris-707f75716c37
        #   realized we could actually be very smart about loading in case we stop training for some 
        #   reason
        if os.path.isfile(file):
            self.model.load_weights(file)


    def get_move(self, state):
        # given a state, make the next move
        all_states = state.get_next_possible_states()

        # unpack
        grid_states = np.array([entry[0] for entry in all_states])
        oh_states = np.array([entry[1] for entry in all_states])
        rewards = np.array([entry[2] for entry in all_states])
        dones = [entry[3] for entry in all_states]

        # get q value
        q = rewards + self.main_net((grid_states, oh_states), training=False)

        # pick the best option
        b = np.argmax(q, axis=0)[0]
        next_state, next_reward, next_done = grid_states[b], rewards[b], dones[b]

        return (next_state, next_reward, next_done) 

Agent()