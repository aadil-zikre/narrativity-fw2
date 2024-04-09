import pandas as pd
from preprocessing_utils import (preprocessing_utils,
                                 NERProcessingUtils)
from tqdm import tqdm
tqdm.pandas()

data_dir = ""

if __name__ == "__main__":

    filename = f"{data_dir}/processed_data.parquet"

    print(f"Reading File :: {filename}")

    df = pd.read_parquet(filename, lines=True)

    pu = preprocessing_utils(ner_categories = 18, ner_library = 'flair', enable_ner = True)
    
    df['NER_flair_18'] = df['doc_a'].progress_apply(pu.flair_ner)

    print(f"Writing File :: {filename}")
    
    df = df.to_parquet(filename, lines=True)