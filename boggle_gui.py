import tkinter as tki
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

    def __init__(self, model: Game, root):
        self.root = root  # main window of the game
        self.model = model  # List[List[str]]
        self.frame = tki.Frame(root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR, highlightthickness=5,
                               width=10, height=10)
        self.frame.pack()
        self.buttons = dict()
        self.current_path = []

    def set_buttons_grid(self):
        """ for each coordinate create a button and place in grid according to coordinate"""
        for i in range(BOARD_Y_LEN):
            tki.Grid.columnconfigure(self.frame, i, weight=1)

        for i in range(BOARD_X_LEN):
            tki.Grid.rowconfigure(self.frame, i, weight=1)

        for row in range(BOARD_Y_LEN):
            for col in range(BOARD_X_LEN):
                self.buttons[(row, col)] = self._make_button(self.model.get_letter(row, col), row, col)

    def _make_button(self, button_char, row, col, rowspan=1, columnspan=1):
        """create button for each coord in board and binds click event to changing bg color"""
        button = tki.Button(self.frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)

        button.bind("<Button>", lambda event: self.button_clicked_handler((row, col)))

        return button

    def button_clicked_handler(self, coordinate):
        coord_possible_neighbors = self.model.steprecommender.get_valid_neighbors(self.current_path)
        if coordinate not in coord_possible_neighbors:
            return
        self.current_path.append(coordinate)
        possible_steps = self.model.steprecommender.get_valid_neighbors(self.current_path)
        for coord, button in self.buttons.items():
            if coord in self.current_path:
                button['background'] = CLICKED_BUTTON_BG
                continue
            if coord in possible_steps:
                button['background'] = POSSIBLE_NEXT_STEP_BG
                continue
            button['background'] = NEUTRAL_BG

    def reset_buttons_color(self):
        """resets the buttons to neutral color"""
        for button in self.buttons.values():
            button.configure(bg=NEUTRAL_BG)

    def run(self):
        # just for test
        self.set_buttons_grid()
        self.frame.mainloop()


class Countdown:
    """This class only manages the presentation of the time remaining for game"""

    def __init__(self, root, timer):
        self.root = root
        self.timer = timer
        self.time_var = tki.StringVar()
        self.label = tki.Label(root, bg=GAME_ORANGE_COLOR, textvariable=self.time_var, font=("Courier", 20))
        self.label.pack()
        self.root.after(10, self.set_remaining_time)

    def set_remaining_time(self):
        self.time_var.set(self.timer.remaining_time_string())
        self.root.after(10, self.set_remaining_time)


board = [['B', 'A', 'C', 'Y'],
         ['E', 'R', 'A', 'D'],
         ['N', 'E', 'T', 'I'],
         ['C', 'E', 'QU', 'H']]
# board = boggle_board_randomizer.randomize_board()

model = Game(board=board)

root = tki.Tk()
LG = LettersGrid(model, root)
timer = Timer()
timer.start()
CTD = Countdown(root, timer)
root.mainloop()
# LG.run()
