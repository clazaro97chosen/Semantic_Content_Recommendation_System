from flask import render_template, request
from dtale.views import startup
from dtale.app import build_app, get_instance
from dtale.global_state import cleanup
import pandas as pd
from app import app
from app.forms import SearchForm
from sentence_transformers import SentenceTransformer, util
import torch
#from config import corpus_embeddings
import dtale.global_state as global_state

global_state.set_app_settings(dict(max_column_width=100))


def load_data_props():
    instance = get_instance("1")

    if instance is not None:
        return dict(data_exists=True)
    return dict(data_exists=False)

def find_n_similar_listings(search_query, top_n_results):
    """
    Finds the top_n_results that are  most similar to the users title/text search_query
    using cosine similarity of text/title text embeddings of the contract data. 
    
    Embeddings are created by 'distiluse-base-multilingual-cased-v1'
    which comes from the library Sentence-Transformers which  supports 15 languages among which are:
    Chinese, Dutch, English, French, German, Korean, Portuguese, Russian, Spanish. 

    To do:
        change return_n_listings argument to a dynamic value that is gathered through the SearchForm

    Args:
        search_query : users text/title query, which they desired to find similar listings to in their data
        return_n_listings: users desired number of listings they want to see are similar to their search query


    Returns:
        A dataframe of length - top_n_results -, which contains listings from the contract_data that are most 
        similar to the users search query
    """
    #test version

    return app.config["DATA_FILE"].loc[app.config["DATA_FILE"]["product_name"].str.contains(f"{search_query}"),:].copy()

#create function to allow users to pick their text columns that define and embedding.
# def pick_columns_for_embedding(df_columns, )

def update_dtale_data(similar_listings):
    curr_data = get_instance("1")
    if curr_data is not None:
        cleanup("1")
    startup(data_id="1",data=similar_listings)

@app.route("/")
def base():
    form = SearchForm()
    return render_template("index.html", form=form, **load_data_props())

@app.route("/load-listings", methods=["POST"])
def load_listings():
    form = SearchForm()
    if form.validate_on_submit():
        similar_listings = find_n_similar_listings(form.search_query.data,
                                                   app.config["TOP_N_RESULTS"]) 
        update_dtale_data(similar_listings)
        return render_template("index.html", form=form, search_query=form.search_query.data,
                                **load_data_props())
    return render_template("index.html",**load_data_props())