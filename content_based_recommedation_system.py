# -*- coding: utf-8 -*-
"""content based recommedation system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/129IsQ_Lv4BOGbJVCWbmCL84cu3THabdW
"""

!rm songdata.*
!wget https://github.com/ugis22/music_recommender/blob/master/content%20based%20recommedation%20system/songdata.csv?raw=true
!mv songdata.* ./songdata.csv

import numpy as np
import pandas as pd

from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

songs = pd.read_csv('/content/songdata.csv')
songs.head(20)

songs = songs[:5000].drop('link', axis=1).reset_index(drop=True)
songs['text'] = songs['text'].str.replace(r'\n', '')
songs.head()

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
lyrics_matrix = tfidf.fit_transform(songs['text'])

cosine_similarities = cosine_similarity(lyrics_matrix)
similarities = {}

for i in range(len(cosine_similarities)):
    # Now we'll sort each element in cosine_similarities and get the indexes of the songs. 
    similar_indices = cosine_similarities[i].argsort()[:-10:-1] 
    # After that, we'll store in similarities each name of the 50 most similar songs.
    # Except the first one that is the same song.
    similarities[songs['song'].iloc[i]] = [(cosine_similarities[i][x], songs['song'][x], songs['artist'][x]) for x in similar_indices][1:]
# similarities.values()

class Recommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix

    def _print_message(self, song, recom_song):
        rec_items = len(recom_song)
        
        print(f'The {rec_items} recommended songs for {song} are:')
        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score") 
            print("--------------------")
        
    def recommend(self, recommendation):
        # Get song to find recommendations for
        song = recommendation['song']
        # Get number of songs to recommend
        number_songs = recommendation['number_songs']
        # Get the number of songs most similars from matrix similarities
        if (number_songs < 0):
            recom_song = self.matrix_similar[song]
            return recom_song
        else:
            recom_song = self.matrix_similar[song][:number_songs]
            # print each item
            self._print_message(song=song, recom_song=recom_song)

recommedations = Recommender(similarities)

print(songs['song'])
#song_idx = 2008
#inp = song_idx
sname = "As Good As New"

recommendation = {
    "song": sname,
    "number_songs": 4 
}
recommedations.recommend(recommendation)

recommendation2 = {
    "song": songs['song'].iloc[2456],
    "number_songs": 4 
}
recommedations.recommend(recommendation2)



"""### Predict by similarity score and emotion"""

!git clone https://github.com/sheemachinnu/music-recommendation-system

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn import svm
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
warnings.filterwarnings("ignore")
import pandas as pd
import nltk
import re
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

df=pd.read_csv("/content/music-recommendation-system/datasets/lyrics_emotion_dataset/training.csv")
df_new=pd.read_csv("/content/music-recommendation-system/datasets/lyrics_emotion_dataset/testing.csv")
df.head()

df_new['lyrics'] = [entry.lower() for entry in df_new['lyrics']]
df_new['lyrics']= [word_tokenize(entry) for entry in df_new['lyrics']]

df['lyrics'] = [entry.lower() for entry in df['lyrics']]
df['lyrics']= [word_tokenize(entry) for entry in df['lyrics']]

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV
for index,entry in enumerate(df_new['lyrics']):
    Final_words = []
    word_Lemmatized = WordNetLemmatizer()
    for word, tag in pos_tag(entry):
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    df_new.loc[index,'text_final'] = str(Final_words)

df_new.tail()

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV
for index,entry in enumerate(df['lyrics']):
    Final_words = []
    word_Lemmatized = WordNetLemmatizer()
    for word, tag in pos_tag(entry):
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    df.loc[index,'text_final'] = str(Final_words)

"""### Creating Training data, training label, test data, test label"""

train_x = df['text_final']
valid_x = df_new['text_final']
train_y = df['mood']
valid_y = df_new['mood']

Encoder = LabelEncoder()
train_y = Encoder.fit_transform(train_y.ravel())
valid_y = Encoder.fit_transform(valid_y.ravel())

classLabels = {}
encoderClasses = Encoder.classes_

for i in range(len(encoderClasses)):
    classLabels[i] = encoderClasses[i]

classLabels

all_texts = []
for items in train_x:
    all_texts.append(items) 
for items in valid_x:
    all_texts.append(items)
print(all_texts[0])

"""### TfidfVectorizer Model"""

def tokenizer(text):
    lower_txt = text.lower()
    tokens = nltk.wordpunct_tokenize(lower_txt)
    no_punct = [s for s in tokens if re.match('^[a-zA-Z]+$', s) is not None]
    return no_punct

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect = TfidfVectorizer(
            encoding='utf-8',
            decode_error='replace',
            strip_accents='unicode',
            analyzer='word',
            binary=False,
            stop_words="english",
            tokenizer=tokenizer
    )

#tfidf_vect = TfidfVectorizer(analyzer='word',max_features=7000)
tfidf_vect.fit(all_texts)
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)

"""### Model"""

from sklearn.metrics import f1_score

claf=svm.LinearSVC(class_weight="balanced")
claf.fit(xtrain_tfidf,train_y)
p = claf.predict(xvalid_tfidf)

score = f1_score(valid_y[:len(p)], p, average='weighted')
print("F1_Score", "{:.2f}".format(score))

def predictEmotion(lyrics):
    wt=word_tokenize(lyrics)
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    Final_words = []
    word_Lemmatized = WordNetLemmatizer()
    for word, tag in pos_tag(wt):
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    result = str(Final_words)
    df9=pd.DataFrame(columns=["lyrics"])
    df9=df9.append({'lyrics':result},ignore_index=True)
    
    testx=df9['lyrics']
    
    xvalid_tfidf =  tfidf_vect.transform(testx)
    y=claf.predict(xvalid_tfidf)

    return classLabels[y[0]]

recommendation = {
    "song": sname,
    "number_songs": -1
}

recommnded_songs = recommedations.recommend(recommendation)
emotionOfSelectedSong = predictEmotion(songs[songs['song'] == sname]['text'].values[0])
emotionOfSelectedSong

songs

noOfRecomendations = 4
reccomendedSongsByEmotion = []

for song in recommnded_songs:
    emotion = predictEmotion(songs["text"][songs["song"] == song[1]].values[0])
    # print(songs["text"][songs["song"] == song[1]].values[0])
    if (emotionOfSelectedSong == emotion):
        reccomendedSongsByEmotion.append((song[1], song[0], emotion))
        noOfRecomendations -= 1
        if (noOfRecomendations == 0): break

n = len(reccomendedSongsByEmotion)

print(f'The {n} recommended songs for {sname} are:\n')
for i in range(n):
    print(f"Number {i+1}:")
    print(f"{reccomendedSongsByEmotion[i][0]} with {round(reccomendedSongsByEmotion[i][1], 3)} similarity score with mood {reccomendedSongsByEmotion[i][2]}") 
    print("--------------------")







