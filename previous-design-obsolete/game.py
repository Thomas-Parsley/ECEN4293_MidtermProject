from board import ConnectFourBoard, InvalidMoveError
from UnbeatablePlayer import ConsolePlayer, CPUPlayer

class ConnectFourGame:
    """Represents a Connect 4 game. Manages board and players."""

    def __init__(self, rows=6, cols=7, p1_type=ConsolePlayer, p2_type=ConsolePlayer, diff = "Super Hard"):
        """Initialize a new game"""
        while True:
            try:
                p1_type1 = int(input("Enter 1 for P1 console, Enter 2 for P1 CPU: "))
                if p1_type1 == 1:
                    p1_type = ConsolePlayer
                    break
                elif p1_type1 == 2:
                    p1_type = CPUPlayer
                    break
                else:
                    print("Invalid input, need 1 or 2")
            except ValueError:
                print("Invalid input, need 1 or 2")

        while True: #Runs while true
            try: #Tries a user input if they want a local console match or a CPU match
                p2_type1=int(input("Enter 1 for P2 console, Enter 2 for P2 CPU: ")) #Prompts user to choose
                if p2_type1 == 1: #If player chooses 1
                    p2_type = ConsolePlayer #It will be a local console match
                    break #End while true loop
                elif p2_type1 == 2: #If user chooses two
                    p2_type = CPUPlayer #It will be a CPU match
                    break #Ends while true loop
                else:
                    print("Invalid input, need 1 or 2") #If any other input, a try-catch statement is used
            except ValueError: #Value error raised, prompts user again
                print("Invalid Input, need 1 or 2")
        while True:
                    interface_choice = int(input("Choose interface: 1-Console, 2-GUI: "))
                    if interface_choice == 1:
                        self.interface = "console"
                        break
                    elif interface_choice == 2:
                        self.interface = "gui"
                        print("You have chosen GUI!")
                        print("Player symbols must be entered, but they will not be necessary")
                        print("Click the column in which you would like to place your piece. Good Luck!")
                        break
                    else:
                        print("Please enter a 1 or 2")      

        # while True: #Second while true loop to choose difficulty of game
        #     try: #Another try-catch statement for difficulty
        #         diff=int(input("Choose a difficulty - 1:Easy, 2:Medium, 3:Hard, or 4:Super Hard: ")) #Prompts user to choose difficulty, casts to int
        #         if diff == 1: #If user types 1
        #             self.diff = "Easy" #Difficulty set to easy
        #             break #Break while true loop
        #         elif diff == 2: #if user types 2
        #             self.diff = "Medium" #Difficulty set to medium
        #             break #Break while true loop 
        #         elif diff == 3: #If user types 3 
        #             self.diff = "Hard" #Difficulty set to hard
        #             break #Break while true loop
        #         elif diff == 4:  #If the user types 4
        #             self.diff = "Super Hard" #Difficulty set to super hard
        #             break #Break while true loop
        #         else: print("Invalid input, retype 1, 2, 3, or 4 for Easy, Medium, Hard, or Super Hard difficulty respectively") #If 1, 2, 3, or 4 is not inputted
        #     except ValueError: #Raises ValueError if unexpected input is caught
        #         print("Invalid input, retype 1, 2, 3, or 4 for Easy, Medium, Hard, or Super Hard difficulty respectively") #Same as before

        # Set up board
        self.board = ConnectFourBoard(rows, cols)

        # Set up Players
        p1_symbol = self.get_player_symbol("Player 1")
        p2_symbol = self.get_player_symbol("Player 2")
        while p2_symbol == p1_symbol:
            print("Player 2 can't have the same symbol as Player 1!")
            p2_symbol = self.get_player_symbol("Player 2")
        self.player_1 = p1_type(name='Player 1', symbol=p1_symbol)
        self.player_2 = p2_type(name='Player 2', symbol=p2_symbol)

        self.turn = 0

    def start(self):
        """Begin playing a new game.

        Players take turns until either someone wins or the board is full."""

        # Clear the board
        self.board.clear()
        if self.interface == "console":

            # Main game loop
            while not self.board.is_full():
                # Figure out whose turn it is
                match self.turn % 2:
                    case 0:
                        current_player = self.player_1
                    case 1:
                        current_player = self.player_2
                print(f"{current_player.name}'s turn.")

                # Display the board
                self.board.display()

                # Get the next player's move
                move_is_invalid = True
                while move_is_invalid: # Keep trying until we get a valid move
                    if current_player == self.player_1:
                        opponent_sym = self.player_2.symbol
                    else:
                        opponent_sym = self.player_1.symbol
                    col = current_player.move(board=self.board, opponent_symbol=opponent_sym, diff = "Super Hard") #Included opponent_symbol and diff to be used in player.py
                    try:
                        self.board.add_piece(col, current_player.symbol)
                        move_is_invalid = False # If we make it to this line, move was valid
                    except InvalidMoveError as err:
                        print(str(err)) # Otherwise display why the move was not valid

                # Increment the turn count
                self.turn += 1

                # Check for winners
                if self.board.check_winner():
                    self.board.display()
                    print(f'{current_player.name} wins!')
                    break # Get out of the while loop without triggering the else clause
            else:
                # If we reach this line, the board is full
                print('No winner!')
        elif self.interface == "gui":
                    from gui import ConnectFourGUI
                    gui =ConnectFourGUI(self)
                    gui.run()

    def get_player_symbol(self, player_name):
        """Request a valid symbol to use for a player."""
        symbol_is_invalid = True
        while symbol_is_invalid:
            symbol = input(f'Enter a character to use as a symbol for {player_name}: ')
            symbol = symbol.strip() # Remove leading and trailing whitespace
            symbol = symbol[0] # Only keep the first character, ignore everything else
            if not symbol:
                print('Symbol must not be a whitespace character!')
            else:
                # Get positive confirmation from the player
                confirmation = input(f'Use "{symbol}" for {player_name}? (y/N): ')
                symbol_is_invalid = not confirmation.lower().startswith('y')
        return symbol


if __name__ == "__main__":
    # Play a new connect 4 game
    game = ConnectFourGame()

    keep_playing = True
    while keep_playing:
        game.start()
        keep_playing = input('Play again? (y/N): ').lower().startswith('y')
