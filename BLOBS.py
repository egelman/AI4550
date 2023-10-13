from games import Game
from games import GameState
import random
import numpy as np
from games import random_player
from collections import namedtuple

GameState = namedtuple('GameState', 'to_move, utility, board, moves, last_move')
depth_limit = 3
board_hw = 5

def copy_board(board):
        return [row[:] for row in board]

#########################BLOBS Game######################
class BLOBS(Game):
    instance_count = 0

    def __init__(self, N=board_hw):
        self.N = N
        board = [['-' for _ in range(N)] for _ in range(N)]
        board[0][0] = 'X'
        board[0][N-1] = 'O'
        board[N-1][0] = 'O'
        board[N-1][N-1] = 'X'
        
        self.initial = GameState(to_move='X', utility=0, board=board, moves=self.get_all_moves(board, 'X'), last_move=None)
    
    def actions(self, state):
        return state.moves

    def get_all_moves(self, board, color):
        moves = []
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == color:
                    moves.extend(self.legal_moves(board, i, j))
        return moves
    
    def legal_moves(self, board, x, y):
        moves = []
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.N and 0 <= ny < self.N and board[nx][ny] == '-':
                    if abs(dx) <= 1 and abs(dy) <= 1:  # adjacent
                        moves.append((x, y, nx, ny, "new"))
                    elif 1 < abs(dx) <= 2 or 1 < abs(dy) <= 2:  # Jump
                        moves.append((x, y, nx, ny, "jump"))
                    else:
                        moves = None
        return moves
    
    def result(self, state, move):
        #print("Original board:", state.board)
        x, y, nx, ny, action = move  
        new_board = copy_board(state.board)
        player = state.to_move  # Get the color of the current player
        
        if action == "new":  #adjacent
            new_board[nx][ny] = player
        elif action == "jump":  # jump
            new_board[x][y] = '-'  # Remove from original position
            new_board[nx][ny] = player  # Place in new position
        
        next_player = 'O' if player == 'X' else 'X'
        # Return the resulting state
        return GameState(to_move=next_player, utility=self.utility(new_board, next_player), board=new_board, moves=self.get_all_moves(new_board, next_player), last_move=move)
    
    def terminal_test(self, state):
        if state.last_move is None and not state.moves:
            return True  # Both players passed consecutively
        return len(state.moves) == 0  # No available moves

    def utility(self, board, player):
        if not isinstance(board, list):
            raise ValueError(f"Expected a 2D list (board) but got {type(board)} with value {board}")
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        if player == 'X':
            return x_count - o_count
        else:
            return o_count - x_count


    def display_result(self, state):
        x_count = sum(row.count('X') for row in state.board)
        o_count = sum(row.count('O') for row in state.board)
        if x_count > o_count:
            print("Player X wins!\nwith {} points\n".format(x_count))
        elif o_count > x_count:
            print("Player O wins!\nwith {} points\n".format(o_count))
        else:
            print("It's a tie!\n")
        
    def display(self, state):
        board = state.board
        for x in range(self.N):
            for y in range(self.N):
                print(board[x][y], end=' ')
            print()
        
    def play_game(self, *players):
        state = self.initial
        consecutive_passes = 0  
        while True:
            for player in players:
                move = player(self, state)
                if move is None:
                    consecutive_passes += 1
                else:
                    consecutive_passes = 0
                    state = self.result(state, move)
                if self.terminal_test(state) or consecutive_passes >= 2:  # Modify this line
                    self.display(state)
                    return state  # Return the final state
                
    def evaluation(self, state):
        player = state.to_move
        opponent = 'O' if player == 'X' else 'X'

        # Count blobs for player and opponent once
        player_blobs = 0
        opponent_blobs = 0
        for row in state.board:
            player_blobs += row.count(player)
            opponent_blobs += row.count(opponent)

        material_advantage = player_blobs - opponent_blobs

        return material_advantage 



def minmax_decision(game, state, depth=depth_limit, eval_fn=None, cutoff_test=None):
    eval_fn = eval_fn or game.evaluation
    cutoff_test = cutoff_test or (lambda state, depth: depth <= 0 or game.terminal_test(state))

    def max_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth - 1))
        return v

    def min_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth - 1))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), depth-1))



######################Implementing Players and Strategies######################
def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None

def minmax_player(game, state):
    return minmax_decision(game, state)

#Random vs Random
game_instance = BLOBS(board_hw) 
print("Random vs Random") 
final_state = game_instance.play_game(random_player, random_player)
game_instance.display_result(final_state)

#Random vs Minmax
game_instance = BLOBS(board_hw) 
print("Random vs Minimax w Cutoff")
final_state = game_instance.play_game(random_player, minmax_player)
game_instance.display_result(final_state)
print("Depth Limit: {}".format(depth_limit))



   