import pymongo
import hashlib


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


def insert(result: dict, notFound, freq_count, digest):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    fq = db['word_freq']
    dbWordFreq = {'docID':digest,'elements': freq_count}
    dbFoundDict = {'docID': digest, 'elements': result}
    dbNotFoundDict = {'docID': digest, 'elements': notFound}
    try:
        c.insert(dbFoundDict)
    except Exception as e:
        print('error inserting result',e )
    try:
        nf.insert(dbNotFoundDict)
    except Exception as e:

        print('error inserting not found',e)
    try:
        fq.insert(dbWordFreq)
    except Exception as e:
        print('error inserting freq', e)
    return digest


def adv_insert(result: dict, notFound: dict,freq_count, digest):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    c = db['result']
    nf = db['notfound']
    rk = db['ranked']
    fq = db['word_freq']
    dbWordFreq = {'docID':digest,'elements': freq_count}
    dbFoundDict = {'docID': digest, 'elements': result}
    dbNotFoundDict = {'docID': digest, 'elements': notFound}
    try:
        c.insert(dbFoundDict)
    except Exception as e:
        print('an error occurred inserting found dict',e)
    try:
        nf.insert(dbNotFoundDict)
    except Exception as e:
        print('an error occurred inserting not found dict',e)
    try:
        fq.insert(dbWordFreq)
    except Exception as e:
        print('an error occurred inserting freq dict', e)
    return digest


def updateRank(digest, orderedRank: list):
    client = pymongo.MongoClient()
    db = client['dataAnalyticsDB']
    rk = db['ranked']
    dbRankDict = {'docID': digest, 'elements': orderedRank}
    rk.delete_one({'docID': digest})
    try:
        rk.insert(dbRankDict)
    except Exception as e:
        print('an error inserting ranks occurred', e)
