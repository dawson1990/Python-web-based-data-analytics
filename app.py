from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import basic_analysis
import adv_analysis
import os
import pymongo
import data_utils
import nltk
import string
import json
import mongo

UPLOAD_FOLDER = 'C:/Users/Kevin/Google Drive/college/Year4/Web Dev/data analysis assignment/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def home():
    return render_template('page1.html',  header='Data Analytics')


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    assoc={}
    freq={}
    notfound={}
    text = ''
    tokens =[]
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    fq = db['word_freq']
    rk = db['ranked']
    if request.method == 'POST':
        file = request.files['file']
        checked = request.form.getlist('advanced')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fname = os.path.join('C:/Users/Kevin/Google Drive/college/Year4/Web Dev/data analysis assignment/uploads',
                                 file.filename)
            with open('ea-thesaurus-lower.json') as normsf:
                norms = json.load(normsf)
            with open(fname, 'r', encoding="mac_roman") as s:
                for line in s.readlines():
                    # using both nltk to tokenize word and using string to translate punctuation into a space
                    tokens += nltk.word_tokenize(
                                    line.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))))
                    text += line.lower().translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                text_digest = mongo.checkIfExists(text)
                digest = text_digest['key']
                basic = text_digest['basic']
                adv = text_digest['adv']
                if basic is True and adv is True:
                    return mongo.findAndDisplay(digest, file.filename)
                elif basic is True and adv is False or basic is False and adv is False:
                    if checked:
                        options = request.form['options']
                        adv_analysis.advanced(options,norms,tokens, digest)
                        associations = c.find_one({'docID': digest})
                        assoc = data_utils.processAssoc(associations)
                        wordFreq = fq.find_one({'docID': digest})
                        freq = data_utils.processFreq(wordFreq)
                        nf = nf.find_one({'docID': digest})
                        notfound = data_utils.processNotFound(nf)
                        r = rk.find_one({'docID': digest})
                        rank = r.get('elements',{})
                        combinedDict = data_utils.combine(assoc, freq, rank)
                        return render_template('adv_upload.html',heading='Result', combined=combinedDict.values(),
                                               ranks=rank, freq=freq,
                                               filename=filename,
                                               notfound=notfound)
                    else:
                        if basic is True:
                            return mongo.findAndDisplay(digest, file.filename)
                        else:
                            basic_analysis.basic(norms, tokens, digest)
                            associations = c.find_one({'docID': digest})
                            assoc = data_utils.processAssoc(associations)
                            wordFreq = fq.find_one({'docID': digest})
                            freq = data_utils.processFreq(wordFreq)
                            sortedFreq = data_utils.sortFreq(freq)
                            nf = nf.find_one({'docID': digest})
                            notfound = data_utils.processNotFound(nf)
                            r = rk.find_one({'docID': digest})
                            if r is None:
                                return render_template('upload.html', heading='Result', filename=filename,
                                                       associations=assoc, freq=sortedFreq,
                                                       notfound=notfound)
                            else:
                                rank = data_utils.processRank(r)
                                combinedDict = data_utils.combine(assoc, freq, rank)
                                return render_template('adv_upload.html', heading='Result',
                                                       combined=combinedDict.values(), ranks=rank, freq=freq,
                                                       filename=filename,
                                                       notfound=notfound)
        else:
            return render_template('upload.html', filename='did not work, make sure file is a text file')


if __name__ == '__main__':
    app.run(debug=True)
