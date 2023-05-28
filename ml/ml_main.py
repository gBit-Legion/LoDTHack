import re
import nltk
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score

from pkg_dataset_preprocessor.m_dataset_preprocessor import preprocessing_text

import string
lst_stopwords = nltk.corpus.stopwords.words('russian')
lst_stopwords.extend(['…', '«', '»', '...'])

def import_file(file_path):
    df_raw = pd.read_excel(file_path)
    df_raw.dropna(inplace=True)
    df_raw.rename(columns={'text': 'content'}, inplace=True)
    return df_raw

df_raw=import_file(r"../ml/Московский постамат_Дата-cет_Этап 1.xlsx",)

preprocessing_text(df_raw)