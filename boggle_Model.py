import boggle_board_randomizer
import ex12_utils
import time

WORD_FILE_PATH = "boggle_dict.txt"
BOARD_X_LEN = 4
BOARD_Y_LEN = 4
GAME_DURATION = 180


class Timer:
    """this class creates a countdown for game duration from the time it was initialized"""
    def __init__(self, game_duration=GAME_DURATION):
        self.start_time = None
        self.game_duration = game_duration

    def remaining_time(self):
        if self.start_time is None:
            raise ValueError("Game was not started!")
        return int(self.game_duration - (time.time() - self.start_time))

    def remaining_time_string(self):
        remaining_time = self.remaining_time()
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        return str(minutes) + ":" + str(seconds)

    def start(self):
        self.start_time = time.time()


class ScoreCalculator:
    """this class calculates the score for a list of words"""

    def get_score(self, word):
        """gets a word and calculates the score of that word.
        If the word is not in the dictionary, return 0. Otherwise, return len(word) ^ 2"""
        return len(word) ** 2

    def get_game_score(self, words):
        """gets a list of str and calculates the score of that list:
        each first appearance of word receives a score calculated by len(word) ** 2
        each further appearance of word is not scored"""
        word_set = set(words)
        score = 0
        for word in word_set:
            score += self.get_score(word)
        return score


class StepRecommender:
    """This class gets a path(list[tuples]) ,where the last tuple is the last step taken,
    and returns the next possible steps"""
    def get_all_neighbors(self, coordinate):
        """calculate all the neighbors coordinates in the board (regardless if they were already clicked or not)"""
        x, y = coordinate
        potential_neighbors = ex12_utils.get_neighbors(x, y)
        return [coord for coord in potential_neighbors if self._valid_coordinates(coord)]

    def _valid_coordinates(self, coordinate):
        """check if coordinate in board limits"""
        return 0 <= coordinate[0] < BOARD_X_LEN and 0 <= coordinate[1] < BOARD_Y_LEN

    def _board_coordinates(self):
        board_coordinates = []
        for i in range(BOARD_X_LEN):
            for j in range(BOARD_Y_LEN):
                board_coordinates.append((i, j))
        return board_coordinates

    def get_valid_neighbors(self, path):
        """path: List[tuples].
        get neighbors of the last tuple in path and returns the neighbors that are not already in the path."""
        if not path:
            return self._board_coordinates()
        last_step = path[-1]
        step_neighbors = self.get_all_neighbors(last_step)
        return [coord for coord in step_neighbors if coord not in path]


class Game:
    """this class manages a boggle game"""
    def __init__(self, board):

        self.board = board
        self.timer = Timer()
        self.score_calculator = ScoreCalculator()
        self.steprecommender = StepRecommender()

        self.words_dict = ex12_utils.load_words_dict(WORD_FILE_PATH)  # a list of valid words that can be found in board
        self.found_words = set()

    def add_new_word(self, word):
        if word in self.words_dict:
            self.found_words.add(word)

    def get_letter(self, row, col):
        return self.board[row][col]

    @property
    def score(self):
        return self.score_calculator.get_game_score(self.found_words)

    @property
    def remaining_game_time(self):
        return self.timer.remaining_time()







    # def create_current_path(self, current_path):
    #     """this function keeps receiving coordinates from user until they choose to check the word
    #     (meaning the word in the current path)"""
    #     while self.check_path is False:
    #         possible_steps = self.steprecommender.get_valid_neighbors(current_path)
    #         print("the valid next steps are", possible_steps)
    #         input_str = input("what's your next step?")
    #         next_step = (int(input_str[0]), int(input_str[1]))
    #         if next_step in possible_steps:
    #             current_path.append(next_step)
    #         else:
    #             print("the step isn't valid")
    #         check_input = input("would you like to check this word? enter Y/N")
    #         if check_input == "Y":
    #             self.check_path = True
    #     # print(self.current_path) # just a test

    # def from_current_path_get_word(self):
    #     """from current_path returns a str according to the matching str on board"""
    #     word = ""
    #     for coord in self.current_path:
    #         x, y = coord
    #         word += self.board[x][y]
    #     return word



# game = Game()
#
# game.create_current_path()
# print(game.from_current_path_get_word())







