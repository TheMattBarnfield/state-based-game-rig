"""Simple human-controlled player"""
from player import Player

class HumanPlayer(Player):
    """Takes input for moves via console"""

    def move(self, game, state):
        moves = game.get_moves(state)
        for i, move in enumerate(moves):
            print('~~MOVE: '+str(i)+'~~\n' + game.display(move))
        return int(input('Pick a move (0-'+str(len(moves)-1)+'): '))
