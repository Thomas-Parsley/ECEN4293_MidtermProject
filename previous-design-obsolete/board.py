_EMPTY = ' ' # Used to indicate empty spaces in the board

class InvalidMoveError(ValueError):
    pass

class ConnectFourBoard:

    """Represents a Connect 4 board. Handles board state and checks moves for validity."""

    def __init__(self, num_rows, num_cols):
        """Initialize a new board"""
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.clear()

    def clear(self):
        """Replace all pieces with empty spaces."""
        self.rows = list()
        for row in range(self.num_rows):
            self.rows.append([_EMPTY for col in range(self.num_cols)])

    def display(self):
        """Display the current board state"""
        for row in range(self.num_rows):
            print(f'\t|{"|".join(self.rows[row])}|')
        print('\t ' + ' '.join([str(col) for col in range(self.num_cols)]))

    def check_winner(self):
        """Check whether someone has won the game.""" #ideally done
        for row in range(self.num_rows): #loops through rows
            for col in range(self.num_cols): #nested loop through columns
                if self.rows[row][col] == _EMPTY: #if a space is empty, don't pay attention
                 continue
                # Check horizontal -> Checks if the given connect 4 is within the board's range and searches for a connect 4
                if col + 3 <self.num_cols and self.rows[row][col] == self.rows[row][col + 1] == self.rows[row][col +2] == self.rows [row][col + 3]:
                    return True
                # Check vertical -> Checks if the possible connect 4 is within the board's range and checks for a vertical connect 4
                if row + 3 <self.num_rows and self.rows[row][col] == self.rows[row + 1][col] == self.rows[row+2][col] == self.rows [row+3][col]:
                    return True
                # Check diagonal (up-right) -> Checks if the possible connect 4 is within the board's range and checks for an up-right (from left to right) connect 4
                if row - 3 >=0 and col + 3 < self.num_cols and self.rows[row][col] == self.rows[row - 1][col+1] == self.rows[row - 2][col+2]==self.rows[row-3][col+3]:
                    return True
                # Check diagonal (down-right) -> Checks if the possible connect 4 is withing the board's range and checks for a down-right (from left to right) connect 4
                if row + 3 <self.num_rows and col + 3 < self.num_cols and self.rows[row][col] == self.rows[row+1][col+1] == self.rows[row+2][col+2] == self.rows[row+3][col+3]:
                    return True
        return False # Not a win if none of the above conditions are met

    def is_full(self):
        """Check whether the board is full."""
        for row in range(self.num_rows): #Loops through rows
            for col in range(self.num_cols): #Nested loops through cols
                if self.rows[row][col] == _EMPTY: #If there is an empty space
                    return False #Return false, board is not full
        return True #True if there is no empty spaces

    def add_piece(self, col, symbol):
        """Add a piece to the specified column."""
        # TODO: Add code to check if the move is valid (and raise InvalidMoveError if not) 
        if col<0 or col>=self.num_cols:
            raise InvalidMoveError("Specified Location not in Range")
        #If specified column is not >0 and < total # of columns, it is invalid

        if self.rows[0][col] != _EMPTY:
            raise InvalidMoveError("Column is Full!")
        #If the specified column has no empty spaces, it will raise an error

        # Find the first empty row in col and replace it with symbol
        for row in reversed(range(self.num_rows)):
            if self.rows[row][col] == _EMPTY:
                self.rows[row][col] = symbol
                break


        