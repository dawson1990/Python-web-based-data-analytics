import collections
import string


def sortFreq(freq):
    tupleList = [(k, v) for k, v in freq.items()]
    sortedRank = sorted(tupleList, key=lambda x: x[1], reverse=True)
    return sortedRank


def processRank(rank):
    ranks = {}
    final = {}
    r = {}
    oDict = collections.OrderedDict()
    temp = rank
    ranks = temp.get('elements',{})
    for element in ranks:
        oDict[element[0]] = element[1]
    for k, v in oDict.items():
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
    return wordFreq.get('elements', {})


def combine(assoc: dict, freq: dict, rank: list):
    temp = {}
    for key, value in assoc.items():
        for k, v in freq.items():
            if key == k:
                for element in rank:
                    if element[0] == key:
                        temp[key] = {'word': key, 'associations': value, 'frequency': v, 'rank': element[1]}
    return temp


# goes through keys in associations and replaces punctuation with a space
def cleanValues(value: list):
    for element in value:
        temp = {}
        temp = element
        for k in temp.keys():
            newKey = k.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            element[newKey] = element.pop(k)
    return value


def getRank(options, assoc, freq):
    rank = {}
    associationvalue = 0
    for k1, v1 in freq.items():
        for k2, v2 in assoc.items():
            if k1 == k2:
                occfreq = freq[k2]
                item = assoc[k2][int(options)]
                for k, v in item.items():
                    associationvalue = v
                rank[k2] = int(associationvalue) * int(occfreq)
    tupleList = [(k, v) for k, v in rank.items()]
    sortedRank = sorted(tupleList, key=lambda x: x[1], reverse=True)
    return sortedRank
