import re

def welcome(): #main welcome screen
    print("----------------------------------------------------------------------------")
    print("                           Welcome to WordleSolver")
    print("----------------------------------------------------------------------------")
    print("How to use:")
    print("    Type your guess in the following way (each guess must be 5 letters long)")
    print("      - (UPPERCASE) if letter is in the RIGHT position   (example: A)")
    print("      - (lowercase) if letter is in  a  WRONG position   (example: a)")
    print("      - (.letter)   if letter is NOT PRESENT in the word (example: .a)\n")

def readWords(): #read all words in words.txt
    with open("words.txt", "r") as inp: return inp.read().split("\n")

def removechars(s, remove): #remove characters in (string remove) from (string s)
    return ''.join([ char         if char not in remove else ''  for char in s])

def getpos(s, remove, guess): #return a string long 5 with letters in right position (example: f___y_ul)
    return ''.join([ char.lower() if char in     s      else '_' for char in removechars(guess, remove)])

def validate(guess): #decode the input given returning right/wrong position letters and the ones not in word
    notPrese = ''.join([ char[1:] for char in re.findall(r'[.]+\w', guess) ])
    wrongPos = removechars( re.sub('[^a-z]', '', guess), notPrese )
    rightPos = getpos     ( re.sub('[^A-Z]', '', guess), notPrese, guess)

    notPrese = ''.join([ a for a in notPrese if all( (a != b) for b in rightPos) ]) #remove duplicates from notPrese that are also present in rightPos

    return (rightPos, wrongPos, notPrese)

def isrightpos(words, right): #remove words that don't have certain characters in right position
    return [word for word in words if all( (a == b) or (b == "_")  for a, b in zip(word, right) )]

def iswrongpos(words, wrong): #remove words that don't have certain characters
    return [word for word in words if all( char in word  for char in wrong)]

def isnotprese(words, notPrese): # remove words that have characters that aren't present
    return [word for word in words if all( (a != b)  for a in word for b in notPrese )]

def update(words, guessdata): #update words list with guess input
    words = isnotprese(words, guessdata[2]) 
    words = iswrongpos(words, guessdata[1]) 
    words = isrightpos(words, guessdata[0]) 

    return words

def main():
    words = readWords()
    welcome()   

    while True:
        guess = input("\nguess: ")
        words = update(words, validate(guess))

        print("\nPossible Words:", words)

if __name__ == '__main__':
    main()
