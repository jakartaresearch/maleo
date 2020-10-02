import pandas as pd
import emoji
import re

from itertools import groupby
from nltk.tokenize import word_tokenize


def scan(dataframe, text_column, params={}):
    print(f"params: {params}")
    columns_to_drop = list(set(dataframe.columns) - set([text_column]))
    new_dataframe = dataframe.drop(columns=columns_to_drop, axis=1).copy()

    granular_analysis = False
    if (not params):
        params = {
            'granular': True,
        }

    if 'granular' in params:
        granular_analysis = params['granular']

    if granular_analysis: 
        new_dataframe['characters_count'] = new_dataframe[text_column].apply(len)
        new_dataframe['spaces_count'] = new_dataframe[text_column].apply(count_spaces)
        new_dataframe['words_count'] = new_dataframe[text_column].apply(words_count)
        new_dataframe['duplicates_count'] = new_dataframe[text_column].apply(count_duplicates)
        new_dataframe['chars_excl_spaces_count'] = new_dataframe[text_column].apply(count_characters_excluding_spaces)
        new_dataframe['emoji_count'] = new_dataframe[text_column].apply(count_emojis)
        new_dataframe['whole_numbers_count'] = new_dataframe[text_column].apply(count_whole_numbers)
        new_dataframe['alpha_numeric_count'] = new_dataframe[text_column].apply(count_alpha_numeric)
        new_dataframe['non_alpha_numeric_count'] = new_dataframe[text_column].apply(count_non_alpha_numeric)
        new_dataframe['punctuations_count'] = new_dataframe[text_column].apply(count_punctuations)
        new_dataframe['dates_count'] = new_dataframe[text_column].apply(count_dates)

    return new_dataframe


def count_spaces(text):
    spaces = re.findall(r' ', text)
    return len(spaces)


def gather_words(text):
    return re.findall(r'\b[^\d\W]+\b', text)


def words_count(text):
    return len(gather_words(text))


def gather_duplicates(text):
    tokenized_text = word_tokenize(text.lower())
    sorted_tokenized_text = sorted(tokenized_text)
    duplicates = {}
    for value, group in groupby(sorted_tokenized_text):
        frequency = len(list(group))
        if frequency > 1:
            duplicates.update({value: frequency})

    return duplicates


def count_duplicates(text):
    return len(gather_duplicates(text))


def count_characters_excluding_spaces(text):
    return len(text) - count_spaces(text)


def gather_emojis(text):
    emoji_expaned_text = emoji.demojize(text)
    return re.findall(r'\:(.*?)\:', emoji_expaned_text) 


def count_emojis(text):
    list_of_emojis = gather_emojis(text)
    return len(list_of_emojis)


def gather_whole_numbers(text):
    line = re.findall(r'[0-9]+', text)
    return line


def count_whole_numbers(text):
    list_of_numbers = gather_whole_numbers(text)
    return len(list_of_numbers)


def gather_alpha_numeric(text):
    return re.findall('[A-Za-z0-9]', text)


def count_alpha_numeric(text):
    return len(gather_alpha_numeric(text))


def gather_non_alpha_numeric(text):
    return re.findall('[^A-Za-z0-9]', text)


def count_non_alpha_numeric(text):
    return len(gather_non_alpha_numeric(text))


def gather_punctuations(text):
    line = re.findall(r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*', text)
    string = "".join(line)
    return list(string)


def count_punctuations(text):
    return len(gather_punctuations(text))


def gather_dates(text, date_format='dd/mm/yyyy'):
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    regex_list =  {
        'dd/mm/yyyy': ddmmyyyy, 'yyyy/mm/dd': yyyymmdd
    }
    return re.findall(regex_list[date_format], text)


def encode_dates(text):
    ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
    yyyymmdd = r'\b([0-9]{4})/(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])\b'
    date = re.compile('|'.join([ddmmyyyy, yyyymmdd]))
    return re.sub(date, '<DATE>', text)


def count_dates(text):
    return len(gather_dates(text))