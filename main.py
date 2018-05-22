"""Module to play draughts with ML"""
from draughts import Draughts
from human_player import HumanPlayer
from random_player import RandomPlayer
from minimax_player import MinimaxPlayer

def main():
    """Program entrypoint"""
    matches = 10000
    view = False
    scores = [0, 0]
    game = Draughts()
    player_one = RandomPlayer()
    player_two = RandomPlayer()
    for _ in range(matches):
        state = game.new_game([player_one, player_two])
        while game.evaluate(state) == 0:
            if view and state['turn'] == 0:
                print(game.display(state))
            state = game.play_turn(state)
        scores[1-state['turn']] += 1
        print('Scores:'+ str(scores[0])+'-' + str(scores[1]))
    print('Final scores:'+ str(scores[0])+'-' + str(scores[1]))

if __name__ == '__main__':
    main()
