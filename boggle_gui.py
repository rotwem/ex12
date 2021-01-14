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

INSTRUCTIONS = "YOU HAVE 3 MINUTES TO FIND AS MANY WORDS AS YOU CAN\n IN THE RANDOM LETTERS IN THE GRID.\n" \
               "THE LETTERS YOU USE MUST BE TOUCHING\n VERTICALLY, HORIZONTALLY OR DIAGONALLY IN A CHAIN.\n" \
               "EACH WORD YOU FIND MUST BE AT LEAST 3 LETTERS LONG.\n THE LONGER THE WORD, THE HIGHER THE SCORE.\n" \
               "GOOD LUCK!"

ENTRY = "LET'S PLAY BOGGLE"
TOO_SHORT = "IS TOO SHORT"
TOO_LONG = "IS TOO LONG"
INVALID_WORD = "IS NOT A WORD"
FOUND = "YOU FOUND"
ALREADY_FOUND = "YOU ALREADY FOUND"
CLICK_TO_PLAY = "CLICK TO PLAY"
CLICK_TO_PLAY_AGAIN = "CLICK TO PLAY AGAIN"
START_OVER = "START OVER"
CHECK_WORD = "CHECK WORD"


class BoggleGui:
    """This class only manages the gui for the letters grid of buttons"""

    def __init__(self, model: Game):
        self.root = tki.Tk()  # main window of the game
        # these lines are for initializing the frames
        self.root.resizable(False, False)
        self.upper_frame = tki.Frame(self.root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR,
                                     highlightthickness=3,
                                     width=10,
                                     height=10)  # frame for message (label) + start over (button) + check word (button)
        self.upper_frame.pack()
        self.message_val = tki.StringVar()
        self.message_val.set(ENTRY)
        self.message_label = tki.Label(self.upper_frame, bg=GAME_BLACK_COLOR, fg=GAME_ORANGE_COLOR,
                                       font=("Courier", 20), textvariable=self.message_val)
        self.message_label.pack(expand=True)
        self.mid_frame = tki.Frame(self.root, bg=GAME_ORANGE_COLOR, highlightbackground=GAME_BLACK_COLOR,
                                   highlightthickness=3,
                                   width=10, height=10)  # frame for click to start (button) + timer and score(labels)
        self.mid_frame.pack()
        self.grid_frame = tki.Frame(self.root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR,
                                    highlightthickness=3,
                                    width=10, height=10)  # frame dor instructions (label) + letter grid (buttons grid)
        self.grid_frame.pack()
        self.instructions_label = tki.Label(self.grid_frame, text=INSTRUCTIONS, font=("Courier", 10))
        self.instructions_label.pack()
        self.found_words_frame = tki.Frame(self.root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR,
                                           highlightthickness=3,
                                           width=10, height=10)  # frame for found words
        self.found_words_title = tki.Label(self.found_words_frame, font=("Courier", 15), text="WORDS YOU FOUND",
                                           bg=GAME_ORANGE_COLOR)
        self.found_words_str = tki.StringVar()
        self.found_words_label = tki.Label(self.found_words_frame, font=("Courier", 10),
                                           textvariable=self.found_words_str)

        # LettersGrid
        self.model = model  # List[List[str]]
        # self.frame = tki.Frame(self.root, bg=NEUTRAL_BG, highlightbackground=GAME_BLACK_COLOR, highlightthickness=5,
        #                        width=10, height=10)
        # self.frame.pack()
        self.buttons = dict()
        self.current_path = []
        self.current_word = ""
        self.found_words = ""

        # countdown
        self.time_var = tki.StringVar()
        self.countdown_label = tki.Label(self.mid_frame, bg=GAME_ORANGE_COLOR, textvariable=self.time_var,
                                         font=("Courier", 20))
        self.current_score = 0
        self.score_val = tki.StringVar()
        self.score_label = tki.Label(self.mid_frame, bg=GAME_ORANGE_COLOR, textvariable=self.score_val,
                                     font=("Courier", 20))

        self.start_over_button = tki.Button(self.upper_frame, bg=NEUTRAL_BG, text=START_OVER, font=("Courier", 20))
        # self.start_over_button.bind("<Button>", lambda event: self.start_over())
        self.check_word_button = tki.Button(self.upper_frame, bg=NEUTRAL_BG, text=CHECK_WORD, font=("Courier", 20))
        self.check_word_button.bind("<Button>", lambda event: self.check_word())

        self.click_to_play = tki.Button(self.mid_frame, bg=GAME_ORANGE_COLOR, fg=GAME_BLACK_COLOR, text=CLICK_TO_PLAY)
        self.click_to_play.pack()
        self.click_to_play.bind("<Button>", lambda event: self.clicked_to_start())

    def set_buttons_grid(self):
        """ for each coordinate create a button and place in grid according to coordinate"""
        for i in range(BOARD_Y_LEN):
            tki.Grid.columnconfigure(self.grid_frame, i, weight=1)

        for i in range(BOARD_X_LEN):
            tki.Grid.rowconfigure(self.grid_frame, i, weight=1)

        for row in range(BOARD_Y_LEN):
            for col in range(BOARD_X_LEN):
                self.buttons[(row, col)] = self._make_button(self.model.get_letter(row, col), row, col)

    def _make_button(self, button_char, row, col, rowspan=1, columnspan=1):
        """create button for each coord in board and binds click event to changing bg color"""
        button = tki.Button(self.grid_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)

        button.bind("<Button>", lambda event: self.button_clicked_handler((row, col)))

        return button

    def button_clicked_handler(self, coordinate):
        coord_possible_neighbors = self.model.steprecommender.get_valid_neighbors(self.current_path)
        if coordinate not in coord_possible_neighbors:
            return
        self.current_path.append(coordinate)
        row, col = coordinate
        self.current_word += self.model.get_letter(row, col)
        self.message_val.set(self.current_word)
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

    def set_remaining_time(self):
        """set the time string in countdown label"""
        self.time_var.set(self.remaining_time_string(self.model.remaining_game_time))
        self.root.after(10, self.set_remaining_time)

    def remaining_time_string(self, remaining_time):
        minutes = str(remaining_time // 60)
        seconds = str(remaining_time % 60)
        if len(minutes) < 10:
            minutes = "0" + minutes
        if len(seconds) < 2:
            seconds = "0" + seconds
        return minutes + ":" + seconds

    def start_over(self):
        self.model = Game(boggle_board_randomizer.randomize_board())

    def clicked_to_start(self):
        self.instructions_label.forget()
        self.click_to_play.forget()
        self.set_buttons_grid()
        self.model.start_game()
        self.countdown_label.pack(side=tki.LEFT, expand=True)
        self.root.after(10, self.set_remaining_time)
        self.score_val.set("SCORE: 0")
        self.score_label.pack(side=tki.RIGHT, expand=True)
        self.start_over_button.pack(side=tki.LEFT)
        self.check_word_button.pack(side=tki.RIGHT)
        self.found_words_frame.pack()
        self.found_words_title.pack()
        self.found_words_label.pack()

    def check_word(self):
        if len(self.current_word) < 3:
            self.message_val.set('"' + self.current_word + '" ' + TOO_SHORT)
            self.clear_word()
            return
        valid_word = self.model.add_new_word(self.current_word)
        if not valid_word:
            self.message_val.set('"' + self.current_word + '" ' + INVALID_WORD)
            self.clear_word()
            return
        game_score = self.model.score_calculator.get_game_score(self.model.found_words)
        if game_score > self.current_score:
            self.current_score = game_score
            self.score_val.set("SCORE: " + str(game_score))
            self.message_val.set(FOUND + ' "' + self.current_word + '"')
            self.found_words += self.current_word + ", "
            self.found_words_str.set(self.found_words)
            self.clear_word()
            return
        self.message_val.set(ALREADY_FOUND + ' "' + self.current_word + '"')
        self.clear_word()

    def clear_word(self):
        self.current_path = []
        self.current_word = ""
        self.reset_buttons_color()




    def game_handler(self):
        pass

    def run(self):
        # just for test
        # self.set_buttons_grid()
        self.root.mainloop()
        print(self.current_path)


board = [['B', 'A', 'C', 'Y'],
         ['E', 'R', 'A', 'D'],
         ['N', 'E', 'T', 'I'],
         ['C', 'E', 'QU', 'H']]
# board = boggle_board_randomizer.randomize_board()

model = Game(board=board)

BG = BoggleGui(model)
BG.run()
# LG.run()
