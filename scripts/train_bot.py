from scripts.tictactoe_bot import TicTacToeBot
import pandas as pd


def run():

    alpha = 0.6
    gamma = 0.8
    epsilon = 0.1

    bot = TicTacToeBot(alpha=alpha, gamma=gamma, epsilon=epsilon)
    bot.train(iterations=1000)

    pd.to_pickle(bot.q_table, 'q_table.pkl')

    pass


if __name__ == '__main__':
    run()