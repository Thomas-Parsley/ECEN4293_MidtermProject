from abc import ABC, abstractmethod
from board import ConnectFourBoard
import random
import copy


class AbstractPlayer(ABC):
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def move(self, **kwargs):
        """Return an integer representing the column where the player intends to play a piece."""


class ConsolePlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Get which column to play in from the user via text console"""
        return int(input('Enter which column to play in: '))


# TODO: Create an UNBEATABLE CPUPlayer class which selects moves without user intervention
class CPUPlayer(AbstractPlayer):
    def __init__(self, symbol, name):
        super().__init__(symbol, name) #Comes from AbstractPlayer class, purely for naming (self.name, self.symbol)
        self.search_depth = 6 #How many moves ahead the AI will look, much more will cause time delays due to computation
    
    def can_move(self, board, col): #Checks if a move is valid or not
        return 0 <= col < board.num_cols and board.rows[0][col] == ' ' #returns true if col is from 0 to num_cols and the column is empty

    def simulate(self, board, col, symbol): #Simulates a move on a copied board
        for row in reversed(range(board.num_rows)): #Needs to be reversed so as the AI doesn't place a piece on row 0
            if board.rows[row][col] == ' ':
                board.rows[row][col] = symbol
                break

    def check_outcome(self, board, maximizing, opponent_symbol):

        if board.check_winner():
            return True
        
        if maximizing: #Same as other player win logic, If can win: place here
            for col in range(board.num_cols):
                if self.can_move(board, col):
                    temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
                    temp_board.rows = [row[:] for row in board.rows]
                    temp_board.add_piece(col, self.symbol)
                    if temp_board.check_winner():
                        return True
                    
        else: #Same as other player block logic, if opponent wins: place here
            for col in range(board.num_cols):
                if self.can_move(board, col):
                    temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
                    temp_board.rows = [row[:] for row in board.rows]
                    temp_board.add_piece(col, opponent_symbol)
                    if temp_board.check_winner():
                        return True
        return False

    def evaluate_window(self, window, opponent_symbol):
        score = 0

        ai_count = window.count(self.symbol) #Counts number of bot pieces
        opp_count = window.count(opponent_symbol) #Counts number of opponent pieces
        empty_count = window.count(' ') #Counts empty spaces

        if ai_count == 4: #If AI wins, give big score
            score += 1000

        elif ai_count == 3 and empty_count == 1: #If AI is about to win, give it a decent score
            score += 50

        elif ai_count == 2 and empty_count == 2: #If AI is halfway, give it a moderate score
            score += 10

        if opp_count == 3 and empty_count == 1: #If human is one move away from winning, give a negative score
            score -= 40

        if opp_count == 4:
            score -=1000

        return score

    def evaluate_board(self, board, opponent_symbol):
        score = 0 #Start with 0 score, add as we find good patterns

        #CENTER CONTROL: Priority for bot
        center_array=[board.rows[row][3] for row in range(board.num_rows)] #Array for column 3
        center_count = center_array.count(self.symbol) #How many spaces belong to the AI
        score += center_count * 3

        #Horizontal Windows
        for r in range(board.num_rows): #Each makes a window of horiz, vert, or diag, and checks where the best places to move will be based on window score, defined above
            for c in range(board.num_cols - 3):
                window = [board.rows[r][c+i] for i in range(4)] #Creates a group (window) of 4 cells left to right
                score += self.evaluate_window(window, opponent_symbol)

        #Vertical Windows
        for c in range(board.num_cols):
            for r in range(board.num_rows - 3):
                window = [board.rows[r+i][c] for i in range(4)] #Creates vertical window
                score += self.evaluate_window(window, opponent_symbol)

        #Down right windows
        for r in range(board.num_rows - 3):
            for c in range(board.num_cols - 3):
                window = [board.rows[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, opponent_symbol)

        #Up right windows
        for r in range(3, board.num_rows):
            for c in range(board.num_cols - 3):
                window = [board.rows[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, opponent_symbol)

        return score #returns total score, if AI is winning -> Positive, if not -> negative

    
    def minimax(self, board, depth, alpha, beta, maximizing, opponent_symbol):
        #if self.check_outcome(board, maximizing, opponent_symbol):#Is not maximizing = human turn, trying to minimize human score
            #return float('inf') if not maximizing else float('-inf') #Is maximizing = AI turn, trying to maximize score to beat human

        if board.is_full():
            return 0

        if depth == 0:
            return self.evaluate_board(board, opponent_symbol)


        if maximizing: #It is the AI's turn, robot looking for highest score, WIN LOGIC
            max_eval = float('-inf') #If I get a score better than this, I want it
            for col in range(board.num_cols):
                if self.can_move(board, col): #If I can move here
                    board_copy = copy.deepcopy(board) #make a deep copy
                    self.simulate(board_copy, col, self.symbol) #Simulate all moves
                    eval = self.minimax(board_copy, depth - 1, alpha, beta, False, opponent_symbol) #Switch to human turn, simulate
                    max_eval = max(max_eval, eval) #Did human turn give a better score than previously?
                    alpha = max(alpha, eval) #Move robot made now becomes new alpha
                    if beta <= alpha: #If human makes a move worse for me than I've seen, stop looking
                        break
            return max_eval #Return highest possible score
        else:
            min_eval = float('inf')#Pretend it is the human turn, BLOCK LOGIC
            for col in range(board.num_cols):
                if self.can_move(board, col): #I want to get the lowest possible score for the bot
                    board_copy = copy.deepcopy(board) #Copy current board
                    self.simulate(board_copy, col, opponent_symbol) #Simulate a move
                    eval = self.minimax(board_copy, depth - 1, alpha, beta, True, opponent_symbol) #Robot turn, what does robot do?
                    min_eval = min(min_eval, eval)#If robot responds in a way that minimizes its own score based on previous human move, it becomes new min
                    beta = min(beta, eval) #Beta is smallest possible score
                    if beta <= alpha: #If AI has a move better for them than I can make negative, stop looking
                        break
            return min_eval #return lowest score
    
    def move(self, board, opponent_symbol, diff="Super Hard"):
        best_score = float('-inf') #defines best score, will be replaced to track best moves
        best_col = None #Will be used to hold value based on best score
        valid_cols = [col for col in range(board.num_cols) if self.can_move(board, col)] #Determines if input column is valid via helper function
        if not valid_cols:
            return 0

        # for col in range(board.num_cols):
        #     if self.can_move(board, col):
        #         temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
        #         temp_board.rows = [row[:] for row in board.rows]
        #         temp_board.add_piece(col, self.symbol)
        #         if temp_board.check_winner():
        #             return col

        # for col in range(board.num_cols):
        #             if self.can_move(board, col):
        #                 temp_board = ConnectFourBoard(board.num_rows, board.num_cols)
        #                 temp_board.rows = [row[:] for row in board.rows]
        #                 temp_board.add_piece(col, opponent_symbol)
        #                 if temp_board.check_winner():
        #                     return col

        empty_board = True #If it is the first move of the game, Play in the 3rd column
        for row in range(board.num_rows): 
            for col in range(board.num_cols):
                if board.rows[row][col] != ' ': #loops through rows & cols to find a non-empty space
                    empty_board = False
                    break
            if not empty_board: #breaks early if found early to save time
                break
        if empty_board:
            return board.num_cols // 2 #If first move, play in third column

        for col in valid_cols:
            board_copy = copy.deepcopy(board) #creates full, independent copy of board
            self.simulate(board_copy, col, self.symbol) #Runs simulation
            score = self.minimax(board_copy, self.search_depth, float('-inf'), float('inf'), False, opponent_symbol) #Defines score based on minimax

            if score > best_score: 
                best_score = score #Finds best score, thus best move
                best_col = col #makes best move based on best col
                print("best score:", best_score)
                print("best col:", best_col)
        return best_col if best_col is not None else valid_cols[0] #Return best move based on minimax


