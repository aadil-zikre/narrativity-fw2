LOGGER_NAME = "taaco_features.py"

import pandas as pd
from TAACOnoGUI import runTAACO
from subprocessing_utils import cmd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from file_logger import *
import matplotlib.pyplot as plt

temp_dir = "/home/azikre/aadil/github/narrativity-fw2/temp"
data_dir = "/home/azikre/aadil/github/narrativity-fw2/data"
filename = f"{data_dir}/processed_data.parquet"

log_file_loc = '/home/azikre/aadil/github/narrativity-fw2/tmp.log'
init_logger(log_file_loc)

class TAACO_utils:
    def __init__(self):
        log_info("init TAACO utils")
        
    def save_df_rows(self,df, id_col, text_col):
        cmd(f"rm {temp_dir}/airbnb_reviews/*.txt")
        for row in df.itertuples():
            with open(f"{temp_dir}/airbnb_reviews/review_{getattr(row, id_col)}.txt", mode = 'w') as fp:
                fp.write(getattr(row, text_col))
                
    def run_TAACO(self, sampleVars=None, save_as="runTaaco_no_name.csv"):
        if not sampleVars: 
            raise NotImplementedError("Pass SampleVars. Default not defined.")
        
        runTAACO(f"{temp_dir}/airbnb_reviews/", f"{temp_dir}/{save_as}", sampleVars)
        log_info(f"TAACO finished Running. Results saved at: {temp_dir}/{save_as}")

if __name__ == "__main__":

    df = pd.read_parquet(filename)

    tu = TAACO_utils()
    tu.save_df_rows(df, 'review_id', 'doc_a')

    sampleVars = {'sourceKeyOverlap': False,
    'sourceLSA': False,
    'sourceLDA': False,
    'sourceWord2vec': False,
    'wordsAll': True,
    'wordsContent': True,
    'wordsFunction': True,
    'wordsNoun': True,
    'wordsPronoun': True,
    'wordsArgument': True,
    'wordsVerb': True,
    'wordsAdjective': True,
    'wordsAdverb': True,
    'overlapSentence': True, # Calculate sentence to sentence overlap
    'overlapParagraph': False,
    'overlapAdjacent': True, # Calculate overlap for adjacent sections (sentences or paragraphs)
    'overlapAdjacent2': True,
    'otherTTR': False,
    'otherConnectives': True, # Calculate connective indicidence indices
    'otherGivenness': True, # Calculate givenness indices
    'overlapLSA': True,
    'overlapLDA': True,
    'overlapWord2vec': True,
    'overlapSynonym': True,
    'overlapNgrams': True,
    'outputTagged': False,
    'outputDiagnostic': False}

    # Run TAACO on a folder of texts ("ELLIPSE_Sample/"), give the output file a name ("packageTest.csv), provide output for particular indices/options (as defined in sampleVars)
    # tu.run_TAACO(sampleVars)

    df_taaco_res = pd.read_csv(f"{temp_dir}/runTaaco_no_name.csv")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_taaco_res.iloc[:,1:])

    # Create a PCA object with all components
    pca_all = PCA()

    # Fit the PCA model to the scaled data
    pca_all.fit(X_scaled)

    # Get the explained variance ratio for each component
    explained_variance_ratio = pca_all.explained_variance_ratio_

    # Prompt the user to enter the desired number of components
    n_components = 10

    # Create a PCA object with the specified number of components
    pca = PCA(n_components=n_components)

    # Fit the PCA model to the scaled data
    pca.fit(X_scaled)

    # Get the principal components (eigenvectors)
    principal_components = pca.components_

    # Transform the data to obtain the transformed PCA vectors
    transformed_data = pca.transform(X_scaled)

    # Create a new DataFrame with the transformed PCA vectors
    pca_df = pd.DataFrame(data=transformed_data, columns=[f'cohesion_pc{i+1}' for i in range(n_components)])

    pca_df.insert(0, 'review_id', df_taaco_res['Filename'])

    try:
        pca_df['review_id'] = pca_df.review_id.apply(lambda x : int(x.split(".")[0].split("_")[1]))
    except:
        pca_df['review_id'] = pca_df.review_id.apply(lambda x : "_".join(x.split(".")[0].split("_")[1:])) 

    df = df.merge(pca_df, on='review_id', how='left', copy=False)

    df.to_parquet(filename)