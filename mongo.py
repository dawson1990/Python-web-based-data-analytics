import pymongo
import hashlib
import pprint
from flask import render_template
import data_utils



def checkIfExists(text: str):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    a = db['ranked']
    basic = False
    adv = False
    digest = hashlib.sha256(bytes(text, encoding='utf-8')).hexdigest()
    if c.find({'docID': digest}).count() > 0 and a.find({'docID': digest}).count() > 0:
        basic = True
        adv = True
        return {'key': digest, 'basic': basic, 'adv': adv}
    elif c.find({'docID': digest}).count() > 0 and  not a.find({'docID': digest}).count() > 0:
        basic = True
        adv = False
        return {'key': digest, 'basic': basic, 'adv': adv}
    else:
        return {'key': digest, 'basic': basic, 'adv': adv}


def findAndDisplay(digest,fname):
    assoc= {}
    freq = {}
    nf = {}
    r = {}
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']
    associations = c.find_one({'docID': digest})
    assoc = data_utils.processAssoc(associations)
    wordFreq = fq.find_one({'docID': digest})
    freq = data_utils.processFreq(wordFreq)
    sortedFreq = data_utils.sortFreq(freq)
    nf = nf.find_one({'docID': digest})
    notfound = data_utils.processNotFound(nf)
    r = rk.find_one({'docID': digest})
    if r is None:
        return render_template('upload.html', heading='Previous Result', filename=fname, associations=assoc,
                               freq=sortedFreq,
                               notfound=notfound)
    else:
        print('has r')
        rank = r.get('elements', {})
        combinedDict = data_utils.combine(assoc, freq, rank)
        return render_template('adv_upload.html', heading='Previous Result', combined=combinedDict.values(), ranks=rank,
                               freq=freq,
                               filename=fname,
                               notfound=notfound)


def insert(result: dict, notFound, freq_count, digest):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']
    if c.find({'docID': digest}).count() > 0:
        print('DOC EXISTS\nFETCHING')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': digest}))
    else:
        print('INSERTING DOC')
        dbWordFreq = {'docID':digest,'elements': freq_count}
        dbFoundDict = {'docID': digest, 'elements': result}
        dbNotFoundDict = {'docID': digest, 'elements': notFound}
        try:
            c.insert(dbFoundDict)
        except:
            print('error inserting result',dbFoundDict )
        try:
            nf.insert(dbNotFoundDict)
        except:

            print('error inserting not found')
        try:
            fq.insert(dbWordFreq)
        except:
            print('error inserting freq')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': digest}))
    return digest


def adv_insert(result: dict, notFound: dict,freq_count, digest, rank: list):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']

    if c.find({'docID': digest}).count() > 0 and nf.find({'docID': digest}).count() > 0 and fq.find({'docID': digest}).count() > 0 and rk.find({'docID': digest}).count() > 0:
        print('DOC EXISTS\nFETCHING')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': digest}))
    elif c.find({'docID': digest}).count() > 0 and nf.find({'docID': digest}).count() > 0 and fq.find({'docID': digest}).count() > 0 and not rk.find({'docID': digest}).count() > 0:
        print('INSERTING RANK DOC')
        dbRankDict = {'docID': digest, 'elements': rank}
        try:
            rk.insert(dbRankDict)
        except:
            print('an error occurred inserting rank dict')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': digest}))
    else:
        print('INSERTING DOC')
        dbWordFreq = {'docID':digest,'elements': freq_count}
        dbRankDict = {'docID': digest, 'elements': rank}
        dbFoundDict = {'docID': digest, 'elements': result}
        dbNotFoundDict = {'docID': digest, 'elements': notFound}
        try:
            c.insert(dbFoundDict)
        except:
            print('an error occurred inserting found dict')
        try:
            nf.insert(dbNotFoundDict)
        except:
            print('an error occurred inserting not found dict')
        try:
            rk.insert(dbRankDict)
        except:
            print('an error occurred inserting rank dict')
        try:
            fq.insert(dbWordFreq)
        except:
            print('an error occurred inserting freq dict')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': digest}))
    return digest