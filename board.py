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
        """Check whether someone has won the game."""
        # TODO: Implement this function instead of just returning false
        win = False
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                current_slot = self.rows[row][col]
                if (current_slot != _EMPTY):
                    #Up
                    if(row >= 3 and self.rows[row-1][col] == current_slot and self.rows[row-2][col] == current_slot and self.rows[row-3][col] == current_slot):
                        win = True
                    #Down
                    if(row <= (self.num_rows - 4) and self.rows[row+1][col] == current_slot and self.rows[row+2][col] == current_slot and self.rows[row+3][col] == current_slot):
                        win = True
                    #Left
                    if(col <= (self.num_cols - 4) and self.rows[row][col+1] == current_slot and self.rows[row][col+2] == current_slot and self.rows[row][col+3] == current_slot):
                        win = True
                    #Right
                    if(col >= 3 and self.rows[row][col-1] == current_slot and self.rows[row][col-2] == current_slot and self.rows[row][col-3] == current_slot):
                        win = True
                    #Up Right
                    if(row >= 3 and col <= (self.num_cols - 4) and self.rows[row-1][col+1] == current_slot and self.rows[row-2][col+2] == current_slot and self.rows[row-3][col+3] == current_slot):
                        win = True
                    #Up Left
                    if(row >= 3 and col >= 3 and self.rows[row-1][col-1] == current_slot and self.rows[row-2][col-2] == current_slot and self.rows[row-3][col-3] == current_slot):
                        win = True
                    #Down Right
                    if(row <= (self.num_rows - 4) and col <= (self.num_cols - 4) and self.rows[row+1][col+1] == current_slot and self.rows[row+2][col+2] == current_slot and self.rows[row+3][col+3] == current_slot):
                        win = True
                    #Down Left
                    if(row <= (self.num_rows - 4) and col >= 3 and self.rows[row+1][col-1] == current_slot and self.rows[row+2][col-2] == current_slot and self.rows[row+3][col-3] == current_slot):
                        win = True
        return win

    def is_full(self):
        """Check whether the board is full."""
        # TODO: Implement this function instead of just returning false
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                current_slot = self.rows[row][col]
                if current_slot == _EMPTY:
                    return False
        return True

    def add_piece(self, col, symbol):
        """Add a piece to the specified column."""
        # TODO: Add code to check if the move is valid (and raise InvalidMoveError if not)
        if (col >= self.num_cols or col < 0):
            raise InvalidMoveError("This column doesn't exist!")
        elif (self.rows[0][col] != _EMPTY):
            raise InvalidMoveError("Column is full!")

        # Find the first empty row in col and replace it with symbol
        for row in reversed(range(self.num_rows)):
            if self.rows[row][col] is _EMPTY:
                self.rows[row][col] = symbol
                break

