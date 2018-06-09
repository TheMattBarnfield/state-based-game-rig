"""Monte Carlo Tree Search"""
import math
import time
import random

from player import Player
from game import GameState

class MCTSPlayer(Player):
    """Player that selects moves based on MCTS, with a preset time per move"""

    def __init__(self, time_limit, max_depth=-1):
        super().__init__()
        self.time_limit = time_limit
        self.max_depth = max_depth

    def move(self, game, state):
        if len(game.get_moves(state)) == 1:
            return 0
        start_time = time.time()
        root = {
            "state": state,
            "plays": 0,
            "wins": 0,
            "parent": None
        }
        root["children"] = self.expand(game, root)

        while time.time() - start_time < self.time_limit:
            current_node = root
            while current_node["children"]:
                current_node = current_node["children"][MCTSPlayer.select(current_node, True)]
            current_node["children"] = self.expand(game, current_node)
        return MCTSPlayer.select(root, False)


    @classmethod
    def select(cls, parent, explore):
        """Choose best child from an expanded parent node"""
        selection = -1
        max_score = -1
        for (choice, child) in enumerate(parent["children"]):
            score = MCTSPlayer.UCT(child, parent["plays"], explore)
            if score > max_score:
                max_score = score
                selection = choice
        return selection

    @classmethod
    def UCT(cls, child, total_plays, explore):
        """Upper Confidence Bound 1 applied to trees"""
        wins = child["wins"]
        plays = child["plays"]
        if explore:
            return (wins/plays) + math.sqrt(1.5*math.log(total_plays)/plays)
        return wins/plays

    def random_playout(self, game, node):
        """Play out a game with random moves and update the tree"""
        depth = 0
        active = True
        state = node["state"]
        result = game.evaluate(state)
        while depth != self.max_depth and result == GameState.ONGOING:
            depth += 1
            state = random.choice(game.get_moves(state))
            result = game.evaluate(state)
            active = not active

        score = result.score()
        if active:
            MCTSPlayer.back_prop(node, (score + 1)/2)
        else:
            MCTSPlayer.back_prop(node, 1-((score + 1)/2))

    @classmethod
    def back_prop(cls, node, result):
        """Propogate playout result up the tree"""
        finished = False
        while not finished:
            node["plays"] += 1
            node["wins"] += result
            result = 1-result
            if node["parent"] is None:
                finished = True
            else:
                node = node["parent"]


    def expand(self, game, parent):
        """Find the children of a parent node and add to the tree"""
        children = []
        for move in game.get_moves(parent["state"]):
            children.append({
                "state": move,
                "plays": 0,
                "wins": 0,
                "parent": parent,
                "children": []
            })
            self.random_playout(game, children[-1])

        return children
