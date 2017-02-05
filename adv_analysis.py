import json
import nltk
import mongo
import string
import os
import basic_analysis


def advanced(file, option):
    tokens = []
    freq_count = {}
    notFound = {}
    result = {}
    text = ''
    values = {}
    value = []
    rank = {}
    associationvalue = 0
    fname = os.path.join('C:/Users/Kevin/Google Drive/college/Year4/Web Dev/data analysis assignment/uploads', file.filename)
    with open(fname, encoding='utf-8') as s:
        with open('lower_case_version.txt', 'w', encoding='utf-8') as lower_s:
            for word in s:
                word = word.lower()
                print(word, file=lower_s)
    with open('ea-thesaurus-lower.json') as normsf:
        norms = json.load(normsf)
    with open('lower_case_version.txt',encoding='utf-8' ) as s:
        for line in s.readlines():
            # using both nltk to tokenize word and using string to translate punctuation into a space
            tokens += nltk.word_tokenize(line.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))))
            text += line.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        for element in tokens:
            if element == '•' or element == '–' or element == '-' or element == '¬':
                tokens.remove(element)
    for element in tokens:
        freq_count[element] = tokens.count(element)
    for k, v in norms.items():
        for key in freq_count.keys():
            if k == key:
                value = v[:3]
                v = basic_analysis.cleanValues(value)
                result[key] = value
            if key not in norms.keys():
                notFound[key] = 'not found'
    for k1, v1 in freq_count.items():
        for k2, v2 in result.items():
            occfreq = freq_count[k2]
            item = result[k2][int(option)]
            for k, v in item.items():
                associationvalue = v
            rank[k2] = int(associationvalue) * int(occfreq)
    tupleList = [(k, v) for k, v in rank.items()]
    sortedRank = sorted(tupleList, key=lambda x:x[1],reverse=True)
    return mongo.adv_insert(result, notFound,freq_count, text, sortedRank)
