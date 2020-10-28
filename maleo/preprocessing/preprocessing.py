import re
import pickle
import json
import pandas as pd
from number_parser import parse
from price_parser import Price
from flashtext import KeywordProcessor


def word2number(series: pd.Series, lang='id') -> pd.Series:
    if lang == 'eng':
        return series.apply(parse)
    else:
        return series


def extract_hashtag(series: pd.Series) -> pd.DataFrame:
    list_text, list_hashtag = [], []
    for _, value in series.items():
        get_hashtag = list(
            set(part[1:] for part in value.split() if part.startswith('#')))
        if get_hashtag:
            list_text.append(value)
            list_hashtag.append(get_hashtag)

    return pd.DataFrame({'Text': list_text, 'Hashtag': list_hashtag})


def extract_price(series: pd.Series) -> pd.DataFrame:
    list_text, list_price = [], []
    for _, value in series.items():
        price = Price.fromstring(value)
        if price.currency in ['Rp', 'RP', '$']:
            list_text.append(value)
            list_price.append(price)

    return pd.DataFrame({'Text': list_text, 'Price': list_price})


def encode_email(series: pd.Series) -> pd.Series:
    series = series.replace(regex=r'[\w\.-]+@[\w\.-]+\.\w+', value='<EMAIL>')
    return series


def encode_date(series: pd.Series) -> pd.Series:
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    date = re.compile('|'.join([ddmmyyyy, yyyymmdd]))
    series = series.replace(regex=date, value='<DATE>')
    return series


def encode_phone_num(series: pd.Series) -> pd.Series:
    re_phone_num = r'(\+62\s?|0)(\d{3,4}-?){2}\d{3,4}'
    series = series.replace(regex=re_phone_num, value='<PHONE NUM>')
    return series


def read_json(json_path: str) -> dict:
    with open(json_path, 'r') as file:
        data_dict = json.load(file)
    return data_dict


def convert_slang_formal(series: pd.Series) -> pd.Series:
    dict_alay = read_json('maleo/preprocessing/slang_dict.json')

    keyword_proc = KeywordProcessor()
    for word in dict_alay.items():
        keyword_proc.add_keyword(word[0], word[1])

    series = pd.Series(series)
    result = series.apply(keyword_proc.replace_keywords)
    result = result.replace(r"\s{2,}", "")
    result = result.str.strip()
    return result


def convert_emojis_to_word(series: pd.Series) -> pd.Series:
    with open('maleo/preprocessing/Emoji_Dict.p', 'rb') as fp:
        emoji_dict = pickle.load(fp)
    emoji_dict = {v: k for k, v in emoji_dict.items()}

    for emot in emoji_dict:
        pattern = r'(' + emot + ')'
        val = "_".join(emoji_dict[emot].replace(
            ",", "").replace(":", "").split())
        series = series.replace(regex=pattern, value=val)
    return series
