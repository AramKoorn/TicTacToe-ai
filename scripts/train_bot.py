from scripts.tictactoe_bot import TicTacToeBot


def run():

    alpha = 0.4
    gamma = 0.8
    epsilon = 0.1

    bot = TicTacToeBot(alpha=alpha, gamma=gamma, epsilon=epsilon)
    bot.train(iterations=1000)

    1
    pass


if __name__ == '__main__':
    run()