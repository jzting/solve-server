from multiprocessing import Process, Queue
from Queue import Empty
from subprocess import Popen, PIPE
from time import time
import glob
from os.path import basename

from words import *

TESTS_FOLDER = './tests'
# LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
LETTERS = ['e', 'a', 'r', 'n', 'i', 'o', 'm', 'j', 'z', 'f', 't', 's', 'p', 'l', 'w', 'g', 'd', 'k', 'h', 'u', 'c', 'b', 'q', 'v', 'y', 'x']

def fast_match(q, letter_path, letter, filename):
     cmd = "./FastMatchTemplate -t %s/%s.png -s %s" % (letter_path, letter, filename)
     p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
     stdout, stderr = p.communicate()
     result = stdout.split('|')
     word_length = 0
     
     try:
         word_length = int(result[1])
     except IndexError:
         pass
     
     # add found letters to list
     for i in range(0, int(result[0])):
         q.put(letter)
         if letter_path is 'letters-red':
            word_length += 1
     
     q.put(word_length)

def main():
    files = glob.glob('%s/*.jpg' % TESTS_FOLDER)
    files.extend(glob.glob('%s/*.jpeg' % TESTS_FOLDER))
        
    for filename in files:
        actual_word = basename(filename).split('.')[0]
        # print actual_word
        
        q = Queue()
        start = time()
        solved_words = []
        got_letters = []
        word_length = 0
    
        # find blanks
        p1 = Process(target=fast_match, args=(q, 'letters', '_', filename))
        p1.start()
    
        # scan for letters
        for letter in LETTERS:
            p2 = Process(target=fast_match, args=(q, 'letters', letter, filename))
            p2.start()
            
            p3 = Process(target=fast_match, args=(q, 'letters-red', letter, filename))
            p3.start()            
    
        # gather results
        while True:
            try:
                item = q.get(timeout=1)
                if type(item) is str:
                    got_letters.append(item)
                else:
                    word_length += item
            except Empty:
                break
    
        if word_length == 0:
            print 'not found'
            
        # print got_letters
        # print word_length
        
        # solve the word
        try:
            for word in WORDS[word_length]:
                letters = got_letters[:]
                solved_word = []
        
                for char in word:
                    if char in letters:
                        letters.remove(char)
                        solved_word.append(char)
        
                if len(solved_word) == len(word):
                    solved_words.append(word)
        
            if actual_word in solved_words:
                print 'PASS: found %s in %0.2fs' % (actual_word, time()-start)                
            else:
                print 'FAIL: %s' % actual_word
        except KeyError:
            print 'FAIL: %s (word too long at %i characters)' % (actual_word, word_length)
            
if __name__ == "__main__":
    main()