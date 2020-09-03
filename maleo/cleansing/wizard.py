import os
import re
import string
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup

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
        
    def run(self, text):
        series = self.convert_dtype(text)
        series = self.remove(series)
        series = self.remove_html(series)
        series = self.remove_non_ascii(series)
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