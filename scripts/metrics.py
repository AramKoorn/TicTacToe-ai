import numpy as np
import pandas as pd
from scripts.tictactoe import TicTacToe
from scripts.tictactoe_bot import Qtable


def play_against_random(iterations, bot_player='O', verbose=False):

    if bot_player == 'O':
        bot = pd.read_pickle('data/bot_o_7000.pkl')
    elif bot_player == 'X':
        bot = pd.read_pickle('data/bot_x_7000.pkl')
    else:
        raise ValueError('bot should be either X/O!')

    ai_won = 0
    losses = 0
    draws = 0
    random_moves = 0

    for i in range(iterations):

        env = TicTacToe()

        done = False
        while not done:

            # Random play
            if env.player != bot_player:
                action = env.sample()
                move = {v: k for k, v in env.coordinates().items()}[action]
                game_state = env.insert_board(move)

            # AI PLay
            else:
                key = list({k for k, v in bot.q_ref_table.items() if (env.board == v).sum().sum() == 9})[0]
                try:
                    state = bot.q_table[key]
                    action = np.nanargmax(state)
                    action_coded = {v: k for k, v in env.coordinates().items()}[action]
                    game_state = env.insert_board(action_coded)

                # In case the AI never was in this state before
                except:
                    action = env.sample()
                    move = {v: k for k, v in env.coordinates().items()}[action]
                    game_state = env.insert_board(move)
                    random_moves += 1

            if (game_state == 'win') & (env.player == bot_player):
                ai_won += 1
            if (game_state == 'win') & (env.player != bot_player):
                losses += 1
            if game_state == 'draw':
                draws += 1

            if game_state != 'notdone':
                done = True

                if verbose:
                    print(f'---\n{env.board}\n---')

    return ai_won, draws, losses, random_moves


def save_results(wins, draws, losses, bot_player, iterations):

    if not os.path.exists('results/'):
        os.mkdir('results/')

    # Save results
    print(f'Results for plater {bot_player}')
    print(f'AI won {wins / iterations * 100}% of {iterations} games')
    print(f'AI lost {losses / iterations * 100}% of {iterations} games')
    print(f'AI draws {draws / iterations * 100}% of {iterations} games')

    # Put in dictionary
    res_dict = {'wins': wins, 'draws': draws, 'losses': losses}

    # Save in dictionary
    pd.to_pickle(res_dict, f'results/{bot_player}_iterations_{iterations}.pkl')

    pass


def run():

    iterations = 100

    # PLayer: X
    bot_player = 'X'
    ai_won, draws, losses, random_moves = play_against_random(iterations=iterations, bot_player=bot_player, verbose=True)
    save_results(ai_won, draws, losses, bot_player, iterations)

    # PLayer O
    bot_player = 'O'
    ai_won, draws, losses, random_moves = play_against_random(iterations=iterations, bot_player=bot_player, verbose=True)
    save_results(ai_won, draws, losses, bot_player, iterations)

    pass


if __name__ == '__main__':

    import os
    os.chdir('..')

    run()