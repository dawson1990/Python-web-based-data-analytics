import pymongo
import hashlib
import pprint
import string


def checkIfExists(text: str):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    text_digest = hashlib.sha256(bytes(text, encoding='utf-8')).hexdigest()
    if c.find({'docID': text_digest}).count() > 0:
        exists = True
        print('PRE CHECK: EXISTS')
    else:
        exists = False
        print('PRE CHECK: DOESNT EXIST')
    if exists:
        return text_digest
    else:
        return None


def find(text_digest):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']


def insert(result: dict, notFound, freq_count, text: str):
    text_digest = hashlib.sha256(bytes(text, encoding='utf-8')).hexdigest()
    # filename_digest = hashlib.sha256(bytes(filename, encoding='utf-8')).hexdigest()
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']
    if c.find({'docID': text_digest}).count() > 0:
        print('DOC EXISTS\nFETCHING')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': text_digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': text_digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': text_digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': text_digest}))
    else:
        print('INSERTING DOC')
        dbWordFreq = {'docID':text_digest,'elements': freq_count}
        dbFoundDict = {'docID': text_digest, 'elements': result}
        dbNotFoundDict = {'docID': text_digest, 'elements': notFound}
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
        pprint.pprint(c.find_one({'docID': text_digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': text_digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': text_digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': text_digest}))
    return text_digest


def adv_insert(result: dict, notFound: dict,freq_count, text: str, rank: list):
    text_digest = hashlib.sha256(bytes(text, encoding='utf-8')).hexdigest()
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']

    if c.find({'docID': text_digest}).count() > 0 and nf.find({'docID': text_digest}).count() > 0 and fq.find({'docID': text_digest}).count() > 0 and rk.find({'docID': text_digest}).count() > 0:
        print('DOC EXISTS\nFETCHING')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': text_digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': text_digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': text_digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': text_digest}))
    elif c.find({'docID': text_digest}).count() > 0 and nf.find({'docID': text_digest}).count() > 0 and fq.find({'docID': text_digest}).count() > 0 and not rk.find({'docID': text_digest}).count() > 0:
        print('INSERTING RANK DOC')
        dbRankDict = {'docID': text_digest, 'elements': rank}
        try:
            rk.insert(dbRankDict)
        except:
            print('an error occurred inserting rank dict')
        print('\nAssociations:\n')
        pprint.pprint(c.find_one({'docID': text_digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': text_digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': text_digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': text_digest}))
    else:
        print('INSERTING DOC')
        dbWordFreq = {'docID':text_digest,'elements': freq_count}
        dbRankDict = {'docID': text_digest, 'elements': rank}
        dbFoundDict = {'docID': text_digest, 'elements': result}
        dbNotFoundDict = {'docID': text_digest, 'elements': notFound}
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
        pprint.pprint(c.find_one({'docID': text_digest}))
        print('\nFrequency:\n')
        pprint.pprint(fq.find_one({'docID': text_digest}))
        print('\nWords not found:\n')
        pprint.pprint(nf.find_one({'docID': text_digest}))
        print('\nWords ordered by rank:(ADVANCED SEARCH):\n')
        pprint.pprint(rk.find_one({'docID': text_digest}))
    return text_digest