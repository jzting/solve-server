from subprocess import Popen, PIPE
from time import time
import glob
from os.path import basename

from words import *

TESTS_FOLDER = './tests/hi/cropped/partial'
LETTERS = ['e', 'a', 'i', 'o', 'u', 'r', 'n', 'm', 'j', 'z', 'f', 't', 's', 'p', 'l', 'w', 'g', 'd', 'k', 'h', 'c', 'b', 'q', 'v', 'y', 'x']

def fast_match(letter_path, letter, filename):
    cmd = "./FastMatchTemplate -t hi/%s/%s.png -s %s -y 108 -q 94" % (letter_path, letter, filename)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    result = stdout.split('|')
    # print cmd
    # print result
    return result

def main():
    files = glob.glob('%s/*.jpg' % TESTS_FOLDER)
    files.extend(glob.glob('%s/*.jpeg' % TESTS_FOLDER))
    
    total_time = 0.0
    total_found_words = 0
    
    for filename in files:
        start = time()
        actual_word = basename(filename).split('.')[0]
        solved_words = []
        got_letters = []
        word_length = 0
        # print actual_word
        
        # find blanks
        blank_result = fast_match('blue', '_', filename)
        word_length = int(blank_result[0])
        
        # scan for blue letters
        count = 1
        for letter in LETTERS:
            blue_result = fast_match('blue', letter, filename)
            
            # add to word length if in blank row
            try:
                word_length += int(blue_result[1])
            except IndexError:
                pass
            
            # add found letters to list
            for i in range(0, int(blue_result[0])):
                got_letters.append(letter)
            
            if len(got_letters) == 12:
                # print '%i' % count
                break
            
            count += 1
        
        # if no blanks found, check for red letters
        if word_length == 0:
            for letter in LETTERS:
                red_result = fast_match('red', letter, filename)
                
                # add found letters to list
                for i in range(0, int(red_result[0])):
                    got_letters.append(letter)
                
                # add number of found letters to word length
                word_length += int(red_result[0])
                
                if len(got_letters) == 12:
                    break
            
            # if word length is still not found, bail
            if word_length == 0:
                print 'not found'
        
        print got_letters
        print word_length
        
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
                # pass
                # wrong_letters = got_letters[:]
                # for letter in actual_word:
                #     wrong_letters.remove(letter)
                # sorted(wrong_letters)
                # print ''.join(wrong_letters)
                print 'PASS: found %s in %0.2fs' % (actual_word, time()-start)
                total_time += time() - start                
                total_found_words += 1
            else:
                # pass
                print 'FAIL: %s' % actual_word
                        
        except KeyError:
            pass
            # print 'FAIL: %s (word too long at %i characters)' % (actual_word, word_length)                    
        # print '%s: %i' % (actual_word, len(solved_words))
        
    print 'found %i words in %0.2fs' % (total_found_words, total_time)
    print 'average time taken %0.2fs' % (total_time / total_found_words)
        
if __name__ == "__main__":
    main()
