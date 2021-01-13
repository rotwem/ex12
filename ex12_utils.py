import boggle_board_randomizer
import itertools


BOARD_COORDINATES = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3),
                     (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]


def load_words_dict(file_path):
    word_dict = dict()
    f = open(file_path)
    for line in f:
        word = line[:-1]
        word_dict[word] = True
    f.close()
    return word_dict


def is_valid_path(board, path, words):
    if not valid_path(path):
        return None
    word_lst = []
    for coordinate in path:
        x, y = coordinate
        word_lst.append(board[x][y])
    word = "".join(word_lst)
    if word in words:
        return word
    else:
        return None


def valid_path(path):
    for i in range(len(path)-1):
        x, y = path[i]
        if path[i+1] not in get_neighbors(x, y):
            return False
    return True


def get_neighbors(x, y):
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x-1, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1)]

# dict_list = load_words_dict("boggle_dict.txt")
# board = [['B', 'A', 'C', 'Y'],
# ['E', 'R', 'A', 'D'],
# ['N', 'E', 'T', 'I'],
# ['C', 'E', 'QU', 'H']]

# for row in board:
#     print(row)
#
# path = [(0,0),(0,1),(0,2),(0,3)]
#
# print(is_valid_path(board, path, dict_list))


def find_length_n_words(n, board, words):
    """returns all the words with n length that are in board
    notice that the len is according to how many coordinates not how many letters are in coordinate"""
    valid_paths_words = []
    for path in itertools.combinations(BOARD_COORDINATES, n):
        if valid_path(path):
            word_lst = []
            for coordinate in path:
                x, y = coordinate
                word_lst.append(board[x][y])
            word = "".join(word_lst)
            if word in words:
                valid_paths_words.append((word, list(path)))
    return valid_paths_words

#print(find_length_n_words(4, board, dict_list))


