"""Module for tic tac toe"""
from game import GameState, Game
from enum import Enum, unique

@unique
class TTTPiece(Enum):
    """Tic Tac Toe pieces"""
    ALLY = 0
    ENEMY = 1
    EMPTY = 2

    def flip(self):
        """Flip piece to the other team"""
        if self is TTTPiece.EMPTY:
            return TTTPiece.EMPTY
        return TTTPiece(1-self.value)

    def __str__(self):
        return ['A', 'E', ' '][int(self.value)]

class Tictactoe(Game):
    """Tic tac toe"""

    def initial_board(self):
        """Create the initial board"""
        board = []
        for _ in range(9):
            board.append(TTTPiece.EMPTY)
        return board


    def perspective_change(self, state, new_player):
        """Flip the game state to the other player's point of view"""
        new_state = {
            'players' : state['players'],
            'turn'    : state['turn'],
            'board'   : [],
        }
        for piece in state['board']:
            new_state['board'].append(piece.flip())
        return new_state


    def get_moves(self, state):
        moves = []
        for i, piece in enumerate(state['board']):
            if piece is TTTPiece.EMPTY:
                new_state = {
                    'players' : state['players'],
                    'turn'    : 1-state['turn'],
                    'board'   : state['board'].copy(),
                }
                new_state['board'][i] = TTTPiece.ALLY
                moves.append(new_state)
        return moves


    def play_turn(self, state):
        return self.perspective_change(super().play_turn(state), state['turn'])

    def display(self, state):
        line = '-' * (2*3 + 1) + '\n'
        output = line
        for row in Tictactoe.pack(state['board']):
            for piece in row:
                output += '|' + str(piece)
            output += '|\n' + line
        return output


    @classmethod
    def pack(cls, board):
        packed = []
        for i in range(3):
            packed.append([])
            for j in range(3):
                packed[-1].append(board[i*3 + j])
        return packed


    def evaluate(self, state):
        board = Tictactoe.pack(state['board'])
        avenues = board.copy()
        diag = []
        diag2 = []
        for i in range(3):
            avenue = []
            for j in range(3):
                avenue.append(board[j][i])
            avenues.append(avenue)
            diag.append(board[i][i])
            diag2.append(board[i][2-i])
        avenues.append(diag)
        avenues.append(diag2)
        for row in avenues:
            row_val = row[0]
            for piece in row:
                if row_val is not piece:
                    row_val = TTTPiece.EMPTY
            if row_val is TTTPiece.ALLY:
                return GameState.WIN
            elif row_val is TTTPiece.ENEMY:
                return GameState.LOSS
        if TTTPiece.EMPTY in state['board']:
            return GameState.ONGOING
        return GameState.DRAW
