import json
import nltk
import mongo
import string
import pprint
import os



def basic(file):
    tokens = []
    freq_count = {}
    notFound = {}
    result = {}
    text = ''
    fname = os.path.join('C:/Users/Kevin/Google Drive/college/Year4/Web Dev/data analysis assignment/uploads', file.filename)
    print('filename',fname)
    with open(fname) as s:
            with open('lower_case_version.txt', 'w', encoding='utf-8') as lower_s:
                for word in s:
                    word = word.lower()
                    print(word, file=lower_s)
    with open('ea-thesaurus-lower.json') as normsf:
        norms = json.load(normsf)
    with open('lower_case_version.txt', encoding='utf-8') as s:
        for line in s.readlines():
            # using both nltk to tokenize word and using string to translate punctuation into a space
            tokens += nltk.word_tokenize(line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))))
            text += line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        # print('text\n',text,'\n')
        text_digest = mongo.checkIfExists(text)
        if text_digest is not None:
            mongo.find(text_digest)
        else:
            for element in tokens:
                if element == '•' or element == '–' or element == '-' or element == '¬':
                    tokens.remove(element)
        for element in tokens:
            freq_count[element] = tokens.count(element)
        for k, v in norms.items():
            for key in freq_count.keys():
                if k == key:
                    value = v[:3]
                    v = cleanValues(value)
                    result[key] = value
                if key not in norms.keys():
                    notFound[key] = 'not found'
        return mongo.insert(result, notFound, freq_count, text)


# goes through keys in associations and replaces punctuation with a space
def cleanValues(value: list):
    for element in value:
        temp = {}
        temp = element
        for k in temp.keys():
            newKey = k.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            element[newKey] = element.pop(k)
    return value

