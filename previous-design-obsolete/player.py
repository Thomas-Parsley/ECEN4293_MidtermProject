from abc import ABC, abstractmethod
from board import ConnectFourBoard
import random


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


# TODO: Create a CPUPlayer class which selects moves without user intervention
class CPUPlayer(AbstractPlayer):
    def move(self, **kwargs):
        board = kwargs.get("board") #brings board from game.py
        opponent_symbol = kwargs.get("opponent_symbol") #brings opponent symbol from game.py
        diff = kwargs.get("diff") #brings diff from game.py
        
        if board is None:
            raise ValueError("Board not Found") #if no board, raise an error (debug line)
       
        #opponent_symbol = 'x' if self.symbol == 'o' else 'o' #defined oponent symbols only as x or o, previous setup
        
       #GO FOR THE WIN
        for col in range(board.num_cols): #Loops through cols
            if board.rows[0][col] ==' ': #if the column is not full
                temp_board = ConnectFourBoard(board.num_rows, board.num_cols) #create a temp board the size of the current board
                temp_board.rows=[row[:] for row in board.rows] #fill it with the values from the current board
                temp_board.add_piece(col, self.symbol) #add a piece to any spot
                if temp_board.check_winner(): #if adding the piece results in a win somewhere
                    return col #place the piece where it will win, if not keep going
                
        #GO FOR THE BLOCK
        for col in range(board.num_cols): #Loops through cols
            if board.rows[0][col] == ' ': #if column not full
                temp_board = ConnectFourBoard(board.num_rows, board.num_cols) #Make another temp board
                temp_board.rows=[row[:] for row in board.rows] #Fill it again        
                temp_board.add_piece(col, opponent_symbol) #Add opponent pieces to temp board
                if temp_board.check_winner(): #If the opponent can win somewhere

                    #EASY DIFFICULTY
                    if diff == "Easy": #And if you are on easy difficulty
                        if random.randint(1, 5) == 1: #A 5 sided dice will roll, and if it equals 1
                            blunder = [col for col in range(board.num_cols) if board.rows[0][col]==' '] #Pick a random spot on the board
                            return random.choice(blunder) #Place the piece, not blocking the opponent
                        else: #If the dice lands on 2-5
                            return col #Block the opponent

                    #MEDIUM DIFFICULTY    
                    elif diff == "Medium": #If on medium difficulty
                        if random.randint(1, 50) == 1: #Roll a 50 sided dice, if 1 turns up
                            blunder = [col for col in range(board.num_cols) if board.rows[0][col]==' '] #Pick a random spot
                            return random.choice(blunder) #Place the piece, not blocking the user
                        else: #if 2-50 turns up
                            return col #Block the user

                    #HARD DIFFICULTY    
                    elif diff == "Hard": #If on hard difficulty
                        if random.randint(1, 100) == 2: #roll 100 sided dice, and if 2 turns up (for funsies)
                            blunder = [col for col in range(board.num_cols) if board.rows[0][col]==' '] #Pick another random spot
                            return random.choice(blunder) #Blunder the block

                    #SUPER HARD DIFFICULTY    
                        else: #If 2-100 turns up
                            return col #Block user
                    elif diff == "Super Hard": #If super hard difficulty
                        return col #Never blunder   

        #GO FOR THE BEST MOVE
        all_columns=[3, 2, 4, 1, 5, 0, 6]
        preferred_columns = [3, 2, 4] #Prefer to play towards the middle of board, as it interacts with highest number of winning lines
        secondary_columns = [1, 5] #Second pick -> The closest to the middle
        tertiary_columns = [0, 6] #Last pick -> The outer columns
        for col in (all_columns): #Loop through all columns
            if board.rows[0][col] == ' ': #If a column isn't full

                #MOST LIKELY
                if random.randint(1, 60) in range (1, 35): #AND a 60 sided die turns up 1-40
                    return random.choice(preferred_columns) #Choose to play in the middle
                #SECOND MOST
                elif random.randint(1, 60) in range(36, 50): #If it turns up 36 -> 50
                    return random.choice(secondary_columns) #Play the closest to middle columns
                #LEAST LIKELY
                elif random.randint(1, 60) in range(51, 60):#If it turns up 51 -> 60
                    return random.choice(tertiary_columns) #Play the outer columns
           
        return 0  #ends move method
    #I feel like I went nutso bananas on this and am super proud  
                
       

    