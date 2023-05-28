import string
import re
import os
import time

from loguru import logger
from pathlib import Path
import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

try:
    import spacy
    nlp = spacy.load('ru_core_news_sm')
except:
    os.system('python -m spacy download ru_core_news_sm')
    import spacy
    nlp = spacy.load('ru_core_news_sm')

lst_stopwords = nltk.corpus.stopwords.words('russian')
lst_stopwords.extend(['…', '«', '»', '...'])

def clean_text(text, tokenizer, stopwords):

    text = str(text).lower()  
    text = re.sub(r"\[(.*?)\]", "", text)  
    text = re.sub(r"\s+", " ", text)  
    text = re.sub(r"\w+…|…", "", text)  
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)  
    text = re.sub(r"[0-9]", "", text)
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", "", text
    )  

    tokens = tokenizer(text)  
    tokens = [t for t in tokens if not t in lst_stopwords]  
    tokens = ["" if t.isdigit() else t for t in tokens]  
    tokens = [t for t in tokens if len(t) > 1] 
    return tokens

def prep_tokens(df_raw):
    text_columns = ["Комментарий"]
    df_raw["text"] = df_raw[text_columns].apply(lambda x: " | ".join(x), axis=1)
    df_raw["tokens"] = df_raw["text"].map(lambda x: clean_text(x, word_tokenize, lst_stopwords))
    _, idx = np.unique(df_raw["tokens"], return_index=True)
    df_raw = df_raw.iloc[idx, :]

    # Remove empty values
    df_raw = df_raw.loc[df_raw.tokens.map(lambda x: len(x) > 0), ["text", "tokens"]]
    return df_raw

def vectorize(list_of_docs, model):
    features = []

    for tokens in list_of_docs:
        zero_vector = np.zeros(model.vector_size)
        vectors = []
        for token in tokens:
            if token in model.wv:
                try:
                    vectors.append(model.wv[token])
                except KeyError:
                    continue
        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            features.append(avg_vec)
        else:
            features.append(zero_vector)
    return features

def get_lable(some_text, word2vec):
    doc = nlp(some_text[0])
    time_slov={}
    for ent in doc.ents:
        time_slov[f'{ent.label_}']=ent.text
    exper=pd.DataFrame(some_text,columns=['Комментарий'])
    vectorized_dox=vectorize(prep_tokens(exper).iloc[:,1], model=word2vec)
    return vectorized_dox, time_slov

def MiniBatch(text, word2vec, minibatchkmeans):
    dox, time_slov = get_lable([text], word2vec)
    try:
        result = minibatchkmeans.predict(dox)
        return result
    except Exception as e:
        logger.error(e)
        time.sleep(0.5)
        return [999]