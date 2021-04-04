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


def word_to_number(series: pd.Series, lang='id') -> pd.Series:
    if lang == 'eng':
        return series.apply(parse)
    else:
        return series


def get_hashtag(series: pd.Series) -> pd.DataFrame:
    list_text, list_hashtag = [], []
    for _, value in series.items():
        get_hashtag = list(
            set(part[1:] for part in value.split() if part.startswith('#')))
        if get_hashtag:
            list_text.append(value)
            list_hashtag.append(get_hashtag)

    return pd.DataFrame({'Text': list_text, 'Hashtag': list_hashtag})


def get_price(series: pd.Series) -> pd.DataFrame:
    list_text, list_price = [], []
    for _, value in series.items():
        price = Price.fromstring(value)
        if price.currency in ['Rp', 'RP', '$']:
            list_text.append(value)
            list_price.append(price)

    return pd.DataFrame({'Text': list_text, 'Price': list_price})


def email_to_tag(series: pd.Series) -> pd.Series:
    series = series.replace(regex=r'[\w\.-]+@[\w\.-]+\.\w+', value='<EMAIL>')
    return series


def date_to_tag(series: pd.Series) -> pd.Series:
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    date = re.compile('|'.join([ddmmyyyy, yyyymmdd]))
    series = series.replace(regex=date, value='<DATE>')
    return series


def phone_to_tag(series: pd.Series) -> pd.Series:
    re_phone_num = r'(\+62\s?|0)(\d{3,4}-?){2}\d{3,4}'
    series = series.replace(regex=re_phone_num, value='<PHONE NUM>')
    return series


def read_json(json_path: str) -> dict:
    with open(json_path, 'r') as file:
        data_dict = json.load(file)
    return data_dict


def slang_to_formal(series: pd.Series) -> pd.Series:
    slang_dict_path = pkg_resources.resource_filename('maleo',
                                                      'preprocessing/slang_dict.json')
    dict_alay = read_json(slang_dict_path)

    keyword_proc = KeywordProcessor()
    for word in dict_alay.items():
        keyword_proc.add_keyword(word[0], word[1])

    series = pd.Series(series)
    result = series.apply(keyword_proc.replace_keywords)
    result = result.replace(r"\s{2,}", "")
    result = result.str.strip()
    return result


def load_emojis():
    emoji_dict_path = pkg_resources.resource_filename('maleo',
                                                      'preprocessing/Emoji_Dict.p')
    with open(emoji_dict_path, 'rb') as fp:
        emoji_dict = pickle.load(fp)
    emoji_dict = {v: k for k, v in emoji_dict.items()}
    return emoji_dict


def emoji_to_word(series: pd.Series) -> pd.Series:
    whitespace = " "
    emoji_dict = load_emojis()
    
    for emot in emoji_dict:
        pattern = r'(' + emot + ')'
        val = "_".join(emoji_dict[emot].replace(
            ",", "").replace(":", "").split()) + whitespace
        series = series.replace(regex=pattern, value=val)
    return series


def emoji_to_tag(series: pd.Series) -> pd.Series:
    emoji_dict = load_emojis()

    for emot in emoji_dict:
        pattern = r'(' + emot + ')'
        val = "<EMOJI> "
        series = series.replace(regex=pattern, value=val)
    return series


def custom_regex(series: pd.Series, pattern: str, val: str) -> pd.Series:
    series = series.replace(regex=pattern, value=val)
    return series