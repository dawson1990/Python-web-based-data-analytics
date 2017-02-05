import json
import nltk
from collections import Counter

with open('ea-thesaurus-lower.json') as normsf:
	norms = json.load(normsf)
    
tokens = []
wordOccur = {}
with open('lower_case_sample.txt') as s:
    for line in s.readlines():
        tokens += nltk.word_tokenize(line)
    for element in tokens:
        if element == ',' or element == '.' or element == '–' or element == '-' or element == '/' or element == '(' or element == ')' or element == ':'or element ==';' or element == '•' or element == '?' or element == '!' or element =='#':
            tokens.remove(element)
    for element in tokens:
        wordOccur += { 'k' : element , 'v': tokens.count(element)}
print(type(wordOccur))
print(wordOccur)
##notFound = []
##
##for element in tokens:
##    for k, v in norms.items():
##       # try:
##        if k == element:
##            print(element, v[:3],'\n')
##        else:
##            notFound.append(element)
##       # except:
##                
##
##for i in notFound:
##    print(i)

