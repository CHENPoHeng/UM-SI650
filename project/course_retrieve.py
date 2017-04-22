from gensim import corpora, models, similarities
from gensim.matutils import corpus2csc
import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer

course_path = "data/output/eecs_course_list.csv"
stop_list_path = "data/stoplist.txt"
query = 'software engineering'

# Create a stop word list
stop_list = set()
with open(stop_list_path, "r+") as f:
  for line in f:
    if not line.strip():
    	continue
    stop_list.add(line.strip().lower())


course_data = pd.read_csv(course_path)
code_desc_dict = dict(zip(course_data['code'], course_data['description']))
idx_courses_dict = dict(zip(list(range(len(code_desc_dict))), tuple(zip(course_data['code'], course_data['description']))))
result_dict=dict(zip(course_data['code'],tuple(zip(course_data['title'],course_data['credit']))))

tokenizer = RegexpTokenizer(r'[a-zA-z]{2,}') # Exclude single letter
course_descriptions = []
for doc in list(code_desc_dict.values()):
    if type(doc) is str:
        text_raw = tokenizer.tokenize(doc)
        text_filtered = [word.lower() for word in text_raw if word not in stop_list]
        course_descriptions.append(text_filtered)
    else: 
        course_descriptions.append([])

# TODO: If the query words are not in the vocabulary, what to do?
# Use word2vec?
dictionary = corpora.Dictionary(course_descriptions)
corpus = [dictionary.doc2bow(text) for text in course_descriptions]
voc_id = dictionary.token2id
id_voc = dict(zip(voc_id.values(), voc_id.keys()))
# Initialize tf-idf model
tfidf = models.TfidfModel(corpus) 
corpus_tfidf = tfidf[corpus] # Transform the whole corpus
print('TF-IDF model created.')


# Create a LSI model
num_dims = 256
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_dims)
corpus_lsi = lsi[corpus_tfidf]
print('LSI corpus created.')

# Retrieve 
q_bow = dictionary.doc2bow(query.lower().split())
q_lsi = lsi[q_bow] # convert the query to LSI space

# transform corpus to LSI space and index it
index = similarities.MatrixSimilarity(lsi[corpus]) 
# Save corpus LSI index 
#index.save('/tmp/deerwester.index')
#index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[q_lsi] # perform a similarity query against the corpus
#print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples

sims = sorted(enumerate(sims), key=lambda item: -item[1])

for p in sims:
    print(idx_courses_dict[p[0]][0],result_dict[idx_courses_dict[p[0]][0]]) 