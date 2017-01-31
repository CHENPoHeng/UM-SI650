## Question 1: Edit Distance 
# This code is contributed by Bhavya Jain
# A Naive recursive Python program to fin minimum number
# operations to convert str1 to str2
def editDistance(str1, str2, m , n):
    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m==0:
         return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n==0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m-1]==str2[n-1]:
        return editDistance(str1,str2,m-1,n-1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(editDistance(str1, str2, m, n-1),    # Insert
                   editDistance(str1, str2, m-1, n),    # Remove
                   editDistance(str1, str2, m-1, n-1)    # Replace
                   )

s1 = 'kitten'
s2 = 'kitchen'
print editDistance(s1, s2, len(s1), len(s2))

s1 = 'familiar'
s2 = 'similarity'
print editDistance(s1, s2, len(s1), len(s2))

## Question 2: Vector Representation
import math as m
import numpy as np

# basic vector representation
q = np.array([1,1,0,0,0,0,0,0,0])
d1 = np.array([0,1,1,1,0,0,0,0,0])
d2 = np.array([0,0,1,1,1,1,1,0,0])
d3 = np.array([0,1,0,0,0,0,0,1,1])

for i in [d1, d2, d3]:
    numerator = sum(q*i)
    denominator = m.sqrt(sum(q**2))*m.sqrt(sum(i**2))
    print numerator / denominator

# remove stop words
q = np.array([1,1,0,0,0,0,0])
d1 = np.array([0,1,1,0,0,0,0])
d2 = np.array([0,0,1,1,1,0,0])
d3 = np.array([0,1,0,0,0,1,1])

for i in [d1, d2, d3]:
    numerator = sum(q*i)
    denominator = m.sqrt(sum(q**2))*m.sqrt(sum(i**2))
    print numerator / denominator

# normalized similar words such as 'computing', 'computer'
# [computer, information, school, institute, science]
q = np.array([1,1,0,0,0])
d1 = np.array([0,1,1,0,0])
d2 = np.array([1,1,1,0,0])
d3 = np.array([0,1,0,1,1])

for i in [d1, d2, d3]:
    numerator = sum(q*i)
    denominator = m.sqrt(sum(q**2))*m.sqrt(sum(i**2))
    print numerator / denominator

# weighted 
q = np.array([1,1,0,0,0])
d1 = np.array([0,1,3,0,0])
d2 = np.array([1,1,3,0,0])
d3 = np.array([0,1,0,1,1])

for i in [d1, d2, d3]:
    numerator = sum(q*i)
    denominator = m.sqrt(sum(q**2))*m.sqrt(sum(i**2))
    print numerator / denominator

## Question 4: Word Distribution
import nltk 

## 4-1
# load in stopwords
with open('stoplist.txt', 'r') as f:
    sw = f.read().split('\n')   

# load in documents
with open('blog.txt', 'r') as f:
    b = f.read()

b = nltk.word_tokenize(b)
b = [w.lower() for w in b]

# word counts
words = {}
for i in b:
    if i in words:
        words[i] += 1
    else:
        words[i] = 1

# remove stopwords
for i in sw:
    words.pop(i, None)

wordsFreq = sorted(words.values())

# words proportion counts
freqPro = {}
for i in set(wordsFreq):
    freqPro[i] = wordsFreq.count(i)

# plot word frequency vs. frequency proportion
import matplotlib.pyplot as plt
from math import log
import pandas as pd
tmp = pd.DataFrame(list(freqPro.items()), columns = ['word_freq', 'freq_Prop'])
tmp = tmp.sort('word_freq')
lineB = plt.plot(np.log(tmp.word_freq), np.log(tmp.freq_Prop), label = 'Blog')
# x = [log(i) for i in list(freqPro.keys())]
# y = [log(i) for i in list(freqPro.values())]
# plt.plot(x, y)
# plt.savefig('blog_plot.png')

# congress speech
with open('congress_speech.txt', 'r') as f:
    s = f.read()

s = nltk.word_tokenize(s)
s = [w.lower() for w in s]

# word counts
words = {}
for i in s:
    if i in words:
        words[i] += 1
    else:
        words[i] = 1

# remove stopwords
for i in sw:
    words.pop(i, None)

wordsFreq = sorted(words.values())

# words proportion counts
freqPro = {}
for i in set(wordsFreq):
    freqPro[i] = wordsFreq.count(i)

# plot word frequency vs. frequency proportion
import matplotlib.pyplot as plt
from math import log
tmp = pd.DataFrame(list(freqPro.items()), columns = ['word_freq', 'freq_Prop'])
tmp = tmp.sort('word_freq')

lineS = plt.plot(np.log(tmp.word_freq), np.log(tmp.freq_Prop), label = 'Congress Speech')
plt.title('Blog and Congress Speech Word Distribution')
plt.xlabel('frequency of words (in log)')
plt.ylabel('proportion of frequency (in log)')
plt.legend(loc='upper right')
plt.savefig('plot.png')

## 4-2
# load in again
with open('congress_speech.txt', 'r') as f:
    sRaw = f.read()

s = nltk.word_tokenize(sRaw)
# s = [w.lower() for w in s]

with open('blog.txt', 'r') as f:
    bRaw = f.read()

b = nltk.word_tokenize(bRaw)
# b = [w.lower() for w in b]

# vocabulary size
print ('congress speech vocabulary size: ', len(set(s)))
print ('blog vocabulary size: ', len(set(b)))

# freq of sw
swSumB = []
swSumS = []
for i in sw:
    swSumS.append(s.count(i))
    swSumB.append(b.count(i))

print ('congress speech stopword freq: ', sum(swSumS))
print ('blog stopword freq: ', sum(swSumB))

# capital words
import re
print ('congress speech # of capital letters: ', len(re.findall('[A-Z]', sRaw)))
print ('blog # of capital letters: ', len(re.findall('[A-Z]', bRaw)))

# ave # of chars per word
sNChar = sum([ len(i) for i in s ]) / len(s)
bNChar = sum([ len(i) for i in b]) / len(b)

# # of nouns(NN), adj(JJ), verb(VB), adverb(RB), pronouns(PRP)
sTag = nltk.pos_tag(s)
bTag = nltk.pos_tag(b)

sNNN = len([i[1] for i in sTag if 'NN' in i[1]])
sNJJ = len([i[1] for i in sTag if 'JJ' in i[1]])
sNVB = len([i[1] for i in sTag if 'VB' in i[1]])
sNRB = len([i[1] for i in sTag if 'RB' in i[1]])
sNPRP = len([i[1] for i in sTag if 'PRP' in i[1]])
print ('congress speech # of NN, JJ, VB, RB, PRP: ', sNNN, sNJJ, sNVB, sNRB, sNPRP)

bNNN = len([i[1] for i in bTag if 'NN' in i[1]])
bNJJ = len([i[1] for i in bTag if 'JJ' in i[1]])
bNVB = len([i[1] for i in bTag if 'VB' in i[1]])
bNRB = len([i[1] for i in bTag if 'RB' in i[1]])
bNPRP = len([i[1] for i in bTag if 'PRP' in i[1]])
print ('blog # of NN, JJ, VB, RB, PRP: ', bNNN, bNJJ, bNVB, bNRB, bNPRP)

## top 10 NN, VB, JJ
sTagFreq = nltk.FreqDist(sTag)
bTagFreq = nltk.FreqDist(bTag)

print ('congress speech top 10 nouns: ', [i[0] for (i, _) in sTagFreq.most_common() if i[1] == 'NN'][:10])
print ('congress speech top 10 verbs: ', [i[0] for (i, _) in sTagFreq.most_common() if i[1] == 'VB'][:10])
print ('congress speech top 10 adjectives: ', [i[0] for (i, _) in sTagFreq.most_common() if i[1] == 'JJ'][:10])

print ('blog top 10 nouns: ', [i[0] for (i, _) in bTagFreq.most_common() if i[1] == 'NN'][:10])
print ('blog top 10 verbs: ', [i[0] for (i, _) in bTagFreq.most_common() if i[1] == 'VB'][:10])
print ('blog top 10 adjectives: ', [i[0] for (i, _) in bTagFreq.most_common() if i[1] == 'JJ'][:10])

## python underscore
## http://stackoverflow.com/questions/5893163/what-is-the-purpose-of-the-single-underscore-variable-in-python


## 4-3 TF-IDF

with open('congress_speech.txt', 'r') as f:
    sRaw = f.read()

s = nltk.word_tokenize(sRaw)
# s = [w.lower() for w in s]

with open('blog.txt', 'r') as f:
    bRaw = f.read()

b = nltk.word_tokenize(bRaw)

# remove stopwords
b = list(filter(lambda a: a not in sw, b))
s = list(filter(lambda a: a not in sw, s))

# congress TF-IDF
tmp = {}
for i in s:
    if i in tmp:
        tmp[i] += 1
    else:
        tmp[i] = 1

sTF = {i: np.log(tmp[i]+1) for i in tmp}

# IDF
documentFreq = {i:1 for i in set(s)}
for i in set(b):
    if i in documentFreq:
        documentFreq[i] += 1
    else:
        documentFreq[i] = 1

sIDF = {i : 1 + log(2 / documentFreq[i]) for i in set(s)}
sTFIDF = {i: j*sIDF[i] for i, j in sTF.items()}
sTop10 = sorted(sTFIDF.items(), key = lambda x:x[1], reverse = True)[:20]

# blog TF-IDF
tmp = {}
for i in b:
    if i in tmp:
        tmp[i] += 1
    else:
        tmp[i] = 1

bTF = {i: np.log(tmp[i]+1) for i in tmp}

# IDF
bIDF = {i : 1 + log(2 / documentFreq[i]) for i in set(b)}
bTFIDF = {i: j*bIDF[i] for i, j in bTF.items()}
bTop10 = sorted(bTFIDF.items(), key = lambda x:x[1], reverse = True)[:20]

