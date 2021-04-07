import re
import pickle
import json
import pandas as pd
from number_parser import parse
from price_parser import Price
from flashtext import KeywordProcessor
import pkg_resources


__all__ = ["word_to_number", "get_hashtag", "get_price", "email_to_tag", "date_to_tag", 
           "phone_to_tag", "slang_to_formal", "emoji_to_word", "emoji_to_tag", "custom_regex"]


def word_to_number(text: pd.Series, lang='en') -> pd.Series:
    """Convert numbers written in the natural language to it's equivalent numeric forms in text.
    
    It currently supports cardinal numbers in the following languages - English(en), Hindi(hi), 
    Spanish(es), Russian(ru) and ordinal numbers in English.
    
    SUPPORTED_LANGUAGES = ['en', 'es', 'hi', 'ru']
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    lang : str
        Language, Default = 'en'
    Returns
    -------
    prepro_text : pd.Series
        Text with numbers written in numeric forms
    """
    def cvt(row, lang):
        return parse(row, language=lang)
    
    prepro_text = text.apply(cvt, lang=lang)
    return prepro_text


def get_hashtag(text: pd.Series) -> pd.DataFrame:
    """Extract hashtag from text.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.DataFrame
        DataFrame with 2 columns (Text, Hashtag)
    """
    list_text, list_hashtag = [], []
    for _, value in text.items():
        get_hashtag = list(set(part[1:] for part in value.split() if part.startswith('#')))
        if get_hashtag:
            list_text.append(value)
            list_hashtag.append(get_hashtag)
            
    prepro_text = pd.DataFrame({'Text': list_text, 'Hashtag': list_hashtag})
    return prepro_text


def get_price(text: pd.Series) -> pd.DataFrame:
    """Extract price from text, currency that supported => ['Rp', 'RP', '$'].
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.DataFrame
        DataFrame with 2 columns (Text, Price)
    """
    list_text, list_price = [], []
    for _, value in text.items():
        price = Price.fromstring(value)
        if price.currency in ['Rp', 'RP', '$']:
            list_text.append(value)
            list_price.append(price)

    prepro_text = pd.DataFrame({'Text': list_text, 'Price': list_price})
    return prepro_text


def email_to_tag(text: pd.Series) -> pd.Series:
    """Convert email to <EMAIL> tag.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.Series
        Text with encoded an email adress
    """
    prepro_text = text.replace(regex=r'[\w\.-]+@[\w\.-]+\.\w+', value='<EMAIL>')
    return prepro_text


def date_to_tag(text: pd.Series) -> pd.Series:
    """Convert date to <DATE> tag.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.Series
        Text with encoded a date
    """
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    date = re.compile('|'.join([ddmmyyyy, yyyymmdd]))
    prepro_text = text.replace(regex=date, value='<DATE>')
    return prepro_text


def phone_to_tag(text: pd.Series) -> pd.Series:
    """Convert phone number to <PHONE> tag.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.Series
        Text with encoded a phone number
    """
    re_phone_num = r'(\+62\s?|0)(\d{3,4}-?){2}\d{3,4}'
    prepro_text = text.replace(regex=re_phone_num, value='<PHONE>')
    return prepro_text


def read_json(json_path: str) -> dict:
    with open(json_path, 'r') as file:
        data_dict = json.load(file)
    return data_dict


def slang_to_formal(text: pd.Series) -> pd.Series:
    """Convert slang or colloquial word to formal word.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.Series
        Text with formal word
    """
    slang_dict_path = pkg_resources.resource_filename('maleo',
                                                      'preprocessing/slang_dict.json')
    dict_alay = read_json(slang_dict_path)

    keyword_proc = KeywordProcessor()
    for word in dict_alay.items():
        keyword_proc.add_keyword(word[0], word[1])

    prepro_text = text.apply(keyword_proc.replace_keywords)
    prepro_text = prepro_text.replace(r"\s{2,}", "")
    prepro_text = prepro_text.str.strip()
    return prepro_text


def load_emojis():
    emoji_dict_path = pkg_resources.resource_filename('maleo',
                                                      'preprocessing/Emoji_Dict.p')
    with open(emoji_dict_path, 'rb') as fp:
        emoji_dict = pickle.load(fp)
    emoji_dict = {v: k for k, v in emoji_dict.items()}
    return emoji_dict


def emoji_to_word(text: pd.Series) -> pd.Series:
    """Convert emoji to natural language format.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    text : pd.Series
        Text with emoji in natural language format
    """
    whitespace = " "
    emoji_dict = load_emojis()
    
    for emot in emoji_dict:
        pattern = r'(' + emot + ')'
        val = "_".join(emoji_dict[emot].replace(
            ",", "").replace(":", "").split()) + whitespace
        text = text.replace(regex=pattern, value=val)
    return text


def emoji_to_tag(text: pd.Series) -> pd.Series:
    """Convert emoji to <EMOJI> tag.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    text : pd.Series
        Text with emoji encoded in tag format
    """
    emoji_dict = load_emojis()

    for emot in emoji_dict:
        pattern = r'(' + emot + ')'
        val = "<EMOJI> "
        text = text.replace(regex=pattern, value=val)
    return text


def custom_regex(text: pd.Series, pattern: str, val: str) -> pd.Series:
    """Do what you want with customize regex pattern.
    
    Parameters
    ----------
    text : pd.Series
        Series of text data
    Returns
    -------
    prepro_text : pd.Series
        Result text from custom regex
    """
    prepro_text = text.replace(regex=pattern, value=val)
    return prepro_text