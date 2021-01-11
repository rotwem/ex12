import boggle_board_randomizer
import ex12_utils

WORD_FILE_PATH = "boggle_dict.txt"


class BoggleModel:
    def __init__(self):
        self.__game_words = ex12_utils.load_words_dict(WORD_FILE_PATH)
        self.__board = boggle_board_randomizer.randomize_board()
        self.__timer = None
        self.__current_path = []
        self.__current_word = None
        self.__score = 0

    def get_board(self):
        return self.__board

    def init_board(self):
        self.__board = boggle_board_randomizer.randomize_board()

    def set_score(self):
        add = len(self.__current_word) ** 2
        self.__score += add

    def check_path(self):
        pass

    def start_timer(self):
        pass

    def add_to_cur_path(self, coordinate):
        self.__current_path.append(coordinate)

    def clear_cur_path(self):
        self.__current_path = []
