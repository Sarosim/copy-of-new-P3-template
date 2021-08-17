# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 20 rows high.

from random import randrange, randint
import string
import readchar

# defining global variables
num_of_players = 1
players = []

class Board():
    """
    The Board object handling the game-board instances for both players

    properties: \n\trows (number of rows),\n\n\trow_headings,\n
    \n\tcols (number of cols)\n\n\tcol_headings,
    \n\tis_hidden (indicates if ships to be displayed),
    \n\tsquares (list of list for board square status
    \t{0: empty, 1: ship, 2: bomb exploded, 3: ship hit, 4: ship sunk})
    \n\tplayer_name,\n\n\tnum_of_ships (board size dependant)

    methods: \n\tdisplay() - prints the board
    \n\treveal() - prints the board with all info
    """
    def __init__(self, num_of_rows, num_of_cols, is_hidden, player_name):
        self.rows = num_of_rows
        self.row_headings = list(range(1, num_of_rows + 1))
        self.cols = num_of_cols
        self.col_headings = list(string.ascii_uppercase[:num_of_cols])
        self.is_hidden = is_hidden
        # initialise the empty board with zeros on each square
        #   - square statuses:
        #       0: empty
        #       1: ship
        #       2: bomb exploded
        #       3: ship hit
        #       4: ship sunk -- feature to be implemented later
        self.squares = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(0)
            self.squares.append(row)
        self.player_name = player_name
        self.num_of_ships = round(self.rows * self.cols / 25) + 1

    DISP_CHARS = [' ', 'O', '*', '#', '@']

    def display(self):
        """Displays the board according to the 'is_hidden' property"""
        print(f"\n{self.player_name}'s board:")

        # helper function to determine the character to be displayed
        def get_disp_char():
            disp_char = self.DISP_CHARS[self.squares[row_ind][col_ind]]
            if self.squares[row_ind][col_ind] == 1 and self.is_hidden:
                disp_char = self.DISP_CHARS[0]
            return disp_char

        # underlined text with '\033[4m'
        # all formatting options: PURPLE = '\033[95m'; CYAN = '\033[96m';
        # DARKCYAN = '\033[36m'; BLUE = '\033[94m'; GREEN = '\033[92m';
        # YELLOW ='\033[93m' RED ='\033[91m' BOLD ='\033[1m' END ='\033[0m'
        UNDERLINE = '\033[4m'
        # the Column headings
        prt_str = UNDERLINE + ' '
        for c in self.col_headings:
            prt_str += UNDERLINE + ' | ' + c
        prt_str += UNDERLINE + ' |'
        print(prt_str)

        # iterating through the rows and printing one by one
        for row_ind, r in enumerate(self.row_headings):
            prt_str = UNDERLINE + str(r)
            for col_ind in range(self.cols):
                prt_str += UNDERLINE + ' | '
                prt_str += get_disp_char()
            prt_str += UNDERLINE + " |"
            print(prt_str)
        print('\033[0m')

    def reveal(self):
        """Displays the board with all info (regardless of 'is_hidden'"""
        pass


def get_num_of_players():
    """
    Get user input for number of players.
    1 play against computer,
    2 play with friend
    """
    no_valid_input = True
    while no_valid_input:
        try:
            num_of_players = int(input("Number of players? (1 or 2)\n"))
            if num_of_players in (1, 2):
                no_valid_input = False
            else:
                raise ValueError
        except ValueError:
            print("\nOops!  That wasn't a valid entry.  Try again...\n\n"
                  "You can either play against the computer - enter 1"
                  "\nOr play against another person - enter 2\n")
    return num_of_players


def get_board_size():
    """Setting the board size with user input"""
    no_valid_input = True
    while no_valid_input:
        try:
            num_cols = int(input("Number of columns? (between 4 and 15)\n"))
            if num_cols in range(4, 16):
                no_valid_input = False
            else:
                raise ValueError
        except ValueError:
            print("\nOops!  That wasn't a valid entry.  Try again...\n\n"
                  "Enter an integer between 4 and 15\n")
    no_valid_input = True
    while no_valid_input:
        try:
            num_rows = int(input("Number of rows? (between 4 and 15)\n"))
            if num_rows in range(4, 16):
                no_valid_input = False
            else:
                raise ValueError
        except ValueError:
            print("\nOops!  That wasn't a valid entry.  Try again...\n\n"
                  "Enter an integer between 4 and 15\n")
    return (num_cols, num_rows)


def place_ships(board, is_human):
    """
    Function placing ships on a board.

    Parameters:
    - board: the Board calss instance to place the ships on
    - is_human: a boolean to indicate whether the user or algorithm sets ships
    \n\t(True: user input needed, False: set programmatically)
    """
    for _ in range(board.num_of_ships):
        no_valid_input = True
        while no_valid_input:
            try:
                ship_row = int(input("Please provide the number of the row "
                               "for the top left position of your ship: "))
                if ship_row in range(1, board.rows + 1):
                    no_valid_input = False
                else:
                    raise ValueError
            except ValueError:
                print("\nOops!  That wasn't a valid entry.  Try again...\n\n"
                      f"Enter an integer between 1 and {board.rows}\n")
        no_valid_input = True
        while no_valid_input:
            try:
                ship_col = (input("Please provide the letter of the column "
                                  "for the top left position of your ship: ")
                            .upper())
                if ship_col.upper() in board.col_headings:
                    no_valid_input = False
                else:
                    raise ValueError
            except ValueError:
                print("\nOops!  That wasn't a valid entry.  Try again...\n\n"
                      f"Enter a letter btw A and {board.col_headings[-1]}\n")
        print(board.num_of_ships, 'Row', ship_row, "Col", ship_col)


def orchestrate():
    """The main function that controls the gameflow"""
    play_again = True
    while (play_again):

        # get number of players (two players or against computer)
        num_of_players = get_num_of_players()

        # get player name(s)
        for i in range(num_of_players):
            # TODO need a verification, say min 3 chars, cannot be "Computer"
            players.append(input("Enter player name:\n").capitalize())

        # add 'Computer' to players list if not a two-player game
        if len(players) == 1:
            players.append("Computer")
        print(f"{players=}")

        # get board size
        board_dimensions = get_board_size()
        # print(board_dimensions)
        # print(type(board_dimensions))

        # Instantiate players' boards
        global pl_1_board
        pl_1_board = Board(
                    board_dimensions[1],
                    board_dimensions[0],
                    num_of_players == 2,
                    players[0]
                    )
        global pl_2_board
        pl_2_board = Board(
                    board_dimensions[1],
                    board_dimensions[0],
                    True,
                    players[1]
                    )
        pl_1_board.display()
        pl_2_board.display()

        # player 1 ship placement
        place_ships(pl_1_board, True)

        print("Play another game? (y/n) ")
        play_again = readchar.readchar() == b"y"
        print(play_again)


if __name__ == "__main__":
    orchestrate()
