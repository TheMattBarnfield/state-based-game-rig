"""Play a fixed depth minimax search"""
from player import Player
from draughts import DraughtsPiece

class MinimaxPlayer(Player):
    """Minimax class"""

    def __init__(self, depth, heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.depth = depth

    def move(self, game, state):
        """Make a move given the game state"""
        max_val = -2
        choice = -1
        for i, move in enumerate(game.get_moves(state)):
            node_value = -self.max(game, game.perspective_change(move), 0)
            if node_value > max_val:
                choice = i
                max_val = node_value
        return choice


    def max(self, game, state, depth):
        """
        Implements the minimax making use of the perspective_change funciton
        """
        value = game.evaluate(state)
        if not value == 0:
            return value
        elif depth == self.depth:
            return self.heuristic(state)
        else:
            max_val = -1
            for move in game.get_moves(state):
                min_val = -self.max(game, game.perspective_change(move), depth+1)
                if min_val > max_val:
                    max_val = min_val
            return max_val

    @classmethod
    def draughts_count_heuristic(cls, state):
        """focuses purely on piece count"""
        allies = 0
        enemies = 0
        for row in state['board']:
            for piece in row:
                if piece is DraughtsPiece.ALLY or piece is DraughtsPiece.ALLY_KING:
                    allies += 1
                elif piece is not DraughtsPiece.EMPTY:
                    enemies += 1
        return (allies-enemies)/(allies+enemies)
