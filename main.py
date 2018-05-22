"""Module to play draughts with ML"""
from draughts import Draughts
from human_player import HumanPlayer
from random_player import RandomPlayer
from minimax_player import MinimaxPlayer

def main():
    """Program entrypoint"""
    game = Draughts()
    state = game.new_game([MinimaxPlayer(2, MinimaxPlayer.draughts_count_heuristic), RandomPlayer()])
    while game.evaluate(state) == 0:
        if state['turn'] == 0:
            print(game.display(state))
        state = game.play_turn(state)
    print('Game won by player ' + str(1-state['turn']))

if __name__ == '__main__':
    main()
