"""
This script :
- Retrieves full-text articles from local PDF files.
- Removes citations, references, links, \n... from full text.

In order to work, this script needs :
- A "pdfs" directory containing pdf files of articles. Filenames are the articles title.
"""

from os import listdir
from os.path import isfile, join
from helpers import load_pubmed_dataset
from fitz import *
import re
import string

df = load_pubmed_dataset()

pdf_files = [f for f in listdir('pdfs') if isfile(join('pdfs', f))]

occurrences = []

for ind in df.index:
    first_words = df['Question'][ind].split()[:4]
    first_words = ' '.join(first_words)

    has_pdf_file = any(first_words.lower() in pdf.lower() for pdf in pdf_files)
    pdf_file = next((pdf for pdf in pdf_files if first_words.lower() in pdf.lower()), None)

    occurrences.append({
        'pmid': df['Document_ID'][ind],
        'has_pdf_file': has_pdf_file,
        'pdf_file': pdf_file
    })

full_text_column_values = []

for ind in df.index:
    match = next((d for d in occurrences if d['pmid'] == df['Document_ID'][ind]), None)

    print(match['has_pdf_file'])
    if match['has_pdf_file']:
        doc = fitz.Document("pdfs/" + match['pdf_file'])

        text = ''
        for page in doc:
            text += page.getText()

        full_text_column_values.append(text)
        doc.close()
    else:
        full_text_column_values.append("/")

df['Full_Text'] = full_text_column_values

# Removing citations
df["Full_Text"] = df["Full_Text"].apply(
    lambda s: re.sub('\[([0-9\-]+\,? *)+]', '', str(s).strip())
)  # [1] or [1-2, 1]
df["Full_Text"] = df["Full_Text"].apply(
    lambda s: re.sub(r"\s\([A-Z][a-z]+,\s[A-Z][a-z]?\.[^\)]*,\s\d{4}\)", '', str(s))
)  # (F. Last name YYYY)

# Removing links
df["Full_Text"] = df["Full_Text"].apply(
    lambda s: re.sub(r'https?:\/\/.*[\r\n]*', '', str(s))
)  # http[s]://link.com/sub/folders

# Removing punctuation and newlines \n
df["Full_Text"] = df["Full_Text"].apply(
    lambda s: str(s).replace("\n", " ").translate(str.maketrans('', '', string.punctuation))
)

# Removing useless parts of the text (list of references)
df["Full_Text"] = df["Full_Text"].apply(lambda s: str(s).lower().split('references', 1)[0])

df.to_csv('fulltext_dataset_pdf.csv', index=False)
