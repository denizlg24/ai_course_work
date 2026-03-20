import numpy as np
import time
NUM_ROWS = 6
NUM_COLUMNS = 7


class ConnectFourState:
    
    def __init__(self):
        
        # initial board state (empty board)
        self.state = np.zeros((NUM_ROWS, NUM_COLUMNS))
        
        # players
        self.player_1 = 1   # player 1 symbol
        self.player_2 = 2   # player 2 symbol
        self.current_player = self.player_1
        
        # game status
        self.game_over = False   # track if game has ended
        self.winning_player = 0   # store the player that wins, when the game is over (0 if we have a draw)
    
    
    def __str__(self):
        return str(self.state)
    
    
    def game_draw(self):
        '''
        Checks if the game has ended with  a draw.
        '''
        return self.game_over == True and self.winning_player == 0;
    
    
    def available_moves(self):
        '''
        Returns a list with the available moves (columns that are not full).
        '''
        # your code here
        return [col for col in range(NUM_COLUMNS) if self.state[0][col] == 0]
    
    
    def move(self, column):
        '''
        Implements a move of the current player for the given column.
        After the move, checks if the player has won or if the game has ended with a draw.
        '''
        
        # find the lowest empty position in the column and place piece there (current_player)
        # your code here
        for row in range(NUM_ROWS - 1, -1, -1):
            if self.state[row][column] == 0:
                self.state[row][column] = self.current_player
                break
        
        # check if won
        if(self.is_winner(row, column)):
            self.game_over = True
            self.winning_player = self.current_player
        else:
            # check if game has ended
            if(len(self.available_moves()) == 0):   #if there are no more available moves
                self.game_over = True
                self.winning_player = 0
        
        # change players turn
        self.current_player = self.player_2 if self.current_player == self.player_1 else self.player_1
        
        return
    
    
    def is_winner(self, row, col):
        '''
        Checks if the player that played in the (row, col) position has made a 4-line (horizontally, vertically, or diagonally).
        '''
        
        player = self.state[row][col]
        
        # your code here
        # check horizontal
        for c in range(max(0, col-3), min(NUM_COLUMNS-4, col)+1):
            if all(self.state[row][c+i] == player for i in range(4)):
                return True
        
        # check vertical
        for r in range(max(0, row-3), min(NUM_ROWS-4, row)+1):
            if all(self.state[r+i][col] == player for i in range(4)):
                return True
        
        # check diagonal (top-left to bottom-right)
        for d in range(-3, 1):
            if all(0 <= row+d+i < NUM_ROWS and 0 <= col+d+i < NUM_COLUMNS and self.state[row+d+i][col+d+i] == player for i in range(4)):
                return True
        
        # check diagonal (bottom-left to top-right)
        for d in range(-3, 1):
            if all(0 <= row-d+i < NUM_ROWS and 0 <= col+d+i < NUM_COLUMNS and self.state[row-d+i][col+d+i] == player for i in range(4)):
                return True

        
        return False
    
    
    def number_of_lines_with_four_pieces(self, player):
        """
        Gets the number of lines (horizontal, vertical, diagonal) where the player has at least 4 pieces
        (not necessarily consecutive).
        """
        
        n_four_pieces_lines = 0
        
        # Horizontal check:
        for row in range(NUM_ROWS):
            if((self.state[row] == player).sum() >= 4):
                n_four_pieces_lines += 1
        
        # Vertical check:
        # your code here
        for col in range(NUM_COLUMNS):
            if((self.state[:, col] == player).sum() >= 4):
                n_four_pieces_lines += 1
        
        
        
        # Diagonals
        # your code here
        for d in range(-NUM_ROWS + 1, NUM_COLUMNS):
            if((np.diag(self.state, d) == player).sum() >= 4):
                n_four_pieces_lines += 1
            if((np.diag(np.fliplr(self.state), d) == player).sum() >= 4):
                n_four_pieces_lines += 1
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        return n_four_pieces_lines
    
    
    def number_of_winning_spots(self, player):
        """
        Gets the number of consecutive 4 positions in a line (horizontal, vertical, diagonal) 
        where 3 are player pieces and 1 is empty.
        """
        
        n_winning_spots = 0
        
        # Horizontal check:
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS-3):
                pieces = [self.state[row][col], self.state[row][col+1],
                          self.state[row][col+2], self.state[row][col+3]]
                #check if we found a 4-position sequence with 3 instances of the current player and 1 empty spot
                if pieces.count(player) == 3 and pieces.count(0) == 1:
                    n_winning_spots += 1
        
        # Vertical check:
        # your code here
        for col in range(NUM_COLUMNS):
            for row in range(NUM_ROWS-3):
                pieces = [self.state[row][col], self.state[row+1][col],
                          self.state[row+2][col], self.state[row+3][col]]
                if pieces.count(player) == 3 and pieces.count(0) == 1:
                    n_winning_spots += 1
        
        # Diagonal - Top-Left to Bottom-Right:
        # your code here
        
        
        for col in range(NUM_COLUMNS-3):
            for row in range(NUM_ROWS-3):
                pieces = [self.state[row][col], self.state[row+1][col+1],
                          self.state[row+2][col+2], self.state[row+3][col+3]]
                if pieces.count(player) == 3 and pieces.count(0) == 1:
                    n_winning_spots += 1
        
        
        
        
        # Diagonal - Bottom-Left to Top-Right:
        # your code here
        
        
        for col in range(NUM_COLUMNS-3):
            for row in range(3, NUM_ROWS):
                pieces = [self.state[row][col], self.state[row-1][col+1],
                          self.state[row-2][col+2], self.state[row-3][col+3]]
                if pieces.count(player) == 3 and pieces.count(0) == 1:
                    n_winning_spots += 1
        
        
        
        
        return n_winning_spots
    
    
    def central_points(self, player):
        """
        Assigns 2 points to each player piece in the center column of the board (column 4)
        and 1 point to each piece in the columns around it (columns 3 and 5).
        """
        points = 0
        # your code here
        for row in range(NUM_ROWS):
            if self.state[row][3] == player:
                points += 1
            if self.state[row][4] == player:
                points += 2
            if self.state[row][5] == player:
                points += 1
        
        
        
        
        
        return points

class ConnectFourGame:
    
    def __init__(self, player_1, player_2, log = True):
        '''
        The player_1 and player_2 arguments are player objects, which should have a ``get_move`` method 
        for generating a move in the game, via player.get_move(self).
        '''
        
        self.log = log
        self.players = {1: player_1, 2: player_2}   # map player numbers to objects
        self.state = ConnectFourState()
        self.state.current_player = 1
        self.game_over = False
    
    
    def play_game(self):
        '''
        Plays one Connect Four game and returns the winner (or 0 if we have a draw).
        '''
        
        # create a new board
        
        # force player_1 to play first or decide randomly who starts (1 or 2)
        #self.state.current_player = np.random.choice([1, 2])
        
        while self.state.game_over == False:
            # your code here
            move = self.players[self.state.current_player].get_move(self.state)
            self.state.move(move)

        if self.state.game_draw():
            if self.log:
                print(f"\nGame over! The Game ended with a draw!")
                print(self.state.state)
            return 0
        else:
            if self.log:
                print(f"\nGame over! {self.players[self.state.winning_player].name} (Player_{self.state.winning_player}) won!")
                print(self.state.state)
            return self.state.winning_player
    
    
    def run_n_matches(self, n, log = False):
        pass
    

class Player:
    
    def get_move(self, game):
        # This method should be implemented by subclasses
        raise NotImplementedError("Subclasses must implement this method")


class RandomPlayer(Player):
    
    def __init__(self, name):
        self.name = name
    
    def get_move(self, game):
        return np.random.choice(game.available_moves())
    
class HumanPlayer(Player):
    
    def __init__(self,name):
        self.name = name
    
    def get_move(self, game):
        '''
        Returns a move as chosen by the user. The user choice is validated to ensure it is an available move.
        '''
        print("Available moves:", game.available_moves())
        while True:
            try:
                move = int(input(f"Enter your move (0-6): "))
                if move in game.available_moves():
                    return move
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")
        
        
def eval_game_over(game_state, player):
    if game_state.game_over:
        if game_state.winning_player == 0:
            return 0
        else:
            if game_state.winning_player == player:
                return 1000
            else: return -1000
    else: return 0

def eval1(game_state, player):
    if game_state.game_over:
        return eval_game_over(game_state, player)
    return game_state.number_of_lines_with_four_pieces(player) - game_state.number_of_lines_with_four_pieces(3 - player)
    
    

def eval2(game_state, player):
    if game_state.game_over:
        return eval_game_over(game_state, player)
    return 100 * eval1(game_state, player) + 10 * game_state.number_of_winning_spots(player) - 10 * game_state.number_of_winning_spots(3 - player)
    # your code here
    
    

def eval3(game_state, player):
    if game_state.game_over:
        return eval_game_over(game_state, player)
    return 100 * eval1(game_state, player) + game_state.central_points(player) - game_state.central_points(3 - player)
    # your code here
    
    

def eval4(game_state, player):
    if game_state.game_over:
        return eval_game_over(game_state, player)        
    return 5 * eval2(game_state, player) + eval3(game_state, player)
        

import copy

class MinimaxPlayer(Player):
    
    def __init__(self, name, eval_func, depth):
        self.name = name
        self.eval_func = eval_func
        self.depth = depth
    
    
    def _simulate_move(self, game_state, column):
        """Create a copy of game_state with the move applied"""
        
        new_state = copy.deepcopy(game_state)
        new_state.move(column)
        return new_state
    
    
    def get_move(self, game_state):
        """Find the best move using the Minimax alpha-beta algorithm"""
        
        move = self.minimax_alpha_beta_search(game_state)
        return move
    
    
    def minimax_alpha_beta_search(self, game_state):
        '''
        Returns the move with the best minimax value.
        '''
        
        player = game_state.current_player
        _, move = self.max_value(game_state, self.depth, float('-inf'), float('inf'), player)
        return move
    
    
    def max_value(self, state, depth, alpha, beta, original_player):
        '''
        Returns the evaluation and the move with the max minimax value.
        '''
        print(f"Max: depth={depth}, alpha={alpha}, beta={beta}, state=\n{state}\n")
        if depth == 0 or state.game_over:
            # Evaluate always from the perspective of the AI that started the search
            return self.eval_func(state, original_player), None
        
        # your code here
        value = float('-inf')
        best_move = None
        for move in state.available_moves():
            new_state = self._simulate_move(state,move)
            new_value, _ = self.min_value(new_state, depth-1, alpha, beta, original_player)
            if new_value > value:
                value = new_value
                best_move = move
            if value >= beta:
                return value, best_move
            alpha = max(alpha, value)
        
        return value, best_move
    
    def min_value(self, state, depth, alpha, beta, original_player):
        '''
        Returns the evaluation and the move with the min minimax value.
        '''
        if depth == 0 or state.game_over:
            # Evaluate always from the perspective of the AI that started the search
            return self.eval_func(state, original_player), None
        
        value = float('inf')
        best_move = None
        for move in state.available_moves():
            new_state = self._simulate_move(state,move)
            new_value, _ = self.max_value(new_state, depth-1, alpha, beta, original_player)
            if new_value < value:
                value = new_value
                best_move = move
            if value <= alpha:
                return value, best_move
            beta = min(beta, value)
        return value, best_move
        # your code here
        
        
        
        
        
        

if __name__ == "__main__":
    # random_player_1 = RandomPlayer(name = 'random_1')
    # random_player_2 = HumanPlayer(name = 'human_2')
    minimax_player_1 = MinimaxPlayer(name = 'minimax_1', eval_func=eval1, depth=4)
    minimax_player_2 = MinimaxPlayer(name = 'minimax_2', eval_func=eval2, depth=5)
    game = ConnectFourGame(minimax_player_1, minimax_player_2, log=True)
    game.play_game()
