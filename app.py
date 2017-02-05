from flask import Flask, render_template, request, session, flash, redirect
from werkzeug.utils import secure_filename
import basic_analysis
import adv_analysis
import os
import pymongo
import collections
import operator
import pprint

UPLOAD_FOLDER = 'C:/Users/Kevin/Google Drive/college/Year4/Web Dev/data analysis assignment/uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'


@app.route('/')
@app.route('/home')
def home():
        return render_template('page1.html',  header='Data Analytics')


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    assoc={}
    freq={}
    notfound={}
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    fq = db['word_freq']
    rk = db['ranked']
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/home')
        file = request.files['file']
        checked = request.form.getlist('advanced')
        print('checked', checked, type(checked))
        if file:
            print('file entered')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if checked:
                print('checked')
                options = request.form['options']
                text_digest = adv_analysis.advanced(file,options)
                associations = c.find_one({'docID': text_digest})
                assoc = processAssoc(associations)
                wordFreq = fq.find_one({'docID': text_digest})
                freq = processFreq(wordFreq)
                nf = nf.find_one({'docID': text_digest})
                notfound = processNotFound(nf)
                r = rk.find_one({'docID': text_digest})
                rank = r.get('elements',{}) #processRank(r)
                combinedDict = combine(assoc, freq, notfound, rank)
                return render_template('adv_upload.html', combined=combinedDict.values(), ranks=rank, freq=freq,
                                       filename=filename,
                                       notfound=notfound)
                # return render_template('adv_upload.html', filename=filename, associations=assoc, freq=freq,
                #                        notfound=notfound, ranks=rank)
            else:
                text_digest = basic_analysis.basic(file)
                associations = c.find_one({'docID': text_digest})
                assoc = processAssoc(associations)
                wordFreq = fq.find_one({'docID': text_digest})
                freq = processFreq(wordFreq)
                nf = nf.find_one({'docID': text_digest})
                notfound = processNotFound(nf)
                r = rk.find_one({'docID': text_digest})
                if r is None:
                    return render_template('upload.html', filename=filename, associations=assoc, freq=freq,
                                           notfound=notfound)
                else:
                    rank = processRank(r)
                    combinedDict = combine(assoc, freq, notfound, rank)
                    return render_template('adv_upload.html', combined=combinedDict.values(), ranks=rank, freq=freq, filename=filename,
                                           notfound=notfound)
                    # return render_template('adv_upload.html', combined=combinedDict, filename=filename, associations=assoc, freq=freq,
                    #                        notfound=notfound, ranks=rank)
        else:
            return render_template('upload.html', filename='did not work')



def processRank(rank):
    ranks = {}
    final = {}
    r = {}
    oDict = collections.OrderedDict()
    temp = rank
    ranks = temp.get('elements',{})
    for element in ranks:
        oDict[element[0]] = element[1]
    for k,v in oDict.items():
        r[v] = k
    final = sorted(r.items(), reverse = True)
    return final

def processNotFound(nf:dict):
    return nf.get('elements', {})


def processAssoc(associations:dict):
    temp = {}
    temp = associations.get('elements',{})
    return temp

def processFreq(wordFreq:dict):
    return wordFreq.get('elements',{})


def combine(assoc:dict , freq:dict, notfound:dict, rank:list):
    temp = {}
    for key, value in assoc.items():
        for k,v in freq.items():
            if key == k:
                for element in rank:
                    if element[0] == key:
                        temp[key] = {'word': key,'associations': value, 'frequency': v, 'rank': element[1]}
                # for elem in element:
                    #     if elem == key and key == k:
                    #      temp[key] = {'rank': elem, 'word' : key, 'associations': value, 'frequency': v}
                     # temp[key] = {'word': key,'associations': value, 'frequency': v, 'rank': element[0]}
    print('COMBINED\n', 'length', len(temp), '\n')
    pprint.pprint(temp)
    return temp



if __name__ == '__main__':
    app.run(debug=True)
