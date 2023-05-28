import re
import nltk
import numpy as np
from gensim.models import Word2Vec
from collections import Counter
from nltk import word_tokenize
import string

lst_stopwords = nltk.corpus.stopwords.words('russian')
lst_stopwords.extend(['…', '«', '»', '...'])

class DatasetPreprocessor():
    def clean_text(self, text, tokenizer, stopwords):
        text = str(text).lower()
        text = re.sub(r"\[(.*?)\]", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\w+…|…", "", text)
        text = re.sub(r"(?<=\w)-(?=\w)", " ", text)
        text = re.sub(
            f"[{re.escape(string.punctuation)}]", "", text
        )

        tokens = tokenizer(text)
        tokens = [t for t in tokens if not t in lst_stopwords]
        tokens = ["" if t.isdigit() else t for t in tokens]
        tokens = [t for t in tokens if len(t) > 1]
        return tokens

    def prep_tokens(self, df_raw):
        dataset_preprocessor = DatasetPreprocessor()
        text_columns = ["Комментарий"]
        # df_raw['content'] = df_raw['content'].fillna(" ")
        # for col in text_columns:
        #     df_raw[col] = df_raw[col].astype(str)
        # создаем текст основанный на content title и tag
        df_raw["text"] = df_raw[text_columns].apply(lambda x: " | ".join(x), axis=1)
        df_raw["tokens"] = df_raw["text"].map(lambda x: dataset_preprocessor.clean_text(x, word_tokenize, lst_stopwords))
        _, idx = np.unique(df_raw["tokens"], return_index=True)
        df_raw = df_raw.iloc[idx, :]

        # Remove empty values
        df_raw = df_raw.loc[df_raw.tokens.map(lambda x: len(x) > 0), ["text", "tokens"]]
        return df_raw

    def vectorize(self, list_of_docs, model):
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

def preprocessing_text(df_raw):
    dataset_preprocessor = DatasetPreprocessor()

    prep_data = dataset_preprocessor.prep_tokens(df_raw)
    docs = prep_data["text"].values
    tokenized_docs = prep_data["tokens"].values
    vocab = Counter()
    for token in tokenized_docs:
        vocab.update(token)

    model = Word2Vec(sentences=prep_data['tokens'].values, vector_size=100, window=5, min_count=1, workers=4)

    vectorized_docs = dataset_preprocessor.vectorize(prep_data['tokens'], model=model)
    len(vectorized_docs), len(vectorized_docs[0])

    prep_data['vectors'] = vectorized_docs
    prep_data.fillna('')

    return prep_data