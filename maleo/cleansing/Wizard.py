import os
import re
import string
import pandas as pd
import unicodedata
import emoji

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from itertools import groupby
from maleo.stopword_remover.RemoverFactory import RemoverFactory

class Wizard:
    """ City Search Data <http://spidr-ursa.rutgers.edu/datasets/> Dataset
    
    Args:
        root (string): Root directory of dataset where ``CitySearch/raw/*`` exist.
        
        processed (bool): If True = Download, extract, combine to one .csv file. 
        If False = Download and extract original dataset only
        
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    
    """
    def __init__(self):
        self.tes = 'tes'
        
    def apply(self, text):
        series = self.convert_dtype(text)
        series = self.remove(series)
        series = self.remove_html(series)
        series = self.remove_non_ascii(series)
        series = self.remove_stopword(series)
        return series
    
    def convert_dtype(self, text):
        if type(text) == list or type(text) == str:
            text = pd.Series(text)
        elif type(text) != pd.core.series.Series :
            print('Data Type not supported')
        return text
        
    def remove(self, series):
        # remove link
        series = series.replace(regex=r'http\S+', value='')
        series = series.replace(regex=r'pic.twitter.com\S+', value='')
        # encode email link to 'EMAIL'
        series = series.replace(regex=r'[\w\.-]+@[\w\.-]+\.\w+', value='EMAIL')
        # remove punctuation
        punctuation_pattern = r"[\s{}]".format(re.escape(string.punctuation))
        series = series.replace(regex=punctuation_pattern, value=' ')
        # remove single char
        series = series.replace(regex=r'\s[^uUgGbB0-9]\s', value=' ')
        # remove consecutive repeating char
        series = series.replace(regex=r'([^gG])\1+', value=r'\1')
        # remove multiple whitespaces
        series = series.replace(regex=r'\s\s+', value=' ')
        
        series = series.str.strip()
        return series
    
    def remove_html(self, series):
        new_series = []
        for text in series:
            new_text = BeautifulSoup(text, "html.parser")
            new_series.append(new_text.get_text())
        return pd.Series(new_series)

    def remove_non_ascii(self, series):
        new_series = []
        for text in series:
            new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_series.append(new_text)
        return pd.Series(new_series)
    
    def remove_stopword(self, series):
        factory = RemoverFactory()
        stopword = factory.create_stop_word_remover()
        
        result = series.copy()
        for idx, row in series.items():
            result.iloc[idx,:] = stopword.remove(row)
        return result
        
    def profiling(self, dataframe, text_column, params={}):
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
            new_dataframe['spaces_count'] = new_dataframe[text_column].apply(self.count_spaces)
            new_dataframe['words_count'] = new_dataframe[text_column].apply(self.words_count)
            new_dataframe['duplicates_count'] = new_dataframe[text_column].apply(self.count_duplicates)
            new_dataframe['chars_excl_spaces_count'] = new_dataframe[text_column].apply(self.count_characters_excluding_spaces)
            new_dataframe['emoji_count'] = new_dataframe[text_column].apply(self.count_emojis)
            new_dataframe['whole_numbers_count'] = new_dataframe[text_column].apply(self.count_whole_numbers)
            new_dataframe['alpha_numeric_count'] = new_dataframe[text_column].apply(self.count_alpha_numeric)
            new_dataframe['non_alpha_numeric_count'] = new_dataframe[text_column].apply(self.count_non_alpha_numeric)
            new_dataframe['punctuations_count'] = new_dataframe[text_column].apply(self.count_punctuations)
            #new_dataframe['stop_words_count'] = new_dataframe[text_column].apply(count_stop_words)
            new_dataframe['dates_count'] = new_dataframe[text_column].apply(self.count_dates)

        return new_dataframe
  
    
    def count_spaces(self, text):
        spaces = re.findall(r' ', text)
        return len(spaces)
    
    def gather_words(self, text):
        return re.findall(r'\b[^\d\W]+\b', text)

    def words_count(self, text):
        return len(self.gather_words(text))
    
    def gather_duplicates(self, text):
        tokenized_text = word_tokenize(text.lower())
        sorted_tokenized_text = sorted(tokenized_text)
        duplicates = {}
        for value, group in groupby(sorted_tokenized_text):
            frequency = len(list(group))
            if frequency > 1:
                duplicates.update({value: frequency})

        return duplicates

    def count_duplicates(self, text):
        return len(self.gather_duplicates(text))
    
    def count_characters_excluding_spaces(self, text):
        return len(text) - self.count_spaces(text)
    
    def gather_emojis(self, text):
        emoji_expaned_text = emoji.demojize(text)
        return re.findall(r'\:(.*?)\:', emoji_expaned_text) 

    def count_emojis(self, text):
        list_of_emojis = self.gather_emojis(text)
        return len(list_of_emojis)
    
    def gather_whole_numbers(self, text):
        line = re.findall(r'[0-9]+', text)
        return line

    def count_whole_numbers(self, text):
        list_of_numbers = self.gather_whole_numbers(text)
        return len(list_of_numbers)
    
    def gather_alpha_numeric(self, text):
        return re.findall('[A-Za-z0-9]', text)

    def count_alpha_numeric(self, text):
        return len(self.gather_alpha_numeric(text))
    
    def gather_non_alpha_numeric(self, text):
        return re.findall('[^A-Za-z0-9]', text)

    def count_non_alpha_numeric(self, text):
        return len(self.gather_non_alpha_numeric(text))
    
    def gather_punctuations(self, text):
        line = re.findall(r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*', text)
        string = "".join(line)
        return list(string)

    def count_punctuations(self, text):
        return len(self.gather_punctuations(text))
    
    def gather_dates(self, text, date_format='dd/mm/yyyy'):
        ddmmyyyy = r'\b(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})\b'
        mmddyyyy = r'\b(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/([0-9]{4})\b'
        regex_list =  {
            'dd/mm/yyyy': ddmmyyyy, 'mm/dd/yyyy': mmddyyyy
        }
        return re.findall(regex_list[date_format], text)

    def count_dates(self, text):
        return len(self.gather_dates(text))