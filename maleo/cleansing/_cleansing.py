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
    """Remove multiple space between word in text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text with only single space between word
    """
    clean_text = text.replace(regex=r'\s\s+', value=' ')
    return clean_text


def rm_link(text: pd.Series) -> pd.Series:
    """Remove general and twitter hyperlink from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without general and twitter hyperlink
    """
    clean_text = text.replace(regex=r'http\S+', value='')
    clean_text = clean_text.replace(regex=r'pic.twitter.com\S+', value='')
    return clean_text


def rm_punc(text: pd.Series) -> pd.Series:
    """Remove punctuations from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without punctuations
    """
    punctuation_pattern = r"[\s{}]".format(
        re.escape('!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'))
    clean_text = text.replace(regex=punctuation_pattern, value=' ')
    return clean_text


def rm_char(text: pd.Series) -> pd.Series:
    """Remove single character and consecutive repeating character from text.
    
    Exclude single char {u, g, b, 0-9}.
    
    Exclude consecutive repeating char {g, 0-9}.
    
    Indonesian case : [u g makan?, menggunakan].
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without single and consecutive repeating char
    """
    clean_text = text.replace(regex=r'\s[^uUgGbB0-9]\s', value=' ')
    clean_text = clean_text.replace(regex=r'([^gG0-9])\1+', value=r'\1')
    return clean_text


def rm_html(text: pd.Series) -> pd.Series:
    """Remove HTML Tag from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without HTML Tag
    """
    clean_text = []
    for txt in text:
        new_text = BeautifulSoup(txt, "html.parser")
        clean_text.append(new_text.get_text())
    return pd.Series(clean_text)


def rm_non_ascii(text: pd.Series) -> pd.Series:
    """Remove NON ASCII character from text.
    
    Remove characters that are not based on the English alphabet.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without non ascii char
    """
    clean_text = []
    for txt in text:
        new_text = unicodedata.normalize('NFKD', txt).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        clean_text.append(new_text)
    return pd.Series(clean_text)


def rm_stopword(text: pd.Series) -> pd.Series:
    """Remove Indonesian stopwords using a dictionary based.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without Indonesian stopwords
    """
    factory = RemoverFactory()
    stopword = factory.create_stop_word_remover()

    clean_text = text.copy()
    for idx, row in text.items():
        clean_text.iloc[idx, :] = stopword.remove(row)
    return clean_text


def rm_emoticon(text: pd.Series) -> pd.Series:
    """Remove emoticon using a dictionary based.
    
    Emoticons are punctuation marks, letters, and numbers used to create pictorial icons that generally display an
    emotion or sentiment.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    clean_text : pd.Series
        Text without emoticon
    """
    emoticon_dict_path = pkg_resources.resource_filename('maleo',
                                                         'cleansing/Emoticon_Dict.p')
    with open(emoticon_dict_path, 'rb') as file:
        emoticon_dict = pickle.load(file)
    
    emoticon_pattern = re.compile(
        u'(' + u'|'.join(k for k in emoticon_dict) + u')')
    clean_text = text.replace(regex=emoticon_pattern, value=r'')
    return clean_text