from flask import Flask, render_template, request, session, flash, redirect
from werkzeug.utils import secure_filename
import basic_analysis
import adv_analysis
import os
import pymongo
import data_utils

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
                assoc = data_utils.processAssoc(associations)
                wordFreq = fq.find_one({'docID': text_digest})
                freq = data_utils.processFreq(wordFreq)
                nf = nf.find_one({'docID': text_digest})
                notfound = data_utils.processNotFound(nf)
                r = rk.find_one({'docID': text_digest})
                rank = r.get('elements',{})
                combinedDict = data_utils.combine(assoc, freq, rank)
                return render_template('adv_upload.html', combined=combinedDict.values(), ranks=rank, freq=freq,
                                       filename=filename,
                                       notfound=notfound)
            else:
                text_digest = basic_analysis.basic(file)
                associations = c.find_one({'docID': text_digest})
                assoc = data_utils.processAssoc(associations)
                wordFreq = fq.find_one({'docID': text_digest})
                freq = data_utils.processFreq(wordFreq)
                nf = nf.find_one({'docID': text_digest})
                notfound = data_utils.processNotFound(nf)
                r = rk.find_one({'docID': text_digest})
                if r is None:
                    return render_template('upload.html', filename=filename, associations=assoc, freq=freq,
                                           notfound=notfound)
                else:
                    rank = data_utils.processRank(r)
                    combinedDict = data_utils.combine(assoc, freq, rank)
                    return render_template('adv_upload.html', combined=combinedDict.values(), ranks=rank, freq=freq, filename=filename,
                                           notfound=notfound)
        else:
            return render_template('upload.html', filename='did not work')







if __name__ == '__main__':
    app.run(debug=True)
