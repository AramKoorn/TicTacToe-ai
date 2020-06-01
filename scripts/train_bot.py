from scripts.tictactoe_bot import TicTacToeBot, Qtable
import pandas as pd
import itertools


def run():

    # Init bots
    bot_X = Qtable(player='X')
    bot_O = Qtable(player='O')

    # Parameters
    alpha = 0.6
    gamma = 0.8
    epsilon = 0.1

    # Train




    pd.to_pickle(bot.q_table, 'q_table.pkl')

    pass


if __name__ == '__main__':
    run()