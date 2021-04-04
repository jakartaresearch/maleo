import re
import pickle
import unicodedata
import pandas as pd
import pkg_resources

from bs4 import BeautifulSoup
from maleo.stopword_remover.RemoverFactory import RemoverFactory


__all__ = ["rm_multiple_space", "rm_link", "rm_punc", "rm_char",
           "rm_html", "rm_non_ascii", "rm_stopword", "rm_emoticon"]


def rm_multiple_space(text: pd.Series) -> pd.Series:
    """
    Remove multiple space between word in text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data.
    Returns
    -------
    clean_text : pd.Series
        Text with only single space between word.
    """
    clean_text = text.replace(regex=r'\s\s+', value=' ')
    return clean_text


def rm_link(text: pd.Series) -> pd.Series:
    """
    Remove hyperlink from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data.
    Returns
    -------
    clean_text : pd.Series
        Text without general and twitter hyperlink.
    """
    clean_text = text.replace(regex=r'http\S+', value='')
    clean_text = clean_text.replace(regex=r'pic.twitter.com\S+', value='')
    return clean_text


def rm_punc(text: pd.Series) -> pd.Series:
    """
    Remove punctuations from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data.
    Returns
    -------
    clean_text : pd.Series
        Text without punctuations.
    """
    punctuation_pattern = r"[\s{}]".format(
        re.escape('!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'))
    clean_text = text.replace(regex=punctuation_pattern, value=' ')
    return clean_text


def rm_char(series: pd.Series) -> pd.Series:
    # remove single char
    series = series.replace(regex=r'\s[^uUgGbB0-9]\s', value=' ')
    # remove consecutive repeating char
    series = series.replace(regex=r'([^gG0-9])\1+', value=r'\1')
    return series


def rm_html(series: pd.Series) -> pd.Series:
    new_series = []
    for text in series:
        new_text = BeautifulSoup(text, "html.parser")
        new_series.append(new_text.get_text())
    return pd.Series(new_series)


def rm_non_ascii(series: pd.Series) -> pd.Series:
    new_series = []
    for text in series:
        new_text = unicodedata.normalize('NFKD', text).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_series.append(new_text)
    return pd.Series(new_series)


def rm_stopword(series: pd.Series) -> pd.Series:
    factory = RemoverFactory()
    stopword = factory.create_stop_word_remover()

    result = series.copy()
    for idx, row in series.items():
        result.iloc[idx, :] = stopword.remove(row)
    return result


def rm_emoticon(series: pd.Series) -> pd.Series:
    emoticon_dict_path = pkg_resources.resource_filename('maleo',
                                                         'cleansing/Emoticon_Dict.p')
    with open(emoticon_dict_path, 'rb') as file:
        emoticon_dict = pickle.load(file)
    emoticon_pattern = re.compile(
        u'(' + u'|'.join(k for k in emoticon_dict) + u')')
    result = series.replace(regex=emoticon_pattern, value=r'')
    return result
