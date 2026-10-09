from abc import ABC, abstractmethod
import random
from bridge import best_move

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
        response = 0
        input_not_taken = True
        while input_not_taken == True:
            try:
                response = int(input('Enter which column to play in: '))
                input_not_taken = False
            except ValueError as err:
                print(f"(Error) {err}. Enter which column to play in: ")
        return response


# TODO: Create a CPUPlayer class which selects moves without user intervention
class RandomCPUPlayer(AbstractPlayer):
    def move(self, **kwargs):
        response = 0
        input_not_taken = True
        while input_not_taken == True:
            try:
                num_cols = kwargs["num_cols"]
                response = int(random.randint(0, (num_cols - 1)))
                input_not_taken = False
            except ValueError:
                pass
        return response

# TODO: Create a CPUPlayer class which selects moves without user intervention
class UnbeatableCPUPlayer(AbstractPlayer):
    #uses Pascal Pons connect 4 solver in the c++ files
    def move(self, **kwargs):
        #moves is the list of columns played so far in the order of the played moves
        return best_move(kwargs["moves"])