# This program takes the raw list of words storedi n the words_alpha.txt file and
# assigns each of them weights then stores that info in the mapped_words.txt file

alpha_weights = { 'a':2, 'b':3, 'c':5, 'd':7, 'e':11, 'f':13, 'g':17, 'h':19, 'i':23,
                    'j':29, 'k':31, 'l':37, 'm':41, 'n':43, 'o':47, 'p':53, 'q':59, 'r':61,
                    's':67, 't':71, 'u':73, 'v':79, 'w':83, 'x':89, 'y':97, 'z':101 }

def getKey( word ):
    key = 1
    for letter in word:
        key = key * alpha_weights[letter]

    return key

if __name__ == "__main__":
    dictionary = open('words_alpha.txt','r')
    mapped = open('mapped_words.txt','w')
    
    for line in dictionary:
        if len(line.strip()) >= 3:
            key = getKey(line.strip())
            mapped.write(str(key) + " " + line.strip() + "\n")

    dictionary.close()
    mapped.close()
