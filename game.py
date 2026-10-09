from board import ConnectFourBoard, InvalidMoveError
from player import ConsolePlayer, RandomCPUPlayer, UnbeatableCPUPlayer
import matplotlib.pyplot as plt
import numpy as np

class ConnectFourGame:
    """Represents a Connect 4 game. Manages board and players."""

    def __init__(self, rows=6, cols=7, p1_type=ConsolePlayer):
        """Initialize a new game"""

        # Set up board
        self.board = ConnectFourBoard(rows, cols)

    def players_and_visual_setup(self):
        plt.close('all')
        self.use_visual = input("Use graphical display? (y/N): ").lower().startswith("y")

        #P1 Choice
        p1_choice = input("Do you want P1 to be: 1-Person 2-RandomCPU 3-UnbeatableCPU? (1/2/3):")
        p1_name = ""
        p1_not_chosen = True
        while p1_not_chosen:
            if(p1_choice == "2"):
                p1_type=RandomCPUPlayer
                p1_name = "CPU 1"
                p1_not_chosen = False
            elif (p1_choice == "1"):
                p1_type=ConsolePlayer
                p1_name = "Player 1"
                p1_not_chosen = False
            elif (p1_choice == "3"):
                p1_type=UnbeatableCPUPlayer
                p1_name = "Unbeatable CPU 1"
                p1_not_chosen = False
            if(p1_not_chosen):
                p1_choice = input("Please choose if you want P1 to be: 1-Person 2-RandomCPU 3-UnbeatableCPU? (1/2/3):")

        # P2 Choice
        p2_choice = input("Do you want P2 to be: 1-Person 2-RandomCPU 3-UnbeatableCPU? (1/2/3):")
        p2_name = ""
        op_not_chosen = True
        while op_not_chosen:
            if(p2_choice == "2"):
                p2_type=RandomCPUPlayer
                p2_name = "Normal CPU 2"
                op_not_chosen = False
            elif (p2_choice == "1"):
                p2_type=ConsolePlayer
                p2_name = "Player 2"
                op_not_chosen = False
            elif (p2_choice == "3"):
                p2_type=UnbeatableCPUPlayer
                p2_name = "Unbeatable CPU 2"
                op_not_chosen = False
            if(op_not_chosen):
                p2_choice = input("Please choose if you want P2 to be: 1-Person 2-RandomCPU 3-UnbeatableCPU? (1/2/3):")

        # Set up Players
        if not self.use_visual:
            p1_symbol = self.get_player_symbol(p1_name)
            p2_symbol = self.get_player_symbol(p2_name)
            while p2_symbol == p1_symbol:
                print("Player 2 can't have the same symbol as Player 1!")
                p2_symbol = self.get_player_symbol(p2_name)
        else:
            p1_symbol = "a"
            p2_symbol = "b"
        self.player_1 = p1_type(name=p1_name, symbol=p1_symbol)
        self.player_2 = p2_type(name=p2_name, symbol=p2_symbol)

        self.turn = 0

        #Pre defining stuff for other stuff
        self.fig = None
        self.ax = None
        self.has_clicked = False
        self.matplotlib_column_workaround_variable = None  

        if self.use_visual:
            self.setup_matplotlib()

    def start(self):
        """Begin playing a new game.

        Players take turns until either someone wins or the board is full."""

        # Clear the board
        self.board.clear()

        self.players_and_visual_setup()
        
        if self.use_visual:
            self.fig.suptitle(f"Connect Four\nClick any column to play there!", fontsize=14)

        self.turnorder = []

        # Main game loop
        while not self.board.is_full():
            # Figure out whose turn it is
            match self.turn % 2:
                case 0:
                    current_player = self.player_1
                case 1:
                    current_player = self.player_2
            if not self.use_visual:
                print(f"{current_player.name}'s turn.")
            else:
                self.fig.suptitle(f"Connect Four\n{current_player.name}'s turn. Click any column to play there!", fontsize=14)

            # Display the board
            if self.use_visual:
                self.visual_display()
            else:
                self.board.display()

            # Get the next player's move
            move_is_invalid = True
            while move_is_invalid: # Keep trying until we get a valid move
                if self.use_visual and isinstance(current_player, ConsolePlayer):
                    self.has_clicked = False
                    while not self.has_clicked:
                        plt.pause(0.1)
                    col = self.matplotlib_column_workaround_variable
                else:
                    col = current_player.move(num_cols=self.board.num_cols, moves=self.turnorder)
                    plt.pause(0.1)
                try:
                    self.board.add_piece(col, current_player.symbol)
                    self.turnorder.append(col)
                    move_is_invalid = False # If we make it to this line, move was valid
                except InvalidMoveError as err:
                    if not isinstance(current_player, (RandomCPUPlayer, UnbeatableCPUPlayer)):
                        print(f"(Error) {err}. Please Re-enter a column:") # Otherwise display why the move was not valid

            # Increment the turn count
            self.turn += 1

            # Check for winners
            if self.board.check_winner():
                if not self.use_visual:
                    print(f'{current_player.name} wins!')
                    self.board.display()
                    break # Get out of the while loop without triggering the else clause
                else:
                    self.fig.suptitle(f"Connect Four\n{current_player.name} wins! Start a new game in the console.", fontsize=14)
                    self.visual_display()
                    break # Get out of the while loop without triggering the else clause

        else:
            # If we reach this line, the board is full
            if not self.use_visual:
                print('No winner!')
            else:
                self.fig.suptitle(f"Connect Four\nNo winner! Start a new game in the console.", fontsize=14)
                self.visual_display()

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

    def setup_matplotlib(self):
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click) #apparently gets button presses

        self.ax.set_xlim(-0.5, self.board.num_cols - 0.5)
        self.ax.set_ylim(-0.5, self.board.num_rows - 0.5)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.visual_display()
        self.fig.suptitle("Connect Four\nClick any column to play there!", fontsize=14)
        plt.show(block=False)

    def visual_display(self):
        self.ax.clear()
        for row in range(self.board.num_rows):
            for col in range(self.board.num_cols):
                if self.board.rows[row][col] == self.player_1.symbol:
                    color = "red"
                elif self.board.rows[row][col] == self.player_2.symbol:
                    color = "yellow"
                else:
                    color = "white"
                self.ax.scatter(col, (self.board.num_rows - 1) - row, s=1000, color=color, edgecolors="black") # Circles :)DIOANicnaz

        #walls and floor
        for x in range(self.board.num_cols + 1):
            self.ax.axvline(x - 0.5, color="black", linewidth=2)
        self.ax.axhline(-0.5, color="black", linewidth=2)

        self.ax.set_xlim(-0.5, self.board.num_cols - 0.5)
        self.ax.set_ylim(-0.5, self.board.num_rows - 0.5)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        if event.xdata is None:
            return
        col = int(round(event.xdata)) #Since the stuff is from like -0.5 to 0.5, it should round to 0
        if 0 <= col <= (self.board.num_cols - 1):
            self.matplotlib_column_workaround_variable = col
            self.has_clicked = True

if __name__ == "__main__":
    # Play a new connect 4 game
    game = ConnectFourGame()

    keep_playing = True
    while keep_playing:
        game.start()
        keep_playing = input('Play again? (y/N): ').lower().startswith('y')
