import re
import emoji
import pandas as pd


__all__ = ["scanner"]

def scanner(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Scan text dataset, which is do count char, word, emoji, number, punctuation and date in each text.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of text data
    text_column : str
        Choose specific column name in DataFrame
    Returns
    -------
    df : pd.DataFrame
        Summary of text dataset
    """
    df['chars_count'] = df[text_column].apply(len)
    df['words_count'] = df[text_column].apply(count_words)
    df['emojis_count'] = df[text_column].apply(count_emojis)
    df['numbers_count'] = df[text_column].apply(count_numbers)
    df['punctuations_count'] = df[text_column].apply(count_punctuations)
    df['dates_count'] = df[text_column].apply(count_dates)
    return df


def count_words(text: str) -> int:
    word = re.findall(r'\b[^\d\W]+\b', text)
    return len(word)


def gather_emojis(text: str):
    emoji_expaned_text = emoji.demojize(text)
    return re.findall(r'\:(.*?)\:', emoji_expaned_text)


def count_emojis(text: str) -> int:
    return len(gather_emojis(text))


def gather_numbers(text: str):
    numbers = re.findall(r'[0-9]+', text)
    return numbers


def count_numbers(text: str) -> int:
    return len(gather_numbers(text))


def gather_punctuations(text: str) -> list:
    line = re.findall(r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*', text)
    string = "".join(line)
    return list(string)


def count_punctuations(text: str) -> int:
    return len(gather_punctuations(text))


def gather_dates(text: str, date_format='dd/mm/yyyy'):
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    regex_list = {
        'dd/mm/yyyy': ddmmyyyy, 'yyyy/mm/dd': yyyymmdd
    }
    return re.findall(regex_list[date_format], text)


def count_dates(text: str) -> int:
    return len(gather_dates(text))
