import os
import re
import string
import pandas as pd
import unicodedata

from bs4 import BeautifulSoup
from maleo.stopword_remover.RemoverFactory import RemoverFactory


def remove(series):
    #series = remove_html(series)
    series = remove_link(series)
    series = remove_punctuation(series)
    series = remove_char(series)
    
    # remove multiple whitespaces
    series = series.replace(regex=r'\s\s+', value=' ')
    series = series.str.strip()
    series = remove_non_ascii(series)
    series = remove_stopword(series)
    
    return series


def remove_link(series):
    series = series.replace(regex=r'http\S+', value='')
    series = series.replace(regex=r'pic.twitter.com\S+', value='')
    return series


def remove_punctuation(series):
    punctuation_pattern = r"[\s{}]".format(re.escape('!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'))
    series = series.replace(regex=punctuation_pattern, value=' ')
    return series


def remove_char(series):
    # remove single char
    series = series.replace(regex=r'\s[^uUgGbB0-9]\s', value=' ')
    # remove consecutive repeating char
    series = series.replace(regex=r'([^gG])\1+', value=r'\1')
    return series


def remove_html(series):
    new_series = []
    for text in series:
        new_text = BeautifulSoup(text, "html.parser")
        new_series.append(new_text.get_text())
    return pd.Series(new_series)


def remove_non_ascii(series):
    new_series = []
    for text in series:
        new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_series.append(new_text)
    return pd.Series(new_series)


def remove_stopword(series):
    factory = RemoverFactory()
    stopword = factory.create_stop_word_remover()

    result = series.copy()
    for idx, row in series.items():
        result.iloc[idx,:] = stopword.remove(row)
    return result