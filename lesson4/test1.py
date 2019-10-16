import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
from sklearn.model_selection import train_test_split
baby_df = pd.read_csv('amazon_baby.csv')

#1
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

baby_df['review_clean'] = baby_df['review'].fillna("").apply(remove_punctuation)

#2
def convert_rating(rate):
    if rate == 3:
        return 0
    return -1 if rate < 3 else 1

baby_df['sentiment'] = baby_df['rating'].apply(convert_rating)

#3
baby_train, baby_test = train_test_split(baby_df, test_size=0.9, random_state=44)

#4
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(token_pattern = r'\b\w+\b')
#Use thise token pattern to keep single-letter words
#First learn vocabulary from the training data and assign columns to words
#Then convert the training data into sparce_matrix
train_matrix = vectorizer.fit_transform(baby_train['review_clean'])
words = vectorizer.get_feature_names()
#Then convert the test data into sparce matrix, using the ane word-column mapping
test_matrix = vectorizer.transform(baby_test['review_clean'])
print (train_matrix)
print (test_matrix)

#5
from sklearn.linear_model import LogisticRegression
sentiment_model = LogisticRegression(random_state=0, solver='warn', multi_class='warn').fit(train_matrix, baby_train['sentiment'])
# print(clf)
suma =sum(x >= 0 for x in baby_df['sentiment'])
print(suma)

#6
dupa = test_matrix[0]
print(test_matrix[0])
# reprezentacja recenzji jako ilości słów
test_prediction = sentiment_model.predict( test_matrix)
print(test_prediction)