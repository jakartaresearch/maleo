import re
import pickle
import unicodedata
import pandas as pd
import pkg_resources

from bs4 import BeautifulSoup
from maleo.stopword_remover.RemoverFactory import RemoverFactory


def remove_multiple_space(series: pd.Series) -> pd.Series:
    series = series.replace(regex=r'\s\s+', value=' ')
    return series


def remove_link(series: pd.Series) -> pd.Series:
    series = series.replace(regex=r'http\S+', value='')
    series = series.replace(regex=r'pic.twitter.com\S+', value='')
    return series


def remove_punctuation(series: pd.Series) -> pd.Series:
    punctuation_pattern = r"[\s{}]".format(
        re.escape('!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'))
    series = series.replace(regex=punctuation_pattern, value=' ')
    return series


def remove_char(series: pd.Series) -> pd.Series:
    # remove single char
    series = series.replace(regex=r'\s[^uUgGbB0-9]\s', value=' ')
    # remove consecutive repeating char
    series = series.replace(regex=r'([^gG0-9])\1+', value=r'\1')
    return series


def remove_html(series: pd.Series) -> pd.Series:
    new_series = []
    for text in series:
        new_text = BeautifulSoup(text, "html.parser")
        new_series.append(new_text.get_text())
    return pd.Series(new_series)


def remove_non_ascii(series: pd.Series) -> pd.Series:
    new_series = []
    for text in series:
        new_text = unicodedata.normalize('NFKD', text).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_series.append(new_text)
    return pd.Series(new_series)


def remove_stopword(series: pd.Series) -> pd.Series:
    factory = RemoverFactory()
    stopword = factory.create_stop_word_remover()

    result = series.copy()
    for idx, row in series.items():
        result.iloc[idx, :] = stopword.remove(row)
    return result


def remove_emoticons(series: pd.Series) -> pd.Series:
    emoticon_dict_path = pkg_resources.resource_filename('maleo',
                                                         'cleansing/Emoticon_Dict.p')
    with open(emoticon_dict_path, 'rb') as file:
        emoticon_dict = pickle.load(file)
    emoticon_pattern = re.compile(
        u'(' + u'|'.join(k for k in emoticon_dict) + u')')
    result = series.replace(regex=emoticon_pattern, value=r'')
    return result
