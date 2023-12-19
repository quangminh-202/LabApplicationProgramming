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

mystem = Mystem()
russian_stopwords = stopwords.words("russian")


def read_csv(path: str) -> pd.DataFrame:
    num_list, text_list = [], []
    items = list(csv.reader(open('file_csv.csv', 'r')))
    for item in items:
        with open(item[0], 'r', encoding='utf-8') as f:
            text = f.read()
            num_list.append(item[2])
            text_list.append(text)
    d = {'num': num_list, 'text': text_list}
    df1 = pd.DataFrame(data=d)
    df1 = df1.dropna()
    return df1

def text_update(text: str) -> List[str]:
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()

def count_word(df: pd.DataFrame) -> None:
    df['word_count'] = df['text'].apply(lambda x: len(text_update(x)))

def group_and_mean_word_count(df: pd.DataFrame) -> pd.DataFrame:
    return df[["num", "word_count"]].groupby("num").mean()

def filter_by_word(df: pd.DataFrame, max_count: int) -> pd.DataFrame:
    return df.loc[df['word_count'] <= max_count]

def filter_by_rating(df: pd.DataFrame, num: str) -> pd.DataFrame:
    return df.loc[df['num'] == num]

def preprocess_text(text: str) -> List[str]:
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords]
    text = " ".join(tokens)
    return tokens

def preprocess_text_only_A(text: str) -> List[str]:
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords]
    text = " ".join(tokens)
    words = nltk.word_tokenize(text)
    functors_pos = {'A=m', 'ADV'}
    res = [word for word, pos in nltk.pos_tag(words, lang='rus')
           if pos in functors_pos]
    return res


def group_by_num(df: pd.DataFrame) -> pd.DataFrame:
    num, max, min, mean = [], [], [], []
    groupped_d = {'num': num, 'max': max, 'min': min, 'mean': mean}
    for i in range(1, 6):
        num.append(str(i))
        max.append((df.loc[df['num'] == str(i)]
                   [['word_count']].max()).loc['word_count'])
        min.append((df.loc[df['num'] == str(i)]
                   [['word_count']].min()).loc['word_count'])
        mean.append((df.loc[df['num'] == str(i)]
                    [['word_count']].mean()).loc['word_count'])
    groupped_df = pd.DataFrame(data=groupped_d)
    return groupped_df


def make_histogram(df: pd.DataFrame, num: str) -> Dict[str, int]:
    result = []
    length = len(df.loc[df['num'] == num]['text'])
    for i in range(length):
        text = df.loc[df['num'] == num]['text'].iloc[i]
        text = preprocess_text_only_A(text)
        result += text
        print(i)
    result = dict(Counter(result))
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    result = result[0:10]
    return result


def graph_build(hist_list: Dict[str, int]) -> None:
    words, count = [], []
    for i in range(len(hist_list)):
        words.append(hist_list[i][0])
        count.append(hist_list[i][1])
    fig, ax = plt.subplots()
    y_pos = np.arange(len(words))
    ax.barh(y_pos, count, align='center')
    ax.set_yticks(y_pos, labels=words)
    ax.invert_yaxis()
    ax.set_xlabel('Word count')
    ax.set_title('The most popular words')
    plt.show()

if __name__ == "__main__":
    df = read_csv('file_csv.csv')
    # count_word(df)
    print('----')
    print(df)
    print('----')
    # print(group_and_mean_word_count(df))
    # print(filter_by_word(df, 100))
    # print(filter_by_rating(df, '5'))
    # print(preprocess_text(''))
    # print(group_by_num(df))
    # hist = make_histogram(df, "2")
    # graph_build(hist)
    #
    # df = pd.read_csv('full_data.csv')
    # df = df.drop(df.columns[[0]], axis = 1)
    # df = df.dropna()
    # print(df)
    # for i in range(5000):
    #     text = re.sub(r"[^\w\s]", "", df.iloc[i,1])
    #     tokens = mystem.lemmatize(text.lower())
    #     tokens = [token for token in tokens if token not in russian_stopwords]
    #     text = " ".join(tokens)
    #     words = nltk.word_tokenize(text)
    #     functors_pos = {'A=m', 'ADV'}
    #     res = [word for word, pos in nltk.pos_tag(words, lang='rus')
    #        if pos in functors_pos]
    #     res_text = " ".join(res)
    #     print(res_text)
    #     df.iloc[i,1] = res_text
    #     print(i)
    # print(df)
    # df.to_csv('full_data_lemm_A.csv')