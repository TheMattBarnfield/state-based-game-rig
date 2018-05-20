"""Module to play draughts with ML"""
from draughts import Draughts
from human_player import HumanPlayer
from random_player import RandomPlayer

def main():
    """Program entrypoint"""
    game = Draughts()
    state = game.new_game([HumanPlayer(), RandomPlayer()])
    while game.evaluate(state) == 0:
        print(game.display(state))
        state = game.play_turn(state)
    print('Game won by player ' + str((3-game.evaluate(state))/2))

if __name__ == '__main__':
    main()
