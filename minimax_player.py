"""Play a fixed depth minimax search"""
from player import Player
from draughts import DraughtsPiece
from game import GameState

class MinimaxPlayer(Player):
    """Minimax class"""

    def __init__(self, depth=-1, heuristic=None):
        super().__init__()
        self.heuristic = heuristic
        self.depth = depth

    def move(self, game, state):
        """Make a move given the game state"""
        max_val = -2
        choice = -1
        for i, move in enumerate(game.get_moves(state)):
            node_value = -self.max(game, game.perspective_change(move), 0, -2, max_val)
            if node_value > max_val:
                choice = i
                max_val = node_value
        return choice


    def max(self, game, state, depth, alpha, beta):
        """
        Implements the minimax making use of the perspective_change funciton
        """
        gamestate = game.evaluate(state)
        if gamestate is not GameState.ONGOING:
            return gamestate.score()

        moves = game.get_moves(state)

        if len(moves) == 1:
            return -self.max(game, game.perspective_change(moves[0]), depth, beta, alpha)

        if depth == self.depth:
            return self.heuristic(state)

        max_val = -2
        for move in moves:
            node_val = -self.max(game, game.perspective_change(move), depth+1, beta, alpha)
            if node_val > max_val:
                max_val = node_val
            if node_val > alpha:
                alpha = node_val
            if max_val >= -beta:
                return max_val
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
