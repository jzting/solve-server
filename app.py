from subprocess import Popen, PIPE
from uuid import uuid4
from time import time
import shutil
import hmac
import os
from functools import wraps

from flask import Flask, request, jsonify, abort
from werkzeug import secure_filename
from words import *

SHARED_SECRET = 'allyourdrawingsarebelongtous!'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
TIME_THRESHOLD = 90
LETTERS = ['e', 'a', 'i', 'o', 'u', 'r', 'n', 'm', 'j', 'z', 'f', 't', 's', 'p', 'l', 'w', 'g', 'd', 'k', 'h', 'c', 'b', 'q', 'v', 'y', 'x']

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def requires_auth(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            request_id = request.form['request_id']
            auth_code = request.form['auth_code']
            timestamp = request.form['timestamp']
            now = time()
            difference = now - float(timestamp)
            if now - float(timestamp) < -TIME_THRESHOLD or now - float(timestamp) > TIME_THRESHOLD:
                abort(410)
            obj = hmac.new(SHARED_SECRET, '%s:%s' % (request_id, timestamp))
            if obj.hexdigest() != auth_code:
                abort(401)
        except KeyError:
            abort(400)
        
        return f(*args, **kwargs)
    return inner

@app.route('/update')
def update():
    data = {
        'hi': {
          'quality': 0.1,
          'image_rect': [0, 105, 640, 554],
          'letters_rect': [0, 661, 640, 299]
        },
        'lo': {
          'quality': 0.5,
          'image_rect': [0, 53, 320, 277],
          'letters_rect': [0, 331, 320, 149]
        }
    }

    return jsonify(data=data)
    
@app.route('/', methods=['POST'])
@requires_auth
def index():
    
    file = request.files['file']
    version = request.form.get('version', 'hi')
    quality = 94
    
    if version == 'hi':
        y = 108
    else:
        y = 54
    
    if file and allowed_file(file.filename):
        start = time()
        got_letters = []
        solved_words = []
        word_length = 0
        
        # save with temp filename
        filename = '%s.jpg' % uuid4().hex
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        def fast_match(color, letter, filename):
            cmd = "./FastMatchTemplate -t %s/%s/%s.png -s uploads/%s -y %i -q %i" % (version, color, letter, filename, y, quality)
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            result = stdout.split('|')
            return result
        
        # find blanks
        blank_result = fast_match('blue', '_', filename)
        word_length = int(blank_result[0])
        
        # scan for blue letters
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
                break
        
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
                abort(500)
        
        print got_letters
        print word_length
        
        # solve the word
        for word in WORDS[word_length]:
            letters = got_letters[:]
            solved_word = []
            
            for char in word:
                if char in letters:
                    letters.remove(char)
                    solved_word.append(char)
            
            if len(solved_word) == len(word):
                solved_words.append(word)
        
        if len(solved_words) == 1:
            current_file = 'uploads/%s' % filename
            solved_word_path = 'uploads/%s' % solved_words[0]
            if not os.path.exists(solved_word_path):
                os.makedirs(solved_word_path)
            
            shutil.move(current_file, solved_word_path)
        
        return jsonify(results=solved_words, started=start, time_taken=time()-start)
    else:
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)