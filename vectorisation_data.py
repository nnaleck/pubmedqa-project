#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer



def corpus_list(df,ind) :
    """
    Parameters
    ----------
    df1 : dataframe
        preprocessed dataset.
    ind : string : 'Question', 'Long_Answer', 'Contexts' or 'Full_Text'
        the column to vectorize.

    Returns
    -------
    corpus : string list
           list of ind.

    """
    corpus = [] #List of ind
    for i in df.index :
        #In case no full_text : no new line
        if type(df[ind][i]) == str :
            line = str(df[ind][i]) 
        #Add line to corpus list without special characters and capital letters 
        corpus.append(re.sub(r"[^a-zA-Z0-9 ]"," ",line.lower()))
    
    return corpus

    

def words_to_delete(corpus):
    """
    Preprocessing of the words in the corpus list

    Parameters
    ----------
    corpus : string list
        list of text to process.

    Returns
    -------
    words_to_delete : string list
        list of words to delete.

    """
   
    #List of words with length <= 3
    words_to_delete1 = []
    for text in corpus :
        word_list = text.split() 
        for word in word_list :
            word = str(word)
            if (word not in words_to_delete1) :
                if (len(word) <=3):
                    words_to_delete1.append(word)
    
    # expr = re.compile("\W+",re.U)
    words_dico = dict() #Dictionary (word: occurrence)
    for text in corpus: #For each sentence of the corpus
        
        # text = str(text)
        # text = expr.split(text)
        text = text.split()
        for word in set(text): #Recovering each new word
            if word not in words_dico:
                words_dico[word]=1
            else: #For each word already listed: add 1
                words_dico[word]=words_dico[word]+1
                
    maximum = np.quantile(list(words_dico.values()), 0.9)
    minimum = np.min(list(words_dico.values()))
    
    
    words_freq = list()
    for key, val in words_dico.items():
        words_freq.append( (key, val) )
    words_freq.sort(key=lambda tup: tup[1] ,reverse=True)
    
    #List of too rare words
    words_to_delete2 = [t[0] for t in words_freq if t[1]<=minimum]
    
    
    #List of the most frequent words (with quantile at 0.9)
    words_to_delete3 = [t[0] for t in words_freq[:int(maximum)]]
    
    
     
    #Merge lists
    words_to_delete = words_to_delete1 + words_to_delete2 + words_to_delete3
    return words_to_delete

  
    
    
def vectorization(corpus,words_to_delete,ind) : 
    """

    Parameters
    ----------
    corpus : string list
        list of text to process.
    words_to_delete : string list
        list of words to delete.
    ind : string : 'Question', 'Long_Answer', 'Contexts' or 'Full_Text'
        the column to vectorize.

    Returns
    -------
    None.

    """
    
    #Stop_words : words to deleete
    vectorizer = CountVectorizer(stop_words=words_to_delete,
                                binary=True)
    
    X = vectorizer.fit_transform(corpus)
    
    tokens = vectorizer.get_feature_names()
    
    df_vect = pd.DataFrame(data = X.toarray(),
                                index=(corpus),
                                columns = tokens)
    df_vect.to_csv(ind+'.csv', index=True) 
    
    #vectorization with tf-idf
    tfidfvectorizer = TfidfVectorizer(stop_words=words_to_delete,
                                      use_idf=True,
                                      smooth_idf=True)
    
    Y = tfidfvectorizer.fit_transform(corpus)
    
    tfidf_tokens = tfidfvectorizer.get_feature_names()
    
    df_tfidfvect = pd.DataFrame(data = Y.toarray(),
                                index=(corpus),
                                columns = tfidf_tokens)
    
    df_tfidfvect.to_csv(ind+'_tfidf.csv', index=True) 
    
df = pd.read_csv('ft.csv')

#Vectorization of questions
corpus1 = corpus_list(df,'Question')
words_to_delete1 = words_to_delete(corpus1)
vectorization(corpus1,words_to_delete1,'Question') 

#Vectorization of answers
corpus2 = corpus_list(df,'Long_Answer')
words_to_delete2 = words_to_delete(corpus2)
vectorization(corpus2,words_to_delete2,'Long_Answer') 

#Vectorization of contexts
corpus3 = corpus_list(df,'Contexts')
words_to_delete3 = words_to_delete(corpus3)
vectorization(corpus3,words_to_delete3,'Contexts') 

#Vectorization of full_text
corpus4 = corpus_list(df,'Full_Text')
words_to_delete4 = words_to_delete(corpus4)
vectorization(corpus4,words_to_delete4,'Full_Text') 