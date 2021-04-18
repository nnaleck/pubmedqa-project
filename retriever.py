import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search(tfidf_matrix, model, query, top_documents=5):
    query_transform = model.transform([query])
    similarity = cosine_similarity(query_transform, tfidf_matrix)[0]
    indexes = np.argsort(similarity)[-top_documents:][::-1]

    results = []

    for i in indexes:
        results.append({
            'index': i,
            'similarity': similarity[i]
        })

    return results


def print_result(query, results, df):
    print('\nSearch : ' + query)
    print('\nBest Results :')
    for result in results:
        print('Index = {0:5d} - Cos similarity = {1:5f} - Question = {2}'.format(
            result['index'], result['similarity'], df['Question'].loc[result['index']]
        ))


df = pd.read_csv("fulltext_dataset_pdf.csv")
df = df[df["Full_Text"].notna()]
df = df.reset_index()

text_content = df["Full_Text"]
vector = TfidfVectorizer(
    max_df=0.4,
    stop_words='english',
    lowercase=True,
    use_idf=True,
    norm=u'l2',
    smooth_idf=True
)

tfidf = vector.fit_transform(text_content)

query = "Is Breast cancer dangerous"
result = search(tfidf, vector, query)
print_result(query, result, df)
