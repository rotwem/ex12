# Ex.12: Boggle

## Table of contents
* [About] (#About)
* [Prerequisites] (#Prerequisites)
* [Dependencies] (#Dependencies)
* [Special Features] (#Special Features)
* [Authors] (#Authors)

## About
This programme is for the game "Boggle", the rules of the original game are:
Each round, the user have 3 minutes to find as many valid words as they can in a 4X4 board of random letters.
A valid word is a word that's constructed from the letters of sequentially adjacent board coordinates,
meaning, those horizontally, vertically, and diagonally neighboring.
Each word must be at least three letters long and can't contain the same coordinate more than once.

## Prerequisites
* "boggle_board_randomizer.py": contains a function for creating a 4X4 board of randomize letters
* "boggle_dict.txt": valid words that can be found on boards

## Dependencies
* tkinter
* time

## Special Features
* Step recommender:
Every step the user takes, the next possible steps are colored in a different color to help the user choose a valid word
* Start over:
The user may choose to randomize a new board at any given time

## Authors
* polinski
* rotwem
