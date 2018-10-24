# Open the mapped_words.txt file
# Store all of the information in that file into a dictionary
# Prompt the user for a word input

from dict_map import getKey

hashmap = {}
alpha_weights = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19, 'i': 23,
                 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53, 'q': 59, 'r': 61,
                 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89, 'y': 97, 'z': 101}


# Parses the mapped_words.txt file and stores data into a map
def initHash():
    dictionary = {}
    mapped_words = open('mapped_words.txt', 'r')
    for line in mapped_words:
        key, value = (line.strip()).split(' ')
        if int(key) not in dictionary:
            dictionary[int(key)] = [value]
        else:
            dictionary[int(key)].append(value)
    mapped_words.close()
    return dictionary

# Returns a trimmed word list of words within specified length values
def trimHelper(word_list, minLength=-1, maxLength=-1):
    trimmed_list = []
    for word in word_list:
        if (minLength == -1 or len(word) >= minLength) and (maxLength == -1 or len(word) <= maxLength):
            trimmed_list.append(word)
    return trimmed_list


# Returns a trimmed version of hashmap that only contains the words that exist within string_key
def trimDictionary(dictionary, string_key, minLength=-1, maxLength=-1):
    newMap = {}
    if minLength == -1 and maxLength == -1:
        for key, value in dictionary.items():
            if (string_key % key == 0):
                newMap[key] = value
    else:
        for key, value in dictionary.items():
            if (string_key % key == 0):
                newMap[key] = trimHelper(value, minLength, maxLength)
    return newMap


# Checks if string_key contains all of the required words and returns the modified key if it does, -1 if not
def checkWords(string_key, reqWords):
    for word in reqWords:
        temp = getKey(word)
        if string_key % temp == 0:
            string_key = string_key / temp
        else:
            return -1
    return string_key


# Recursive helper function that returns a list of valid solutions
def solveHelper(dictionary, string_key, word_list=[]):
    solutions = []
    if string_key == 1:
        solutions.append(word_list)
        return solutions
    elif string_key < 1:
        return solutions
    else:
        for key, value in dictionary.items():
            if (string_key % key == 0):
                for word in value:
                    temp_list = solveHelper(dictionary, string_key / key, word_list + [word])
                    if temp_list:
                        for s in temp_list:
                            solutions.append(s)
        if solutions:
            return solutions
        else:
            return []

# Function that sets up recursion done by solveHelper function
def solveAnagram(dictionary, string_key, reqWords):
    solutions = []
    for key in dictionary.copy():
        for word in dictionary[key]:
            word_list = solveHelper(dictionary, string_key / key, reqWords + [word])
            if word_list:
                for s in word_list:
                    solutions.append(s)
        dictionary.pop(key)
    return solutions

# Function that returns a list of assembled strings from a list of a list of words
def StringMaker(word_list):
    result = ['']
    for item in word_list:
        if isinstance(item, list):
            temp = []
            for word in item:
                temp += [s + ' ' + word for s in result]
            result = temp
        else:
            result = [s + ' ' + item for s in result]
    return result

if __name__ == "__main__":
    hashmap = initHash()
    while (1):
        reqWords = []
        minLength = -1
        maxLength = -1

        # Get string input from user or prompt to exit
        word = input("Enter string/letters to check or 1 to exit: ")
        if word == '1':
            break
        keyvalue = getKey(word)

        # Ask user if they want their solutions to include specific words
        f_reqWords = input("Require specific words? (y or n): ")
        if f_reqWords == 'y':
            raw_reqWords = input("Input required words separated by commas: ")
            reqWords = raw_reqWords.split(',')
            keyvalue = checkWords(keyvalue, reqWords)
            if keyvalue == -1:
                print("String does not contain all of the required words")
                break

        # Ask user if they want word length constraints
        f_length = input("Limit answer words to specific lengths? (y or n): ")
        if f_length == 'y':
            minLength = int(input("Minimum length (-1 if none): "))
            maxLength = int(input("Maximum length (-1 if none): "))

        # Get key value, trim dictionary accordingly, and create list of solutions
        trimmed_map = trimDictionary(hashmap, keyvalue, minLength, maxLength)
        solutions = solveAnagram(trimmed_map, keyvalue, reqWords)

        # Print out solutions
        if solutions:
            for s in solutions:
                print(s)
        else:
            print("No solutions")
