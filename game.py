"""Module for abstract game class"""
from abc import ABC
from enum import Enum, unique

@unique
class GameState(Enum):
    """DraughtsPiece type enumeration"""
    ONGOING = 0
    WIN = 1
    DRAW = 2
    LOSS = 3

    def score(self):
        """Score each state from -1 to 1"""
        return [0, 1, 0, -1][int(self.value)]

    def __str__(self):
        return ['Ongoing', 'Win', 'Draw', 'Loss'][int(self.value)]

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
