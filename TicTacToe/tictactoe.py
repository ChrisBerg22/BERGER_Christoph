"""A game of TicTacToe"""


import json

import numpy as np

from datetime import datetime
from warnings import warn

__version__ = "0.1.0"

class Board():
    """A grid of 3 by 3 where players can place
    their markers."""


    def __init__(self):
        """A Board for the game TicTacToe

        Attr:
          grid (np.array):   a grid onto which players can put their markers.
          last_move (int): the position of the last played marker.
        """
        self.grid = np.array([["","",""],["","",""],["","",""]])
        self.last_move = None


    def __str__(self):
        """A nice printable representation of the board

            Returns:
                String containing the printable representation of the board
        """
        row_1 = self.grid[0,0] + "|" + self.grid[0,1] + "|" + self.grid[0,2] + "\n"
        row_2 = self.grid[1,0] + "|" + self.grid[1,1] + "|" + self.grid[1,2] + "\n"
        row_3 = self.grid[2,0] + "|" + self.grid[2,1] + "|" + self.grid[2,2]  
        print(row_1 + row_2 + row_3)
        return (row_1 + row_2 + row_3)
        


    def place(self, position, marker="X"):
        """Place a marker in the given spot

        First checks if the spot chosen is valid. If the index does not
        exist (not between 1 and 9), raise a ValueError, saying the spot is out of bounds. If the
        spot is already taken, raise a ValueError saying that the spot is taken.

            TODO: maybe it would be best to put this check in a helper function
            ``is_valid(position)``

        Then, we place the marker in the given location on the grid.

        We record the position in self.last_move

        Args:
          self:  it is class method
          position (int): the position (between 1 and 9) where the marker should be placed. The positions on the grid must be as follows:

          1 | 2 | 3
          ---------
          4 | 5 | 6
          ---------
          7 | 8 | 9

          marker (str): X or O, the marker of the player
        """
        try:
            assert Board.is_valid(self, position) == True
        except:
            raise ValueError("Not a valid position: full or taken")
        else:
            row = position_to_coordinates(position)[0]
            col = position_to_coordinates(position)[1]
        
            self.grid[row,col] = marker
            self.last_move = self.grid[row,col]


    def is_valid(self, position):
        """helper function to determine if the move is allowed

        If the index does not exist, raise a ValueError, saying the position is
        out of bounds. If the position is taken, raise a ValueError saying that
        the spot is already taken.

        Args:
          position (int): the position number to be checked for validity

        Returns:
          Nothing. It either succeeds or raises an error.

        TODO: reconcile with Game.make_move
        """
        row = position_to_coordinates(position)[0]
        col = position_to_coordinates(position)[1]
        try:
            assert position>=1 and position<=9
        except:
            raise ValueError("Your position is out of bounds")
        else:
            try:
                assert self.grid[row,col] == ""
                return True
            except:
                raise ValueError("The spot is already taken")

    def show_marker(self, marker):
        """
        Returns an array of booleans where all spots with markers of either X or O (specified in the method's arguments) 

        Example:
            Board is:
            
            [["X", "X", "O"],
             ["X", "O", "X"],
             ["X", "",  ""]]
            
            show_marker("X") returns:

            [[True, True, False],
             [True, False, True],
             [True, False, False]]

        Args:
          - marker (str):  the chosen marker whose position will be True in the returned array

        Returns:
          - (np.array): An array with <marker> as ``True``, the rest ``False``.

        """
        return self.grid == marker

    def has_won(self):
        """check if one of the four winning conditions has occurred:

        - "horizontal"
        - "vertical"
        - "falling_diag"
        - "rising_diag"

        and rise a TimeoutError with the player's marker as the text if the game is won.
        """
        test_diag = diagonal(self.grid) # Diagonal win
        if test_diag[0] != "":
           test_equal = test_diag[0]
           count = np.count_nonzero(test_diag == test_equal)
           if count == 3:
               Winner = test_equal
               raise TimeoutError("Diagonal win: " + "Player " + Winner)
        test_andiag = antidiagonal(self.grid)   # Antidiagonal win
        if test_andiag[0] != "":
            test_equal = test_andiag[0]
            count = np.count_nonzero(test_andiag == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Antidiagonal win: " + "Player " + Winner)
        first_row = self.grid[0,:]   # Horizontal win
        if self.grid[0,0] != "":
            test_equal = self.grid[0,0]
            count = np.count_nonzero(first_row == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Horizonzal win: " + "Player " + Winner)
        second_row = self.grid[1,:]
        if self.grid[1,1] != "":
            test_equal = self.grid[1,0]
            count = np.count_nonzero(second_row == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Horizonzal win " + "Player " + Winner)
        third_row = self.grid[2,:]
        if self.grid[2,0] != "":
            test_equal = self.grid[2,0]
            count = np.count_nonzero(third_row == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Horizontal win: " + "Player " + Winner)
        first_column = self.grid[:,0] # Vertikal win
        if self.grid[1,0] != "":
            test_equal = self.grid[1,0]
            count = np.count_nonzero(first_column == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Vertikal win: " + "Player " + Winner)
        second_column = self.grid[:,1]
        if self.grid[0,1] != "":
            test_equal = self.grid[0,1]
            count = np.count_nonzero(second_column == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Vertikal win: " + "Player " + Winner)
        third_column = self.grid[:,2]
        if self.grid[0,2] != "":
            test_equal = self.grid[0,2]
            count = np.count_nonzero(third_column == test_equal)
            if count == 3:
                Winner = test_equal
                raise TimeoutError("Horizontal win: " + "Player " + Winner)
                                
    def is_full(self):
        """Checks if the grid is full and, if so, raises an IndexError"""
        testing_board_full = self.grid != ""
        if np.sum(testing_board_full) == 9:
            raise IndexError("The Board is already full")

def position_to_coordinates(position):
    """helper function: converts a given position (1 - 9) to coordinates (row, col) on the grid"""
    if position == 1:
        row, col = 0,0
    elif position == 2:
        row, col = 0,1
    elif position == 3:
        row, col = 0,2
    elif position == 4:
        row, col = 1,0
    elif position == 5:
        row, col = 1,1
    elif position == 6:
        row, col = 1,2
    elif position == 7:
        row, col = 2,0
    elif position == 8:
        row, col = 2,1
    elif position == 9:
        row, col = 2,2
    else:
        raise ValueError("Your are out of bounds")
    return [row, col]

def diagonal(grid):
    """helper function: find the diagonal of the board"""
    return grid.diagonal()


def antidiagonal(grid):
    """helper function: find the antidiagonal of the board"""
    return grid[::-1].diagonal()


class Player():
    """A player for the game

    Args:
        name (str):  the player's name
        marker (str): a marker for the player. Either X or O
    """
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

    def __str__(self):
        """The representation of Player is their name, so this method should return it"""
        return self.name

    @property
    def name(self):
        """Getter for the name variable
        
        Returns:
            Player's name
        """
        return self._name 

    @name.setter
    def name(self, value):
        """Setter for the name variable. It should prevent setting the name to an empty string by raising a ValueError

        Args:
            value (str): The string that should be set as the player's name

        """
        if value != "":
            self._name = value
        else:
            raise ValueError("Give a real name!")

    @property
    def marker(self):
        """Getter for the marker variable
        
        Returns:
            Player's marker
        """
        return self._marker

    @marker.setter
    def marker(self, value):
        """Setter fo the marker variable. It should prevent setting the marker to anything other than X or O (case insensitive) and transform every given value into upper case.
        When passed an illegal value, it should raise a ValueError

        Args:
            value (str): The marker that should be set for the player (either X or O, case insensitive)
        """
        if value.upper() == "X":
            self._marker = value.upper()
        elif value.upper() == "O":
            self._marker = value.upper()
        else:
            raise ValueError("Not a proper marker either X or O")


class Game():
    """A game of tictactoe"""
    def __init__(self, name_1="Alice", name_2="Bob", statistics="stats.json"):
        """Initialises a Game of TicTacToe

        Args:
          name_1 (str): the name of Player 1
          name_2 (str): the name of Player 2
          statistics (str): hall of fame filename to write the winner to

        Attr:
          self.board (Board): a board object
          self.player_1 (Player): will evaluate to Player with marker X
          self.player_2 (Player): will evaluate to Player with marker O
          self.statistics (str): hall of fame filename to write the winner to
          self._current (Player): The player that is to move next. Should be initialized by setting it to player_1
        """
        self.board = Board()
        self.player_1 = Player(name_1, marker = "X")
        self.player_2 = Player(name_2, marker = "O")
        self.statistics = statistics
        self.current = self.player_1
        
    @property
    def player_1(self):
        """Player 1"""
        return self._player_1


    @player_1.setter
    def player_1(self, value):
        """Set player 1"""
        self._player_1 = value


    @property
    def player_2(self):
        """Player 2"""
        return self._player_2


    @player_2.setter
    def player_2(self, value):
        """Set player 2"""
        self._player_2 = value

    def make_move(self):
        """Let the player in self._current make one move

         - get the current player's desired spot by running the ``query_spot`` method
         - put the player's marker down in the selected spot returned by the ``query_spot`` method. 
           Don't forget to handle errors raised by invalid moves and run the ``query_spot`` method again if
           necessary until a valid choice was made. 
         - check if a win has occurred: if so, raise a TimeoutError with a cheerful message
         - check if a draw has occurred: if so, raise a EOFError with a draw message
         """
        marker = self.current.marker 
        while True:

            position = self.query_spot()
            try:
                self.board.is_valid(position)
                break
            except ValueError:
                continue
        self.board.place(position,marker)
        self.board.__str__()
        try:
            self.board.has_won()
        except TimeoutError:
            print("Congratulations!!! You won: " + self.current.name)
        try:
            self.board.is_full()
        except IndexError:
            raise EOFError("It is a draw")
        if self.current == self.player_1:
            self.current = self.player_2
        else:
            self.current = self.player_1


        

    def query_spot(self):
        """
        Ask the player for a spot, then determine if the answer is an integer.
        If not, check if it was a "Q" or "q".
        If so, end the game without result by raising an EOFError.

        Return:
            The spot (int) the player chose for their marker

        """
        spot = input("Enter your spot: ")
        try:
            return int(spot)
        except:
            if spot == "q" or spot == "Q":
                raise EOFError("You quit the Game")

    def write_stats(self, player, filename="stats.json"):
        """appends the winner with timestamp to the statistics

        Args:
          player (str):   name to write down
          filename (str): filename of the hall of fame (assume it is a json)
        """
        pass
