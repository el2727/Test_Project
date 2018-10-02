# Importing all necessary libraries

import json
import pandas
import os
import glob
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
import numpy
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

# A. CLASSIFICATION


# 1. Restructuring data for classification

# Extracting publication-dataset pairs from "data_set_citations.json"

# Importing and loading the JSON file

file = open('data_set_citations.json', 'r')
json_file = json.load(file)

# Reference link: https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file

# Creating lists and extracting publication and dataset indices

list_pub = []
list_dataset = []
for i in json_file:
    pub = i['publication_id']
    dataset = i['data_set_id']
    list_pub.append(pub)
    list_dataset.append(dataset)

# Saving data to a dataframe and then to a .csv file

data = pandas.DataFrame(list_pub, columns=['publication'])
data['dataset']=list_dataset

# Create folders on the local machine based on dataset indexes

set_dataset = set(list_dataset)
for i in set_dataset:
    os.mkdir(str(i))

# Reference link: https://stackoverflow.com/questions/17889814/create-folders-in-directory-from-values-in-list-python

# Moving of files from "text" folder to multiple folders with dataset indices is performed using "Pub_dataset.csv" and a VBA code in Excel per this reference link: https://www.ozgrid.com/forum/forum/help-forums/excel-general/126154-vba-code-to-move-multiple-files

# As a result we have the following data structure: a folder which contains multiple folders with dataset indices (the classification "labels") and those folders contain texts of all articles associated with a given dataset.

# 2. Loading restuctured data using Sklearn

# Using sklearn load_files function, importing restructured data
# Access to text files is through .data and to classification labels is through .target (folder names based on dataset indices)

data_folder = 'sample_2/'
all_data = load_files(data_folder)

# Reference link: https://github.com/scikit-learn/scikit-learn/blob/master/doc/tutorial/text_analytics/solutions/exercise_01_language_train_model.py

# 3. Creating training and test data
# Training and test data are created using sklearn train_test_split function

docs_train, docs_test, y_train, y_test = train_test_split(
    all_data.data, all_data.target, test_size=0.5)

# Reference link: https://github.com/scikit-learn/scikit-learn/blob/master/doc/tutorial/text_analytics/solutions/exercise_01_language_train_model.py

# 4. Performing TF-IDF transformation on data, training classifiers through Pipeline from Sklearn

classifier_one = Pipeline([('vect', CountVectorizer()),
...                      ('tfidf', TfidfTransformer()),
...                      ('clf', MultinomialNB()),
... ])

# Reference link: https://github.com/scikit-learn/scikit-learn/blob/master/doc/tutorial/text_analytics/working_with_text_data.rst

classifier_one.fit(docs_train, y_train)

classifier_two = Pipeline([('vect', CountVectorizer()),
                           ('tfidf', TfidfTransformer()),
                           ('clf', SGDClassifier(penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                          ])

classifier_two.fit(docs_train, y_train)

# 6. Making predictions on test data

predicted_one = classifier_one.predict(docs_test)

predicted_proba = classifier_one.predict_proba(docs_test)

predicted_two = classifier_two.predict(docs_test)

predicted_confidence_score = classifier_two.decision_function(docs_test)

# 7. Evaluation

accuracy_one = numpy.mean(predicted_one == y_test)

print(predicted_proba)

accuracy_two = numpy.mean(predicted == y_test)

print(predicted_confidence_score)

# B. INFORMATION RETRIEVAL (DOCUMENT RELEVANCE)

# 1. Extracting relevant fields from JSON file on datasets (name, metadata description and list of mentions)¶

# Import data_sets.json file and extracting 'title', 'description' and 'mention_list' fields

file = open('data_sets.json', 'r')
json_file = json.load(file)

list_title = []
list_description = []
list_mention = []
for i in json_file:
    title = i['title']
    description = i['description']
    mention = i['mention_list']
    list_title.append(title)
    list_description.append(description)
    list_mention.append(mention)

# Converting to a string

list_mention_updated = []
for i in list_mention:
    string = ' '.join(i)
    list_mention_updated.append(string)

# Reference link: https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string

# 2. Concatenating all information on datasets together

created_list= [' '.join(i) for i in zip(list_title, list_description, list_mention_updated)]

# Reference link: https://stackoverflow.com/questions/40912968/how-to-concatenate-multiple-lists-element-wise

# 3. Creating corresponding text files for further download in Sklearn

set_dataset_list = []
for i in set_dataset:
    y = str(i) + '.txt'
    set_dataset_list.append(y)

for i, y in zip(created_list, set_dataset_list):
    with open(y, 'w', encoding='utf-8') as output:
        output.write(i)
        
# Reference link: https://stackoverflow.com/questions/6673092/printing-out-elements-of-list-into-separate-text-files-in-python
# Reference link: https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters

text_files = glob.glob(os.path.join(os.getcwd(), 'sample_1', '*.txt'))

list_text_files = []

for i in text_files:
    with open(i) as y:
        list_text_files.append(y.read())
        
# Reference link: https://stackoverflow.com/questions/42407976/loading-multiple-text-files-from-a-folder-into-a-python-list-variable

# 4. Creating TD-IDF representations of dataset strings and documents

combined_list = list_text_files + all_data.data

# 5. Calculating similarity

tfidf = TfidfVectorizer().fit_transform(combined_list)
(tfidf * tfidf.T).A

# Reference link: https://stackoverflow.com/questions/8897593/similarity-between-two-text-documents

# Using gensim

# Reference link: https://www.oreilly.com/learning/how-do-i-compare-document-similarity-using-python
