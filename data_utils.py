import collections


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


def combine(assoc:dict , freq:dict, rank:list):
    temp = {}
    for key, value in assoc.items():
        for k,v in freq.items():
            if key == k:
                for element in rank:
                    if element[0] == key:
                        temp[key] = {'word': key,'associations': value, 'frequency': v, 'rank': element[1]}
    return temp