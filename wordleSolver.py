import re

# Main welcome screen
def welcome():
    print("----------------------------------------------------------------------------")
    print("                           Welcome to WordleSolver")
    print("----------------------------------------------------------------------------")
    print("How to use:")
    print("    Type your guess in the following way (each guess must be 5 letters long)")
    print("      - (UPPERCASE) if letter is in the RIGHT position   (example: A)")
    print("      - (lowercase) if letter is in  a  WRONG position   (example: a)")
    print("      - (.letter)   if letter is NOT PRESENT in the word (example: .a)\n")

# Reads all words in words.txt
def readWords():
    with open("words.txt", "r") as inp: return inp.read().split("\n")

# Removes characters in (string remove) from (string s)
def removeChars(s, remove):
    return ''.join([ char         if char not in remove else ''  for char in s ])

# Returns a string long 5 with letters in right position (example: f___y_u)
def getPos(s, remove, guess):
    return ''.join([ char.lower() if char     in s      else '_' for char in removeChars(guess, remove) ])

# Decodes the input given returning right/wrong position letters and the ones not in word
def validate(guess):
    notPrese = ''.join([ char[1:] for char in re.findall(r'[.]+\w', guess) ])
    wrongPos = getPos( removeChars( re.sub('[^a-z]', '', guess), notPrese ), notPrese, guess )
    rightPos = getPos(              re.sub('[^A-Z]', '', guess),             notPrese, guess )

    # Removes duplicates from notPrese that are also present in rightPos
    notPrese = ''.join([ a for a in notPrese if all( (a != b) for b in rightPos) ])
    return (rightPos, wrongPos, notPrese)

# Removes words that don't have certain characters in right position
def isrightpos(words, right):
    return [word for word in words if all( (a == b)    or (b == "_") for a, b in zip(word, right) )]

# Removes words that don't have certain characters AND removes words that have certain characters in the wrong posions
def iswrongpos(words, wrong): 
    return [word for word in words if all( (c in word) or (c == "_") for c in wrong ) and all( (a != b) or (b =="_" ) for a,b in zip(word, wrong)) ]

# Removes words that have characters that aren't present
def isnotprese(words, notPrese):
    return [word for word in words if all( (a != b)  for a in word for b in notPrese )]

# Update words list with guess input
def update(words, guessdata):
    words = isnotprese(words, guessdata[2]) 
    words = iswrongpos(words, guessdata[1]) 
    words = isrightpos(words, guessdata[0]) 
    return words

# Main program loop
def main():
    welcome()
    words = readWords()
    while True:
        guess = input("\nguess: ")
        words = update(words, validate(guess))
        print("\nPossible Words:", words)

if __name__ == '__main__':
    main()
