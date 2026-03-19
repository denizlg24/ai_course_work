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
        for c in range(max(0, col-3), min(NUM_COLUMNS-3, col)+1):
            if all(self.state[row][c+i] == player for i in range(4)):
                return True
        
        # check vertical
        for r in range(max(0, row-3), min(NUM_ROWS-3, row)+1):
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
        
        
        
        
        
        
        return points

class ConnectFourGame:
    
    def __init__(self, player_1, player_2, log = True):
        '''
        The player_1 and player_2 arguments are player objects, which should have a ``get_move`` method 
        for generating a move in the game, via player.get_move(self).
        '''
        
        self.log = log
        self.players = {1: player_1, 2: player_2}   # map player numbers to objects
    
    
    def play_game(self):
        '''
        Plays one Connect Four game and returns the winner (or 0 if we have a draw).
        '''
        
        # create a new board
        self.state = ConnectFourState()
        
        # force player_1 to play first or decide randomly who starts (1 or 2)
        self.state.current_player = 1
        #self.state.current_player = np.random.choice([1, 2])
        
        while self.state.game_over == False:
            # your code here
            move = self.players[self.state.current_player].get_move(self.state)
            self.state.move(move)
            self.state.current_player = 1 if self.state.current_player == 2 else 2

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
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    random_player_1 = RandomPlayer(name = 'random_1')
    random_player_2 = RandomPlayer(name = 'random_2')
    game = ConnectFourGame(random_player_1, random_player_2, log=True)
    game.play_game()
