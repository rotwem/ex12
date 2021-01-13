import tkinter as tki
import tktimer
import boggle_board_randomizer
from boggle_Model import *

# game colors:
NEUTRAL_BG = 'white smoke'
CLICKED_BUTTON_BG = 'AntiqueWhite4'
POSSIBLE_NEXT_STEP_BG = 'gold'
GAME_ORANGE_COLOR = 'DarkOrange1'
GAME_BLACK_COLOR = 'black'
BOARD_X_LEN = 4
BOARD_Y_LEN = 4
BUTTON_STYLE = {"font": ("Courier", 40),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": NEUTRAL_BG}


class LettersGrid:
    """This class only manages the gui for the letters grid of buttons"""
    def __init__(self, board, root):
        self.root = root # main window of the game
        self.board = board # List[List[str]]
        self.frame = tki.Frame(root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR, highlightthickness=5,
                               width=10, height=10)
        self.frame.pack()
        self.buttons = dict()

    def set_buttons_grid(self):
        """ for each coordinate create a button and place in grid according to coordinate"""
        for i in range(BOARD_Y_LEN):
            tki.Grid.columnconfigure(self.frame, i, weight=1)

        for i in range(BOARD_X_LEN):
            tki.Grid.rowconfigure(self.frame, i, weight=1)

        for row in range(BOARD_Y_LEN):
            for col in range(BOARD_X_LEN):
                self._make_button(self.board[row][col], row, col)


    def _make_button(self, button_char, row, col, rowspan=1, columnspan=1):
        """create button for each coord in board and binds click event to changing bg color"""
        button = tki.Button(self.frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self.buttons[(row, col)] = button

        def change_clicked_button(event):
            button['background'] = CLICKED_BUTTON_BG

        button.bind("<Button>", change_clicked_button)

        return button

    def color_possible_steps(self, possible_steps):
        """color the possible next steps in a different color
        possible_steps: List[tuples]"""
        for coord in possible_steps:
            self.buttons[coord].configure(bg=POSSIBLE_NEXT_STEP_BG)

    def reset_buttons_color(self):
        """resets the buttons to neutral color"""
        for button in self.buttons.values():
            button.configure(bg=NEUTRAL_BG)

    def run(self):
        # just for test
        self.set_buttons_grid()
        self.color_possible_steps([(0,0),(1,1),(2,2),(3,3)])
        self.reset_buttons_color()
        self.frame.mainloop()

class Countdown:
    """This class only manages the presentation of the time remaining for game"""
    def __init__(self, root, timer):
        self.timer = timer
        self.root = root
        self.countdown = tktimer.Countdown(root, beginning=GAME_DURATION, unit='second', precision=0)
        self.countdown.pack()
        self.countdown.start()

    def convert_seconds_to_minutes(self):
        pass

    def display_countdown(self):
        self.countdown.configure(text=str(self.timer.remaining_time()))
        self.label.after(10, func=self.display_countdown())




board = [['B', 'A', 'C', 'Y'],
['E', 'R', 'A', 'D'],
['N', 'E', 'T', 'I'],
['C', 'E', 'QU', 'H']]

root = tki.Tk()
LG = LettersGrid(board, root)
timer = Timer()
CTD = Countdown(root, timer)
root.mainloop()



