GLOBAL_SEED = 1000
data_dir = "/home/azikre/aadil/github/narrativity-fw2/data"
python_venv_dir = "/home/azikre/aadil/venvs/season4"
cohesion_model_venv_path = "/home/azikre/aadil/github/Transformer-Models-for-Text-Coherence-Assessment/.venv"
filename = f"{data_dir}/processed_data.parquet"
input_filename = f"{data_dir}/input_data.parquet"

import pandas as pd
import numpy as np
import os
import pickle
import stanza 
stanza.download('en')


from utils.preprocessing_utils import (preprocessing_utils,
                                       NERProcessingUtils)
import utils.multiprocessing_utils
from utils.subprocessing_utils import cmd
from utils.spacy_utils import TextStats
from utils.connectives_utils import Connectives

log_info = print


if __name__ == "__main__":
    """
    run gold score predictor here
    """

    df = pd.read_parquet(input_filename)

    file_for_inference_path = "/home/azikre/aadil/github/Transformer-Models-for-Text-Coherence-Assessment/processed_data/AIRBNB"

    df.to_json(f"{file_for_inference_path}/S4_test.jsonl", orient='records', lines=True)

    main_filepath = "/home/azikre/aadil/github/Transformer-Models-for-Text-Coherence-Assessment"

    cmd(f"""
    {cohesion_model_venv_path}/bin/python {main_filepath}/main.py --inference --arch 'vanilla' --epochs 10 --gpus 2 --corpus 'airbnb' --freeze_emb_layer --online_mode 0 --task sentence-score-prediction --checkpoint_path "/home/azikre/aadil/github/Transformer-Models-for-Text-Coherence-Assessment/lightning_checkpoints/gcdc-All-vanilla-sentence-score-prediction-roberta-base/epoch=9-step=16000.ckpt"
    """)

    with open("/home/azikre/aadil/github/Transformer-Models-for-Text-Coherence-Assessment/dataset_processor/predictions/predictions.pkl", mode='rb') as fp:
        gold_score_predictions = pickle.load(fp)

    predictions = np.concatenate([i['preds'].numpy() for i in gold_score_predictions]).ravel()

    df["cohesion_score_roberta"] = predictions

    df['cohesion_score_roberta'] = df['cohesion_score_roberta'] / 3

    df = df.to_parquet(filename, index=False)

    df = pd.read_parquet(filename)

    pu = preprocessing_utils()

    df['review_length'] = df['doc_a'].multicore_apply_by_chunks(pu.calculate_word_length, 8, 16)

    df.to_parquet(filename, index=False)

    cmd(f"{python_venv_dir}/bin/python utils/ner_4_flair.py")

    cmd(f"{python_venv_dir}/bin/python utils/ner_18_flair.py")

    df = pd.read_parquet(filename)

    ts = TextStats()

    df['count_adjectives'] = df['doc_a'].progress_apply(ts.count_adjectives)
    df['count_adverbs'] = df['doc_a'].progress_apply(ts.count_adverbs)

    temporal_conn = Connectives('temporal')
    causal_conn = Connectives('causal')
    interclausal_conn = Connectives('interclausal')

    df['count_temporal_connectives'] = df['doc_a'].progress_apply(temporal_conn.findall_connectives)
    df['count_causal_connectives'] = df['doc_a'].progress_apply(causal_conn.findall_connectives)
    df['count_interclausal_connectives'] = df['doc_a'].progress_apply(interclausal_conn.findall_connectives)

    df['count_unique_attributes'] = df['doc_a'].progress_apply(ts.count_unique_attributes) # Point 4.5
    df['count_unique_activites'] = df['doc_a'].progress_apply(ts.count_unique_activites) # Point 4.3

    ner_pu = NERProcessingUtils()

    df['extract_unique_loc_ner'] = df['NER_flair_4'].progress_apply(ner_pu.extract_unique_loc_ner) # Point 4.1
    df['extract_unique_per_ner'] = df['NER_flair_4'].progress_apply(ner_pu.extract_unique_per_ner) # Point 4.2

    df['extract_unique_prod_ner'] = df['NER_flair_18'].progress_apply(ner_pu.extract_unique_prod_ner)

    df['count_unique_locations'] = df['extract_unique_loc_ner'].progress_apply(len)
    df['count_unique_persons'] = df['extract_unique_per_ner'].progress_apply(len)
    df['count_unique_products'] = df['extract_unique_prod_ner'].progress_apply(len)

    df['extract_all_where_ner'] = df['NER_flair_4'].progress_apply(ner_pu.extract_all_where_ner) # Point 7
    df['extract_all_when_ner'] = df['NER_flair_18'].progress_apply(ner_pu.extract_all_when_ner) # Point 7

    df['count_all_where_ner'] = df['extract_all_where_ner'].progress_apply(len)
    df['count_all_when_ner'] = df['extract_all_when_ner'].progress_apply(len)

    nlp = stanza.Pipeline('en', processors = "tokenize,mwt,pos,lemma,depparse" )

    def count_n_subj(sentence):
        doc = nlp(sentence)
        sent_dict = doc.sentences[0].to_dict()
        ct_n_subj = 0 
        for word in sent_dict:
    #         print(word)
            if str(word.get('deprel', 'None')) == 'nsubj':
                ct_n_subj += 1
        return ct_n_subj

    df['count_sub_predicates'] = df['doc_a'].progress_apply(count_n_subj)

    df.to_parquet(filename, index=False)

    cmd(f"cd TAACO/ && python taaco_features.py && cd ..")
