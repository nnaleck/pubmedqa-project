"""
This script retrieves full-text articles from NCBI FTP.
For this script to work properly, an empty "article_files" directory is needed.
"""

from contextlib import closing
from helpers import load_pubmed_dataset
import urllib.request as request
import pubmed_parser as pp
import shutil
import os
import tarfile
import glob
import pandas as pd

# PubMedQA Data loading
df = load_pubmed_dataset()
pmids = df['Document_ID'].tolist()

print('Reading PubMed database...')

oa_file_df = pd.read_csv('oa_file_list.csv')
oa_comm_df = pd.read_csv('oa_comm_use_file_list.csv')

filtered_df = pd.concat(
    [oa_file_df.loc[oa_file_df['PMID'].isin(pmids)], oa_comm_df.loc[oa_comm_df['PMID'].isin(pmids)]]
)

tar_gz_files = []

for ind in filtered_df.index:
    tar_gz_files.append({'PMID': filtered_df['PMID'][ind], 'file': filtered_df['File'][ind]})

# Download tar gz files
print('Downloading files from PubMed database...')
for file in tar_gz_files:
    with closing(request.urlopen('ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/%s' % file['file'])) as r:
        with open('article_files/%s.tar.gz' % file['PMID'], 'wb') as f:
            shutil.copyfileobj(r, f)


# For every tar gz file, extract to "article_files" directory, get to directory and parse .nxml file
print('Extracting archives and parsing nxml files...')
parsed_paragraphs = []
os.chdir('article_files')
for file in tar_gz_files:
    tar = tarfile.open('%s.tar.gz' % file['PMID'])
    tar.extractall()

    dirname = tar.getnames()[0]

    nxml_file = glob.glob('%s/*.nxml' % dirname)[0]
    parsed_file = pp.parse_pubmed_paragraph(nxml_file, all_paragraph=False)

    full_text = []

    for element in parsed_file:
        full_text.append(element['text'])

    parsed_paragraphs.append({'PMID': file['PMID'], 'Full_Text': full_text})

    tar.close()

# Adding a new column to our dataframe and save it as csv
print('Exporting new dataset...')

full_text_column_values = []
for ind in df.index:
    match = next((d for d in parsed_paragraphs if d['PMID'] == df['Document_ID'][ind]), None)

    if match:
        full_text_column_values.append(match['Full_Text'])
    else:
        full_text_column_values.append("No full text")


df['Full_Text'] = full_text_column_values

os.chdir('..')
df.to_csv('fulltext_dataset_ncbi.csv', index=False)

print('Completed.')