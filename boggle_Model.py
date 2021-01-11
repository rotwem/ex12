import boggle_board_randomizer
import ex12_utils

WORD_FILE_PATH = "boggle_dict.txt"


class ScoreCalculator:
    """this class calculates the score for a list of words"""
    def __init__(self):
        self.words_dict = ex12_utils.load_words_dict(WORD_FILE_PATH) # a list of valid words that can be found in board

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
        each further appearance of word receives is not scored"""
        word_set = set(words_lst)
        score = 0
        for word in word_set:
            score += self.get_score(word)
        return score

