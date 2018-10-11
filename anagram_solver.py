# Open the mapped_words.txt file
# Store all of the information in that file into a dictionary
# Prompt the user for a word input

from dict_map import getKey

hashmap = {}
alpha_weights = { 'a':2, 'b':3, 'c':5, 'd':7, 'e':11, 'f':13, 'g':17, 'h':19, 'i':23,
                    'j':29, 'k':31, 'l':37, 'm':41, 'n':43, 'o':47, 'p':53, 'q':59, 'r':61,
                    's':67, 't':71, 'u':73, 'v':79, 'w':83, 'x':89, 'y':97, 'z':101 } 

def initHash():
    mapped_words = open('mapped_words.txt','r')
    for line in mapped_words:
        key, value = (line.strip()).split(' ')
        if int(key) not in hashmap:
            hashmap[int(key)] = [ value ]
        else:
            hashmap[int(key)].append( value )
    mapped_words.close()

if __name__ == "__main__":
    initHash()
    while(1):
        word = raw_input("Enter string/letters to check or 1 to exit: ")
        if word == '1':
            break
        keyvalue = getKey(word)
        if int(keyvalue) in hashmap:
            if hashmap[int(keyvalue)][0] != word:
                print hashmap[int(keyvalue)]
            else:
                print "No results"
        else:
            print "No results"

