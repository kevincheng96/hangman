"""hangman game that will teach users a new word each game (with definitions).
User can look at game history to check on words learned"""
import random, json
from tkinter import *

# load dictionary.json into a python dict
with open('dictionary.json') as file:
    dictionary = json.load(file)
dictKeys = list(dictionary.keys())

# GUI class
class MyGUI:

    # class variable to store history of words tested on (still need to work on how to display this)
    wordHistory = {}

    def __init__(self, master):
        frame = Frame(master)
        master.minsize(width=400, height=350)
        frame.pack()

        self.incorrectLetters = ''
        self.correctLetters = ''
        self.guessesLeft = 6
        self.word = self.getRandomWord()
        self.currentHangmanIndex = 0
        self.hangmanPictures = ['''
          +---+
          |   |
              |
              |
              |
              |
        =========''', '''
          +---+
          |   |
          O   |
              |
              |
              |
        =========''', '''
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========''', '''
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========''', '''
          +---+
          |   |
          O   |
         /|\  |
              |
              |
        =========''', '''
          +---+
          |   |
          O   |
         /|\  |
         /    |
              |
        =========''', '''
          +---+
          |   |
          O   |
         /|\  |
         / \  |
              |
        =========''']

        self.hangman = Label(frame, text=self.hangmanPictures[self.currentHangmanIndex])
        self.hangman.grid(row=0, columnspan=2)

        self.wordLabelVariable = StringVar()
        self.updateWordLabel()
        self.wordLabel = Label(frame, textvariable=self.wordLabelVariable, fg='black')
        self.wordLabel.grid(row=1, columnspan=2)

        self.correctLettersVariable = StringVar()
        self.correctLettersVariable.set('Correct guesses: ')
        self.correctLettersLabel = Label(frame, textvariable=self.correctLettersVariable)
        self.correctLettersLabel.grid(row=2, column=0, rowspan=3)

        self.incorrectLettersVariable = StringVar()
        self.incorrectLettersVariable.set('Incorrect guesses: ')
        self.incorrectLettersLabel = Label(frame, textvariable=self.incorrectLettersVariable)
        self.incorrectLettersLabel.grid(row=2, column=1, rowspan=3)

        self.guessLabelVariable = StringVar()
        self.guessLabelVariable.set('Please enter in your guess: ')
        self.guessLabel = Label(frame, textvariable=self.guessLabelVariable, fg='black')
        self.guessLabel.grid(row=5, columnspan=2)

        self.entryVariable = StringVar()
        self.guessEntry = Entry(frame, textvariable=self.entryVariable)
        self.entryVariable.set("")
        self.guessEntry.bind('<Return>', self.OnPressEnter)
        self.guessEntry.grid(row=6, columnspan=2)

        self.hintButton = Button(frame, text="Hint", command=self.getHint)
        self.hintButton.bind('')
        self.hintButton.grid(row=7, columnspan=2)

        self.definitionLabel = Label(frame, text='', wraplength=350, justify=LEFT)
        self.definitionLabel.grid(row=8, columnspan=3)

        self.gameEndLabel = Label(frame, text='', font=('Arial', 20))
        self.gameEndLabel.grid(row=9, columnspan=3)

    def getRandomWord(self):
        word = random.choice(dictKeys)
        if (' ' or "-") in word:
            word = random.choice(dictKeys)
        return word

    def updateWordLabel(self):
        newWordLabel = ''
        for i in self.word:
            if i in self.correctLetters:
                newWordLabel += i + ' '
            else:
                newWordLabel += '_ '
        self.wordLabelVariable.set(newWordLabel)

    def getHint(self):
        self.definitionLabel.config(text="Word definition: " + dictionary[self.word])

    def OnPressEnter(self, event):
        input = self.entryVariable.get()
        if input == 'yes': # reset game
            self.incorrectLetters = ''
            self.correctLetters = ''
            self.guessesLeft = 6
            self.word = self.getRandomWord()
            self.currentHangmanIndex = 0
            self.guessLabelVariable.set('Please enter in your guess: ')
            self.correctLettersVariable.set('Correct guesses: ')
            self.incorrectLettersVariable.set('Incorrect guesses: ')
            self.hangman.config(text=self.hangmanPictures[0])
            self.definitionLabel.config(text='')
            self.gameEndLabel.config(text='')
            self.updateWordLabel()
        else:
            input = self.processInput(input,self.incorrectLetters + self.correctLetters, self.guessLabelVariable)
            if input != 0:
                self.playGame(input)
                self.incorrectLettersVariable.set('Incorrect guesses: ' + self.incorrectLetters)
                self.correctLettersVariable.set('Correct guesses: ' + self.correctLetters)
                self.updateWordLabel()
        self.entryVariable.set('')
        if self.guessesLeft == 0:
            self.guessLabelVariable.set("Would you like to play again? (yes/no)")

    def processInput(self, guess, alreadyGuessed, label):
            guess = guess.upper()
            if len(guess) != 1:
                label.set('Please enter only one letter')
                return 0
            elif guess in alreadyGuessed:
                label.set('You have already guessed this letter')
                return 0
            elif guess not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                label.set('Please print an uppercase letter')
                return 0
            else:
                return guess

    def playGame(self, input):
        guess = str(input)
        guessedAllLetters = True
        if guess in self.word:
            self.guessLabelVariable.set("The letter " + guess + " was in the word!")
            self.correctLetters += guess
            for j in range(len(self.word)):
                if self.word[j] not in self.correctLetters:
                    guessedAllLetters = False
            if guessedAllLetters:
                self.guessLabelVariable.set("Congrats, you won! The word was " + self.word + ". Play again? (yes/no)")
        else:
            self.incorrectLetters += guess
            self.guessesLeft -= 1
            self.currentHangmanIndex += 1
            self.hangman.config(text=self.hangmanPictures[self.currentHangmanIndex])
            self.guessLabelVariable.set("Sorry, your guess was incorrect. You have " + str(self.guessesLeft) + " left.")
            if self.guessesLeft == 0:
                self.guessLabelVariable.set("Would you like to play again? (yes/no)")
                self.definitionLabel.config(text="Your word was " + self.word + ": " + dictionary[self.word])
                self.gameEndLabel.config(text='Gameover')
                MyGUI.wordHistory[self.word] = dictionary[self.word]

# calling the MyGUI class
root = Tk()
gui = MyGUI(root)
root.mainloop()

""" Also try to allow users to save their past words and look over them to review the definitions """
