"""Module for abstract game class"""
from abc import ABC

class Game(ABC):
    """Game ABC"""

    def __init__(self):
        pass

    def new_game(self, players):
        """
        Begin a new game
        players is a list of the players of the new game_state
        """
        return {
            'players' : players,
            'turn'    : 0,
            'board'   : self.initial_board()
        }


    def initial_board(self):
        """Create the initial board"""
        pass

    def play_turn(self, state):
        """Have the next player make their turn"""
        moves = self.get_moves(state)
        current_player = state['players'][state['turn']]
        move = current_player.move(self, state)
        assert move >= 0 and move < len(moves)
        return moves[move]

    def get_moves(self, state):
        """List of states that can be accessed by a move"""
        pass

    def display(self, state):
        """Display the current game state"""
        pass

    def evaluate(self, state):
        """Determine a game winner"""
        pass
