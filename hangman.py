"""hangman game that will teach users a new word each game (with definitions).
User can look at game history to check on words learned"""
import random, json, tkinter

# variables
incorrectLetters = ''
correctLetters = ''
wordList = ["hello", "chubby", "fats"]
guessesLeft = 5

# load dictionary.json into a python dict
with open('dictionary.json') as file:
    dictionary = json.load(file)
dictKeys = list(dictionary.keys())

# functions
def getGuess(alreadyGuessed):
    print('Please enter in your guess:')
    guess = input()
    guess = guess.upper()
    if len(guess) != 1:
        print('Please enter a single letter')
    elif guess in alreadyGuessed:
        print('You have already guessed this letter')
    elif guess not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        print('Please print an uppercase letter')
    else:
        alreadyGuessed + guess
        return guess
    getGuess(alreadyGuessed)  #calls again if no value is returned

# still need to present the right and wrong letters  guessed while playing the game
def playGame(numGuesses, incorrectList, correctList, wordList):
    word = random.choice(wordList)
    while numGuesses > 0:
        guess = str(getGuess(incorrectList + correctList))
        guessedAllLetters = True
        if guess in word:
            print("The letter " + guess + " was in the word!")
            correctList += guess
            for j in range(len(word)):
                if word[j] not in correctList:
                    guessedAllLetters = False
                    break
            if guessedAllLetters:
                print("Congrats, you won! The word was " + word)
                break
        else:
            incorrectList += guess
            numGuesses -= 1
            print("Sorry, your guess was incorrect. You have " + str(numGuesses) + " left.")
            if numGuesses == 0:
                print("Gameover :D. Your word was " + word)
                break
    print("Definition: " + word + ": " + dictionary[word])
    if playAgain():
        incorrectList = ''
        correctList = ''
        numGuesses = 5
        playGame(numGuesses, incorrectList, correctList, wordList) #recursion to play game again


def playAgain():
    print('Would you like to play again? (y/n)')
    playAgain = input()
    if playAgain == 'y':
        return True
    else:
        return False

# start game

"""  try to use tkinter for GUI
top = tkinter.Tk()
top.mainloop() """

playGame(guessesLeft, incorrectLetters, correctLetters, dictKeys)

""" Also try to allow users to save their past words and look over them to review the definitions """
