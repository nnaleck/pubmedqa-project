#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re




def vectorisation(df,ind):
    """
    Vectorization without column preprocessing

    Parameters
    ----------
    df : dataframe
        preprocessed dataset.
    ind : string : 'Question', 'Long_Answer', 'Contexts' or 'Full_Text' 
        the column to vectorize.

    Returns
    -------
    Matrix : vectorized matrix without preprocessing.

    """
    columns = [] #List of terms
    lines = [] #List of ind
    
    for i in df.index :
        #In case no full_text
        if type(df[ind][i]) == str :
            line = df[ind][i] 
        lines.append(re.sub(r"[^a-zA-Z0-9 ]"," ",line))
        #Get the words for each ind 
        word_list = re.sub(r"[^a-zA-Z0-9 ]"," ",line).split() 
        for word in word_list :
            if word not in columns :
                columns.append(word)
                
                
    #Creation of the vectorization matrix
    mat = pd.DataFrame(index=(lines),columns=(columns))

    for i in columns :
        for j in lines :
            if (i+' ') in j :
                mat[i][j] = 1
            else :
                mat[i][j] = 0
                
    return(mat)



def vectorisation_1(df,ind):
    """
    Processing of the vectorization matrix

    Parameters
    ----------
    df : dataframe
        vectorized data without column preprocessing.
    ind : string : 'Question', 'Long_Answer', 'Contexts' or 'Full_Text' 
        the column to vectorize.

    Returns
    -------
    None.

    """
    #Remove the words <= 3
    for i in df.columns :
        if len(i)<=3 :
            df.pop(i)
      
    #List of number of occurs for each word.       
    list_occ = []
    for j in df.iloc[:,1:] :
        list_occ.append((df[j].sum()))
    
    val_max = np.max(list_occ)
    val_min = np.min(list_occ)
    
    #List of indexes of max and min values
    index_val_min = [indice for indice, valeur in enumerate(list_occ) if valeur==val_min]
    index_val_max = [indice for indice, valeur in enumerate(list_occ) if valeur==val_max]
    
    #List of indexes of columns to delete
    list_del = sorted(index_val_max + index_val_min)
    
    df = df.drop(df.columns[list_del], axis=1)
    
    #Save the matrix in a csv file
    df.to_csv( ind+'.csv', index=True)  
    
    
#Loading the dataset
df = pd.read_csv('ft.csv')

#Vectorization of questions
df1 = vectorisation(df, 'Question')
vectorisation_1(df1, 'Question')


#Vectorization of answers
df2 = vectorisation(df, 'Long_Answer')
df2 = df2.set_index(df['Document_ID'],append=True)
vectorisation_1(df2, 'Long_Answer')


#Vectorization of contexts
df3 = vectorisation(df, 'Contexts')
df3 = df3.set_index(df['Document_ID'],append=True)
vectorisation_1(df3, 'Contexts')


#Vectorization of full_text
df4 = vectorisation(df, 'Full_Text')
df4 = df4.set_index(df['Document_ID'],append=True)
vectorisation_1(df4, 'Full_Text')