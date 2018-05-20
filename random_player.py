"""Player that randomly chooses moves each turn"""
import random

from player import Player

class RandomPlayer(Player):
    """Purely random player"""

    def __init__(self):
        super().__init__()
        random.seed()

    def move(self, game, state, moves):
        return random.randint(0, len(moves)-1)
