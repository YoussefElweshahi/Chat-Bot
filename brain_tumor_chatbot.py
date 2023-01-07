# -*- coding: utf-8 -*-
"""brain_tumor_chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J8NRSKmG1GauJxA2UDvtJmlSHVtDcsjN
"""

import random
import string
import nltk

nltk.download('omw-1.4')

"""loading the file"""

f=open('/content/brain.txt','r',errors='ignore')
raw_doc=f.read()
raw_doc=raw_doc.lower() #convert text to lower case
nltk.download('punkt') #punkt tokenizer
nltk.download('wordnet') #wordnet dictionary
sentence_tokens = nltk.sent_tokenize(raw_doc) #convert document to list of sentences
word_tokens=nltk.word_tokenize(raw_doc)  #convert doc to list of words

sentence_tokens[:2]

word_tokens[:2]

"""Text processing

"""

lemmer=nltk.stem.WordNetLemmatizer()

def lem_tokens(tokens):
  return[lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
  
def lem_normalize(text):
  return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

"""greeting function"""

greet_inputs=("hello","hi","what's up","hey")
greet_response=["hi","hey","hi there","hello","hola"]

def greet(sentence):
  for word in sentence.split():
    if word.lower() in greet_inputs:
      return random.choice(greet_response)

"""response 

"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  bot1_response=''
  TfidfVec = TfidfVectorizer(tokenizer = lem_normalize , stop_words='english')
  tfidf= TfidfVec.fit_transform(sentence_tokens)
  vals = cosine_similarity(tfidf[-1], tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf=flat[-2]
  if(req_tfidf==0):
    bot1_response = bot1_response + "sorry, i don't understand"
  else:
    bot1_response = bot1_response + sentence_tokens[idx]
    return bot1_response

"""start conversation"""

flag=True
print("Baxi: how can i help you ")
while (flag==True):
  user_response= input()
  user_response= user_response.lower()
  if (user_response != 'bye'):
    if(user_response == 'thanks' or user_response=='thank you'):
      flag=False
      print("Baxi: You are welcome !")

    else: 
     if(greet(user_response)!= None):
        print("Baxi: "+ greet(user_response))

     else:

      sentence_tokens.append(user_response)
      word_tokens=word_tokens+nltk.word_tokenize(user_response)
      final_words= list(set(word_tokens))
      print("Baxi: ",end=" ")
      print(response(user_response))
      sentence_tokens.remove(user_response)
  else:
    flag=False
    print("Baxi: Good bye, chat with you later ")
