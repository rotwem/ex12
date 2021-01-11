from string import ascii_lowercase
from random import choices
from tkinter import *

class Boggle():
    def __init__(self, file='boggle_dict.txt', size=5):
        self.size = size   
        self.solution = []      #parameter for ckSoln method
        self.readData(file)     #imports trie, frequency, and counts data structures
        self.board = [ choices(list(self.frequency.keys()), weights=self.counts, k=self.size)
                       for i in range(self.size) ]
        #creates self.size by self.size game board with letters randomly allocated from counts data
        #structure using random_choices module
        self.window = Tk()
        self.window.title('Boggle')
        self.canvas = Canvas(self.window, width = self.size*20, height = self.size*20, bg='white')
        self.canvas.pack()
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20)
                self.canvas.create_text(i*20+10, j*20+10, text=self.board[j][i])
        #self.board is applied to the TK interface window
        self.canvas.bind("<Button-1>", self.extend)     #selects letters
        self.canvas.bind("<Button-2>", self.new)        #resets state of game, keeps same board
        self.canvas.bind("<Button-3>", self.reset)      #resets state of game and board

    def readData(self, file):
        F = open(file)
        words = [ line.strip() for line in F ]
        F.close()
        #frequency function creates a dictionary with letters from the file as keys and the frequency
        #of those letters as values
        def frequency():
            d = {}
            for word in words:
                for letter in word:
                    if letter not in d:
                        d[letter] = 0
                    else:
                        d[letter] = d[letter] + word.count(letter)
            return({v:d[v]/sum(d.values()) for v in d})
        #trie function creates a deeply nested dictionary of dictionary with letters of each words
        #as keys, where the final value of each nested dictionary is the word itself
        def trie():
            root = dict()
            for word in words:
                D = root
                for letter in word[:-1]:
                        D = D.setdefault(letter, {})
                D[word[-1]] = word
            return(root)
        self.frequency = frequency()    
        self.trie = trie()
        self.counts = [ self.frequency[value] for value in self.frequency ]

    def ckSoln(self, soln):
        #helper function checks to see if a move is valid and returns False if it is not
        # - that is to say that said move is performed cardinally from the letter before it
        def contiguous(soln):
            if len(set(soln)) != len(soln):
                return(False)       #no coordinate is the same
            for j in range(len(soln)):
                if soln[j][0] not in range(self.size):
                    return(False)   #no x coordinate should be < 0 or >= self.size
                if soln[j][1] not in range(self.size):
                    return(False)   #no y coordinate should be < 0 or >= self.size
            for i in range(len(soln)-1):
                if abs(soln[i][0]-soln[i+1][0]) > 1:
                    return(False)   #no move should jump a space in the x-direction
                if abs(soln[i][1]-soln[i+1][1]) > 1:
                    return(False)   #no move should jump a space in the y-direction
                if soln[i] == soln[i+1]:
                    return(False)   #no move should be the same
                if abs(soln[i][0]-soln[i+1][0]) == 1 and abs(soln[i][1]-soln[i+1][1]) == 1:
                    return(False)   #no diagonal moves
        #checks to see if soln is a valid, contiguous input.
        if contiguous(soln) == False:
            return(False)
        #this checks to see if the letter from the first element is in the trie data structure.
        #If not, the function returns False. If so, the function goes onto the next letter, while
        #using the letter before, and loops through again until the value of self.trie is returned.
        else:
            v = self.trie
            for elem in soln:
                if self.board[elem[0]][elem[1]] in v:
                    v = v[self.board[elem[0]][elem[1]]]
                else:
                    return(False)
            return(v)

    def boardOverlay(self):     #clears up some code to create an overlay for the board
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill='white')
                self.canvas.create_text(i*20+10, j*20+10, text=self.board[j][i])

    def extend(self, event):
        col = event.x//20
        row = event.y//20
        self.solution.append((row, col))
        #uses ckSoln to check if a move is valid, while using the previous moves before it
        #by utilizing and constantly updating self.solution 
        if self.ckSoln(self.solution) == False:
            #creates red circle if a move is not valid, and updates self.solution accordingly
            self.solution = self.solution[:-1]
            self.canvas.create_oval(col*20, row*20, (col+1)*20, (row+1)*20, fill='red') 
            for i in range(self.size):
                for j in range(self.size):
                    self.canvas.create_text(i*20+10, j*20+10, text=self.board[j][i])    
        elif type(self.ckSoln(self.solution)) == str:
            self.canvas.create_oval(col*20, row*20, (col+1)*20, (row+1)*20, fill='green')
            #resets board and displays message if a word is found
            print("Word found: " + str(self.ckSoln(self.solution)))                             
            self.solution = []  #clears self.solution and maintains current board
            self.boardOverlay()
        else:
            #creates green circle if a move is valid
            self.canvas.create_oval(col*20, row*20, (col+1)*20, (row+1)*20, fill='green')
            for i in range(self.size):
                for j in range(self.size):
                    self.canvas.create_text(i*20+10, j*20+10, text=self.board[j][i])    

    def new(self, event):
        self.solution = []  #clears self.solution
        self.board = [ choices(list(self.frequency.keys()), weights=self.counts, k=self.size)
                       for i in range(self.size) ]  #replaces game with a new board
        self.boardOverlay()

    def reset(self, event):
        self.solution = []  #clears self.solution and maintains current board
        self.boardOverlay()

    def solve(self):
        solutions = []      #stores all solution in a list to be returned
        def helper(coordinates):
            if type(self.ckSoln(coordinates)) == str:
                #a word found is appended to the solutions list
                solutions.append(self.ckSoln(coordinates))
            if type(self.ckSoln(coordinates)) == dict:
                #if a move is valid, then it checks recursively the coordinates beside it
                helper(coordinates + [(coordinates[-1][0]-1, coordinates[-1][1])])  #down
                helper(coordinates + [(coordinates[-1][0], coordinates[-1][1]-1)])  #left
                helper(coordinates + [(coordinates[-1][0]+1, coordinates[-1][1])])  #up
                helper(coordinates + [(coordinates[-1][0], coordinates[-1][1]+1)])  #right
        for x in range(self.size):          #calls on helper functions for all coordinates on the grid
            for y in range(self.size):
                helper([(x, y)])
        return(solutions)                   #solutions are returned

if __name__ == "__main__":
    b = Boggle()
    b.window.mainloop()