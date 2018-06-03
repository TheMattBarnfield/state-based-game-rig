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
            node_value = -self.max(game, game.perspective_change(move), 0, max_val, -2)
            if node_value > max_val:
                choice = i
                max_val = node_value
        return choice


    def max(self, game, state, depth, alpha, beta):
        """
        Implements the minimax making use of the perspective_change funciton
        """
        value = game.evaluate(state).score()
        if not value == 0:
            return value

        moves = game.get_moves(state)

        if len(moves) == 1:
            return -self.max(game, game.perspective_change(moves[0]), depth, beta, alpha)

        if depth == self.depth:
            return self.heuristic(state)
        max_val = -1
        for move in moves:
            min_val = -self.max(game, game.perspective_change(move), depth+1, max_val, alpha)
            if min_val < -alpha:
                return min_val
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

    @classmethod
    def draughts_count_and_king_heuristic(cls, state):
        """same as count heuristic, but with kings worth double"""
        allies = 0
        enemies = 0
        for row in state['board']:
            for piece in row:
                if piece is DraughtsPiece.ALLY:
                    allies += 1
                elif piece is DraughtsPiece.ALLY_KING:
                    allies += 2
                if piece is DraughtsPiece.ENEMY:
                    enemies += 1
                elif piece is DraughtsPiece.ENEMY_KING:
                    enemies += 2
        return (allies-enemies)/(allies+enemies)

    @classmethod
    def draughts_offensive_heuristic(cls, state):
        """minimise number of opposing pieces"""
        enemies = 0
        for row in state['board']:
            for piece in row:
                if piece.is_enemy():
                    enemies += 1
        return 1-(2*enemies)/12

    @classmethod
    def draughts_defensive_heuristic(cls, state):
        """minimise number of opposing pieces"""
        allies = 0
        for row in state['board']:
            for piece in row:
                if piece.is_ally():
                    allies += 1
        return (2*allies)/12 - 1
