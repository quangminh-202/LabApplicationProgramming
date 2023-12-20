import csv
import re
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
from annotation import Annotation
from create_annotation import create_annotation as crt
from typing import List, Dict, Tuple
from collections import Counter
from nltk.corpus import stopwords
from pymystem3 import Mystem
from pymorphy3 import MorphAnalyzer

stopwords_ru = set(stopwords.words('russian'))
patterns = re.compile(
    r'\.|\,|\!|\?|\;|\:|\(|\)|\&|\=|\<|\>|\[|\]|\{|\}|\~|\`|\"|\'|'
    r'\/|\\|\||\-'
)
morph = MorphAnalyzer()

def read_csv_to_dataframe(csv_path: str) -> pd.DataFrame:
    try:
        df_csv = pd.read_csv(csv_path)
        texts = []

        for absolute_path, label in zip(df_csv['Absolute Path'], df_csv['Label']):
            with open(absolute_path, 'r', encoding='utf-8') as file:
                text = file.read()
                texts.append((label, text))

        df_result = pd.DataFrame(texts, columns=['num', 'text'])
        return df_result
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_none(df: pd.DataFrame) -> pd.DataFrame:
    print(df.isnull().sum())
    df.dropna()
    return df

def text_update(text: str) -> List[str]:
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()

def word_count(df: pd.DataFrame) -> pd.DataFrame:
    df['word_count'] = df['text'].apply(lambda x: len(text_update(x)))
    return df

def group_and_mean_word_count(df: pd.DataFrame) -> pd.DataFrame:
    return df[["num", "word_count"]].groupby("num").mean()

def filter_by_word(df: pd.DataFrame, max_count: int) -> pd.DataFrame:
    return df.loc[df['word_count'] <= max_count]

def filter_by_rating(df: pd.DataFrame, num: str) -> pd.DataFrame:
    return df.loc[df['num'] == num]

def group_and_calculator_min_max_mean(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('num').agg({'word_count': ['min', 'max', 'mean']})

def lemmatize(review: str) -> List[str]:
    review = re.sub(patterns, ' ', review)
    tokens = nltk.word_tokenize(review.lower())
    preprocessed_text = []
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        if lemma not in stopwords_ru:
            preprocessed_text.append(lemma)
    return preprocessed_text

def most_popular_words(df: pd.DataFrame, rating: int) -> List[tuple[str, int]]:
    words = df[df['num'] == rating]['text'].apply(lemmatize)
    count = Counter()
    for word in words:
        count.update(word)
    return count.most_common(20)

def graph_build(list_words: List[tuple[str, int]]) -> None:
    words, count = [], []
    for i in range(len(list_words)):
        words.append(list_words[i][0])
        count.append(list_words[i][1])
    figure, axes = plt.subplots()
    axes.barh(words, count)
    axes.set_xlabel('Количество')
    axes.set_title('Гистограмма самых популярных слов')
    plt.show()

if __name__ == "__main__":
    csv_path = "file_csv.csv"
    df = read_csv_to_dataframe(csv_path)
    # if df_result is not None:
    #     print("DataFrame created successfully:")
    #     print(df_result.head())
    # word_count(df)
    # print(df)
    # print(group_and_mean_word_count(df))
    # print(filter_by_word(df, 100))
    # print(group_and_calculator_min_max_mean(df))
    graph_build(most_popular_words(df, 3))
