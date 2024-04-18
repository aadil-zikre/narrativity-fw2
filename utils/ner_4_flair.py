import pandas as pd
from preprocessing_utils import (preprocessing_utils,
                                 NERProcessingUtils)
from tqdm import tqdm
tqdm.pandas()

data_dir = "/home/azikre/aadil/github/narrativity-fw2/data"

if __name__ == "__main__":

    filename = f"{data_dir}/processed_data.parquet"

    print(f"Reading File :: {filename}")

    df = pd.read_parquet(filename)

    pu = preprocessing_utils(ner_categories = 4, ner_library = 'flair', enable_ner = True)

    df['NER_flair_4'] = df['doc_a'].progress_apply(pu.flair_ner)

    print(f"Writing File :: {filename}")
    
    df = df.to_parquet(filename, index=False)