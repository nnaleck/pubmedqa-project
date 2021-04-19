"""
This script converts our dataset in order to build an SQLite
database using DrQA's build_db.py script.
"""

import pandas as pd

# Reorganizing dataset
df = pd.read_csv('fulltext_dataset_pdf.csv')
df = df[df["Full_Text"].notna()]  # Removing observations with no full text
df = df.drop(columns=["Question", "Long_Answer", "final_decision", "Contexts"])
df = df.reset_index()
df = df.rename(columns={
    'Full_Text': 'text',
    'Document_ID': 'id'
})
df = df.drop(columns=["index"])

df["text"] = df["text"].apply(
    lambda s: str(s).replace('"', '')
)

df["id"] = df["id"].astype(str)  # Casting id as string

# Generating one json file per document
for i in df.index:
    df.loc[i].to_json("documents/doc{}.json".format(i))
