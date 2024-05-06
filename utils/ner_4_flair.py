LOGGER_NAME = 'ner_4_flair.py'

import pandas as pd
from preprocessing_utils import (preprocessing_utils,
                                 NERProcessingUtils)
from file_logger import *
from tqdm import tqdm
tqdm.pandas()

log_file_loc = '/home/azikre/aadil/github/narrativity-fw2/tmp.log'
init_logger(log_file_loc)
add_log_prefix_global("ner_4_flair")

data_dir = "/home/azikre/aadil/github/narrativity-fw2/data"

if __name__ == "__main__":

    filename = f"{data_dir}/processed_data.parquet"

    log_info(f"Reading File :: {filename}")

    df = pd.read_parquet(filename)

    pu = preprocessing_utils(ner_categories = 4, ner_library = 'flair', enable_ner = True)

    res = []
    N_ROWS = df.shape[0]
    for i in range(N_ROWS):
        if i%100 == 0:
            log_info(f"{i}/{N_ROWS} rows done.")
        res.append(pu.flair_ner(df['doc_a'].iloc[i]))

    # df['NER_flair_4'] = df['doc_a'].progress_apply(pu.flair_ner)
    df['NER_flair_4'] = res

    log_info(f"Writing File :: {filename}")
    
    df = df.to_parquet(filename, index=False)