import csv
import requests
from StringIO import StringIO

r = requests.get('http://static.iminlikewithyou.com/drawsomething/wordlist.csv')

words = StringIO(r.content)
word_reader = csv.reader(words, delimiter=',')
WORDS = {}

for row in word_reader:
    try:
        WORDS[len(row[0])].append(row[0])
    except KeyError:
        WORDS[len(row[0])] = []
        WORDS[len(row[0])].append(row[0])
    
words_file = open('words.py', 'w')
words_file.write('WORDS = %s' % WORDS)
words_file.close()