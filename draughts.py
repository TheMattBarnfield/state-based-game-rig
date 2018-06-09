"""Draughts game"""
from copy import deepcopy
from enum import Enum, unique
from itertools import product

from game import Game, GameState

@unique
class DraughtsPiece(Enum):
    """DraughtsPiece type enumeration"""
    ALLY_KING = 0
    ALLY = 1
    ENEMY = 2
    ENEMY_KING = 3
    EMPTY = 4

    def flip(self):
        """Flip piece to the other team"""
        if self is DraughtsPiece.EMPTY:
            return DraughtsPiece.EMPTY
        return DraughtsPiece(3-self.value)


    def is_ally(self):
        """Check if a piece is friendly"""
        return self is DraughtsPiece.ALLY or self is DraughtsPiece.ALLY_KING

    def is_enemy(self):
        """Check if a piece is an enemy"""
        return not self.is_ally() and self is not DraughtsPiece.EMPTY


    def king(self):
        """Promote a standard piece"""
        if self is DraughtsPiece.ALLY or self is DraughtsPiece.ENEMY:
            return DraughtsPiece(self.value*3 - 3)
        return self


    def __str__(self):
        return ['A', 'a', 'e', 'E', ' '][int(self.value)]


class Draughts(Game):
    """Game ABC"""

    def __init__(self, max_ply):
        super().__init__()
        self.max_ply = max_ply

    def new_game(self, players):
        state = super().new_game(players)
        state['ply'] = 0
        return state

    def initial_board(self):
        """Create the initial board"""
        board = []
        for _ in range(3):
            board.append([DraughtsPiece.ALLY]*4)
        for _ in range(2):
            board.append([DraughtsPiece.EMPTY]*4)
        for _ in range(3):
            board.append([DraughtsPiece.ENEMY]*4)
        return board

    @classmethod
    def get_moves(cls, state):
        """Get a list of states that can be moved to"""
        board = Draughts.unpack(state)
        take_moves = Draughts.get_take_moves(state, board)
        if take_moves:
            return take_moves
        return Draughts.get_normal_moves(state, board)


    @classmethod
    def get_normal_moves(cls, state, board):
        """All moves that don't include taking a piece"""
        moves = []

        for i, j in product(range(8), range(8)):

            piece = board[i][j]
            places_to_check = Draughts.get_move_directions(piece, i, j)

            for i_diff, j_diff in places_to_check:
                new_i = i + i_diff
                new_j = j + j_diff
                if board[new_i][new_j] is DraughtsPiece.EMPTY:
                    new_board = deepcopy(board)
                    if new_i == 7:
                        new_board[new_i][new_j] = piece.king()
                    else:
                        new_board[new_i][new_j] = piece
                    new_board[i][j] = DraughtsPiece.EMPTY
                    moves.append(Draughts.update_board(state, new_board))

        return moves


    @classmethod
    def get_take_moves(cls, state, board):
        """Find all complete moves that involve taking a piece"""
        take_moves = []
        for i, j in product(range(8), range(8)):
            piece = board[i][j]
            potential_takes = Draughts.takes_from(board, piece, i, j)
            while potential_takes:
                new_potential_takes = []
                for take, new_i, new_j in potential_takes:
                    chain = Draughts.takes_from(take, piece, new_i, new_j)
                    if chain:
                        new_potential_takes += chain
                    else:
                        take_moves.append(Draughts.update_board(state, take))
                potential_takes = new_potential_takes
        return take_moves


    @classmethod
    def get_move_directions(cls, piece, i, j):
        """Get the valid moves for your pieces"""
        places_to_check = []
        if piece.is_ally() and i < 7:
            if j > 0:
                places_to_check.append((1, -1))
            if j < 7:
                places_to_check.append((1, 1))

        if piece is DraughtsPiece.ALLY_KING and i > 0:
            if j > 0:
                places_to_check.append((-1, -1))
            if j < 7:
                places_to_check.append((-1, 1))
        return places_to_check


    @classmethod
    def takes_from(cls, board, piece, i, j):
        """Find any moves that take an opponent's piece"""
        places_to_check = Draughts.get_move_directions(piece, i, j)
        valid_takes = []
        for i_diff, j_diff in places_to_check:
            hop_i = i + i_diff
            hop_j = j + j_diff
            if board[hop_i][hop_j].is_enemy():
                new_i = i + 2*i_diff
                new_j = j + 2*j_diff
                if (
                        new_i < 8 and
                        new_i >= 0 and
                        new_j < 8 and
                        new_j >= 0 and
                        board[new_i][new_j] is DraughtsPiece.EMPTY
                ):
                    new_board = deepcopy(board)
                    if new_i == 7:
                        new_board[new_i][new_j] = piece.king()
                    else:
                        new_board[new_i][new_j] = piece
                    new_board[hop_i][hop_j] = DraughtsPiece.EMPTY
                    new_board[i][j] = DraughtsPiece.EMPTY
                    valid_takes.append((new_board, i + 2*i_diff, j + 2*j_diff))
        return valid_takes


    @classmethod
    def update_board(cls, state, board):
        """Get the state if the player and board changes"""
        return {
            'players' : state['players'],
            'turn'    : 1-state['turn'],
            'board'   : Draughts.pack(board),
            'ply'     : state['ply'] + 1
        }


    def perspective_change(self, state, new_player):
        new_state = state.copy()
        new_state['board'] = []
        for row in reversed(state['board']):
            new_row = []
            for piece in reversed(row):
                new_row.append(piece.flip())
            new_state['board'].append(new_row)
        return new_state


    def play_turn(self, state):
        return self.perspective_change(super().play_turn(state), 1-state['turn'])


    def evaluate(self, state):
        """Check for terminating state"""
        allies = 0
        enemies = 0
        if not Draughts.get_moves(state):
            return GameState.LOSS
        for row in state['board']:
            for piece in row:
                if piece.is_ally():
                    allies += 1
                elif piece.is_enemy():
                    enemies += 1
        if enemies == 0:
            return GameState.WIN
        if allies == 0:
            return GameState.LOSS
        if state["ply"] == self.max_ply:
            return GameState.DRAW
        return GameState.ONGOING

    @classmethod
    def unpack(cls, state):
        """Convert the board to an 8x8 array"""
        indent = False
        unpacked_board = []
        for row in state['board']:
            unpacked_row = []
            if indent:
                unpacked_row.append(DraughtsPiece.EMPTY)
            for piece in row:
                unpacked_row.append(piece)
                if len(unpacked_row) < 8:
                    unpacked_row.append(DraughtsPiece.EMPTY)
            indent = not indent
            unpacked_board.append(unpacked_row)
        return unpacked_board


    @classmethod
    def pack(cls, board):
        """Condense the board to remove unnecessary cells"""
        indent = 0
        packed_board = []
        for row in board:
            packed_row = []
            for i in range(4):
                packed_row.append(row[2*i + indent])
            indent = 1-indent
            packed_board.append(packed_row)
        return packed_board


    @classmethod
    def display(cls, state):
        """Display the current game state"""
        output = '-'*(8*2+1)+'\n'
        for row in reversed(cls.unpack(state)):
            for piece in row:
                output += '|' + str(piece)
            output += '|\n' + '-'*(8*2+1) + '\n'
        return output
