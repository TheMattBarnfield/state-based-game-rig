"""Module containing player ABC"""
from abc import ABC

class Player(ABC):
    """Abstract base class for a player"""

    def __init__(self):
        pass

    def move(self, game, state, moves):
        """Make a move given the game state"""
        pass
