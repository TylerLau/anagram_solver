# Open the mapped_words.txt file
# Store all of the information in that file into a dictionary
# Prompt the user for a word input

from dict_map import getKey

hashmap = {}
alpha_weights = { 'a':2, 'b':3, 'c':5, 'd':7, 'e':11, 'f':13, 'g':17, 'h':19, 'i':23,
                    'j':29, 'k':31, 'l':37, 'm':41, 'n':43, 'o':47, 'p':53, 'q':59, 'r':61,
                    's':67, 't':71, 'u':73, 'v':79, 'w':83, 'x':89, 'y':97, 'z':101 } 

# Parses the mapped_words.txt file and stores data into a map
def initHash():
    mapped_words = open('mapped_words.txt','r')
    for line in mapped_words:
        key, value = (line.strip()).split(' ')
        if int(key) not in hashmap:
            hashmap[int(key)] = [ value ]
        else:
            hashmap[int(key)].append( value )
    mapped_words.close()

# Returns a trimmed version of hashmap that only contains the words that exist within string_key
def trimMap(string_key):
    newMap = {}
    for key, value in hashmap.items():
        if (string_key % key == 0):
            newMap[key] = value
    return newMap

# Returns the modified string_key without the specified word_key
def removeWord(string_key, word_key):
    return string_key/word_key

def solveHelper(dictionary, string_key, word_list = []):
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
                    temp_list = solveHelper(dictionary, string_key/key, word_list + [word])
                    if temp_list:
                        for s in temp_list:
                            solutions.append(s)
        if solutions:
            return solutions
        else:
            return []          

def solveAnagram(dictionary, string_key):
    solutions = []
    for key in dictionary.copy():
        for word in dictionary[key]:
            word_list = solveHelper(dictionary, string_key/key, [word])
            if word_list:
                for s in word_list:
                    solutions.append(s)
        dictionary.pop(key)
    return solutions


if __name__ == "__main__":
    initHash()
    while(1):
        word = raw_input("Enter string/letters to check or 1 to exit: ")
        if word == '1':
            break
        keyvalue = getKey(word)
        trimmed_map = trimMap(keyvalue)
        
        solutions = solveAnagram(trimmed_map, keyvalue)
        
        for s in solutions:
            print s
