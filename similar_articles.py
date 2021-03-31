"""
This script retrieves similar articles (and their DOIs) to PubmedQA dataset
"""

from bs4 import BeautifulSoup
from helpers import load_pubmed_dataset
import pandas as pd
import requests
import re
import time

df = load_pubmed_dataset()
pmids = df['Document_ID'].tolist()

similar_articles = []
i = 1

for pmid in pmids:
    time.sleep(0.5)
    print("Processing PMID : %s" % pmid)
    print("Iteration : %d" % i)

    url = "https://pubmed.ncbi.nlm.nih.gov/%s" % pmid
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Getting similar articles as a HTML list item
    similar_links_elements = soup.select('ul#similar-articles-list.articles-list > li.full-docsum')

    # For each element get the title & pmid & DOI
    for element in similar_links_elements:
        link = element.select('a.docsum-title')[0]
        pmid = link['href']
        pmid = pmid.replace("/", "")
        title = link.text
        title = ' '.join(title.split())
        doi_element = element.select('span.docsum-journal-citation.full-journal-citation')[0]

        try:
            match = re.search(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b', str(doi_element)).group(0)
        except AttributeError:
            match = ''

        similar_articles.append({
            'Document_ID': pmid,
            'Title': title,
            'DOI': match
        })

    i = i + 1

# Export results as a csv
similar_df = pd.DataFrame(similar_articles)
similar_df.to_csv('similar_articles.csv')
