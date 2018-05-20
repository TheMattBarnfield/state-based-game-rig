"""Module to play draughts with ML"""
from draughts import Draughts
from human_player import HumanPlayer

def main():
    """Program entrypoint"""
    game = Draughts()
    state = game.new_game([HumanPlayer(), HumanPlayer()])
    while game.evaluate(state) == 0:
        print(game.display(state))
        state = game.play_turn(state)

if __name__ == '__main__':
    main()
