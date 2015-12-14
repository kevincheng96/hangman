"""hangman game that will teach users a new word each game (with definitions).
User can look at game history to check on words learned"""
import random, json, tkinter

def getRandomWord(list):
    index = random.randint(0, len(list) - 1)
    return list[index]

def getGuess(alreadyGuessed):
    print('Please enter in your guess:')
    guess = input()
    guess = guess.lower()
    if len(guess) != 1:
        print('Please enter a single letter')
    elif guess in alreadyGuessed:
        print('You have already guessed this letter')
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        print('Please print a letter')
    else:
        alreadyGuessed + guess
        return guess
    getGuess(alreadyGuessed)  #calls again if no value is returned

def playGame(numGuesses, incorrectList, correctList, wordList):
    word = getRandomWord(wordList)
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
            if guessesLeft == 0:
                print("Gameover :D")
                break
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

incorrectLetters = ''
correctLetters = ''
wordList = ["hello", "chubby", "fats"]
guessesLeft = 5

#start game

""" top = tkinter.Tk()
top.mainloop() """

playGame(guessesLeft, incorrectLetters, correctLetters, wordList)





dictionary = {}

with open('dictionary.json') as file:
    dictionary = json.load(file)
    """for line in file:
        dictionary.append(json.loads(line))"""
dictKeys = dictionary.keys()
print(dictKeys)