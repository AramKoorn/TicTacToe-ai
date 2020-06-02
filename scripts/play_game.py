#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os
from scripts.tictactoe_bot import Qtable
from scripts.tictactoe import TicTacToe

def play():


    inp = input('Which player do want to be X/O?')

    # Select the inplayer you want to be and import bot
    if inp == 'X':
        bot = pd.read_pickle('data/bot_o_7000.pkl')
    if inp == 'O':
        bot = pd.read_pickle('data/bot_x_7000.pkl')

    # To get all the states
    test = Qtable('X')

    # Create enviornment
    env = TicTacToe()
    print(f'Starting player is: {env.player}')

    done = False
    while not done:
        print(f'It is {env.player} his or her turn')
        print(f'{env.board}')

        if env.player == inp:
            move = input('What move do you want to do?')
            game_state = env.insert_board(move)
            print(f'{env.board}')
        else:
            key = list({k for k, v in bot.q_ref_table.items() if (env.board == v).sum().sum() == 9})[0]
            state = bot.q_table[key]
            action = np.nanargmax(state)
            action_coded = {v: k for k, v in env.coordinates().items()}[action]
            game_state = env.insert_board(action_coded)
            print(f'{env.board}')

        if game_state != 'notdone':
            done = True

    pass


def run():

    # Play the game
    play()


if __name__ == '__main__':

    import os

    os.chdir('..')
    run()