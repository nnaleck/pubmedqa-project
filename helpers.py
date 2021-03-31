import pandas as pd


def load_pubmed_dataset():
    df = pd.read_json('https://raw.githubusercontent.com/pubmedqa/pubmedqa/master/data/ori_pqal.json')
    df = df.transpose()
    df = df.drop(columns=['LABELS', 'MESHES', 'YEAR', 'reasoning_required_pred', 'reasoning_free_pred'])
    df = df.reset_index()
    df.rename(
        columns={'index': 'Document_ID', 'QUESTION': 'Question', 'CONTEXTS': 'Contexts', 'LONG_ANSWER': 'Long_Answer'},
        inplace=True)

    return df
