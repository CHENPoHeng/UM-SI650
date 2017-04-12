from nltk.tokenize import RegexpTokenizer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from scipy.sparse import find
#training_data_path = '../data/train.tsv'
#test_data_path = '../data/test.tsv'
#stop_list_path = '../data/stoplist.txt'

course_data = pd.read_csv('data/course/eecs_course_list.csv')
course_desc = list(course_data['description'].fillna(''))


#course_desc_list = []
#for line in course_desc:
#    if type(line) is str:
#        text_not_filtered = tokenizer.tokenize(line)
#    #    text_not_filtered = line.split()
#        filtered_text = [word.lower() for word in text_not_filtered \
#                         if word.lower() not in stop_words]
#    #    filtered_text = [word.lower() for word in text_not_filtered]
#        course_desc_list.append(filtered_text)
#
#stopwords = re.compile('['+ '|'.join(stop_words) + ']')

query = 'software engineering'

#==============================================================================
# Convert text into scipy sparse matrix
#==============================================================================
#vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,2))
stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r'[a-zA-Z]{1,}')
vectorizer = CountVectorizer(min_df=1, ngram_range=(1,1), tokenizer=tokenizer.tokenize, stop_words=stop_words)
course_corpus = vectorizer.fit_transform(course_desc)
#test_corpus = vectorizer.transform(comments_test)
dictionary = vectorizer.vocabulary_
dictionary_inv = dict(zip(dictionary.values(), dictionary.keys()))
query_transformed = vectorizer.transform([query])
#==============================================================================
# Retrieve Documents
#==============================================================================
query_word_list = []
query_index = find(query_transformed)[1]
res = []

# Only retrieve docs with all query words
for i in range(course_corpus.shape[0]):
    retrieve_idx = course_corpus[i, query_index]
    if len(find(retrieve_idx)[2]) == len(query_index):
#    if len(find(retrieve_idx)[2]) > 0:
        res.append(i)

     