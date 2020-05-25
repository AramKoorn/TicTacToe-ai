from scripts.tictactoe_bot import TicTacToeBot

winners, q_table = TicTacToeBot().train_bot(iterations=1000)
