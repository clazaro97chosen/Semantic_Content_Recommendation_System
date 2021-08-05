import os
import pandas as pd
#from create_corpus_embedding import corpus_embeddings
from sentence_transformers import SentenceTransformer

basedir = os.path.abspath(
    os.path.dirname(__file__)
) 

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TOP_N_RESULTS = 50
    DATA_FILE = pd.read_csv("./data/furniture_shipment.csv").dropna(how="all", inplace=False).fillna("")
    #EMBEDDER = SentenceTransformer('distiluse-base-multilingual-cased-v1')
