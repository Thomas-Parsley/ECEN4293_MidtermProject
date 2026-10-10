import matplotlib.pyplot as plt
import matplotlib.patches as patches
from board import InvalidMoveError
from UnbeatablePlayer import CPUPlayer

####For Matplotlib info, I used primarily matplotlib.org documentation and Ecosia AI for debugging/functionality questions####

class ConnectFourGUI:
    def __init__(self, game): #initialize gui game

        self.game = game 
        self.board = game.board
        self.player_1 = game.player_1
        self.player_2 = game.player_2 #Variable setup
        self.current_player = self.player_1 #Current player always starts as player 1
        self.cpu_player = self.player_2 if isinstance(self.player_2, CPUPlayer) else None #If self.player_2 associated with CPUPlayer (in game.py), player2=CPU
        self.fig, self.ax = plt.subplots() #Create matplotlib figure & axis for board drawing
        self.circle_patches = [] #Stores circles for updating the board
        self.draw_board() #Draw first board
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click) #Connecting mouse click as an event to place chips

    def draw_board(self): #Create the board
        self.ax.clear() #Clear previous game's state
        self.ax.set_xlim(-0.5, self.board.num_cols -0.5) #Set x limits to column number plus a half unit margin
        self.ax.set_ylim(-0.5, self.board.num_rows -0.5) #Same thing for y
        self.ax.set_aspect('equal') #Ensures circles stay as circles and do not warp
        self.ax.invert_yaxis() #Makes top of board column 0 and bottom column 5, the same as the rest of the board logic uses
        

        for row in range(self.board.num_rows): #Loops through rows
            for col in range(self.board.num_cols): #Loops through columns
                cell = self.board.rows[row][col] #Defines "cell" as an individual space on the board
                if cell == self.player_1.symbol: #If the cell is played by player 1
                    color = 'red' #color it red
                elif cell == self.player_2.symbol: #else
                    color = 'yellow' #color it yellow
                else: #else
                    color = 'white' #leave it blank

                circle = patches.Circle((col, row), 0.4, edgecolor='black', facecolor=color) #creates a circle centered at (col, row) with 0.4 radius, with black edges and a color defined above 
                self.ax.add_patch(circle) #adds circle to the board
                self.circle_patches.append(circle) #adds where the circle is to the above list for future reference
            self.fig.canvas.draw() #updates the screen based on where the circles are placed


    def on_click(self, event): #defines event on click
        if event.inaxes != self.ax: #If the click is out of bounds
            return #return, do not place
        col = int(round(event.xdata)) #if the click is in bounds, round the nearest x data value and save within col

        try:
            self.board.add_piece(col, self.current_player.symbol) #add current player's symbol to the board
        except InvalidMoveError: #unless it's invalid
            print("Invalid Move, try another spot") 
            return
        self.draw_board() #Draw the updated board

        if self.board.check_winner(): #Checks if you've won based on method from board.py
            print(f"{self.current_player.name} wins!")
            print("Close window for new game")
            self.fig.canvas.mpl_disconnect(self.cid)
            return

        if self.board.is_full(): #Checks if board is full based on method from board.py
            print("DRAW!")
            print("Close window for new game")
            self.fig.canvas.mpl_disconnect(self.cid)
            return

        self.switch_turns() #Change from player 1 turn to player 2

        if self.cpu_player and self.current_player == self.cpu_player: #If player 2 is CPU
            while True:
                cpu_col = self.cpu_player.move(board=self.board, opponent_symbol=self.player_1.symbol, diff = "Super Hard") #Use CPU class from player.py
                try:
                    self.board.add_piece(cpu_col, self.cpu_player.symbol) #Try adding a piece
                    break
                except InvalidMoveError: #if no work, raise error and try again
                    print("Column Full")
                    continue

            self.draw_board() #Update board

            if self.board.check_winner(): #Checks if CPU won
                print(f"{self.cpu_player.name} wins!")
                print("Close window for new game")
                self.fig.canvas.mpl_disconnect(self.cid)
                return
            if self.board.is_full(): #Checks for CPU draw
                print("DRAW!")
                print("Close window for new game")
                self.fig.canvas.mpl_disconnect(self.cid)
                return

            self.switch_turns() #Switches turns

    def switch_turns(self): #Defines switching turns method
        if self.current_player == self.player_1: #If current player is player 1
            self.current_player = self.player_2 #Change to player 2
        else:
            self.current_player = self.player_1 #If it isn't, change to player 1

    def run(self): #Runs gui
        plt.show() #Brings up matplot
