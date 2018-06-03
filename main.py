"""Module to play draughts with ML"""
from draughts import Draughts
from game import GameState
from human_player import HumanPlayer
from random_player import RandomPlayer
from minimax_player import MinimaxPlayer
from mcts_player import MCTSPlayer

def main():
    """Program entrypoint"""
    matches = 2
    view = True
    scores = [0, 0]
    game = Draughts(100)
    player_one = MCTSPlayer(120, 100)
    player_two = MinimaxPlayer(3, MinimaxPlayer.draughts_count_heuristic)
    for match in range(matches):
        state = None
        if match % 2 == 0:
            state = game.new_game([player_one, player_two])
        else:
            state = game.new_game([player_two, player_one])
        while game.evaluate(state) is GameState.ONGOING:
            if view and state['turn'] == match%2:
                print(game.display(state))
            state = game.play_turn(state)
        score = game.evaluate(state).score()
        score = (score+1)/2
        if match % 2 == 0:
            turn = state['turn']
        else:
            turn = 1-state['turn']
        scores[turn] += score
        scores[1-turn] += 1-score
        print('Scores:'+ str(scores[0])+'-' + str(scores[1]))
    print('Final scores:'+ str(scores[0])+'-' + str(scores[1]))

if __name__ == '__main__':
    main()
