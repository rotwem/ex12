import boggle_board_randomizer
import ex12_utils

WORD_FILE_PATH = "boggle_dict.txt"
BOARD_X_LEN = 4
BOARD_Y_LEN = 4


class ScoreCalculator:
    """this class calculates the score for a list of words"""

    def __init__(self):
        self.words_dict = ex12_utils.load_words_dict(WORD_FILE_PATH)  # a list of valid words that can be found in board

    def get_score(self, word):
        """gets a word and calculates the score of that word.
        If the word is not in the dictionary, return 0. Otherwise, return len(word) ^ 2"""
        if word in self.words_dict:
            return len(word) ** 2
        else:
            return 0

    def get_game_score(self, words_lst):
        """gets a list of str and calculates the score of that list:
        each first appearance of word receives a score calculated by len(word) ** 2
        each further appearance of word is not scored"""
        word_set = set(words_lst)
        score = 0
        for word in word_set:
            score += self.get_score(word)
        return score


class StepRecommender:
    """This class gets a path(list[tuples]) ,where the last tuple is the last step taken,
    and returns the next possible steps"""

    def __init__(self):
        self.board_coordinates = []
        for i in range(BOARD_X_LEN):
            for j in range(BOARD_Y_LEN):
                self.board_coordinates.append((i, j))

    def get_all_neighbors(self, coordinate):
        """calculate all the neighbors coordinates in the board (regardless if they were already clicked or not)"""
        x, y = coordinate
        potential_neighbors = ex12_utils.get_neighbors(x, y)
        return [coord for coord in potential_neighbors if coord in self.board_coordinates]

    def get_valid_neighbors(self, path):
        """path: List[tuples].
        get neighbors of the last tuple in path and returns the neighbors that are not already in the path."""
        last_step = path[-1]
        step_neighbors = self.get_all_neighbors(last_step)
        return [coord for coord in step_neighbors if coord not in path]
