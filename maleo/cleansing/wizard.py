import os
import re
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
        
        
    def run(self, text):
        series = self.convert_dtype(text)
        series = self.remove_link(series)
        series = self.remove_html(series)
        series = self.remove_non_ascii(series)
        return series
    
    def convert_dtype(self, text):
        if type(text) == list or type(text) == str:
            text = pd.Series(text)
        elif type(text) != pd.core.series.Series :
            print('Data Type not supported')
        return text
        
    def remove_link(self, series):
        series = series.replace(regex=r'http\S+', value='')
        series = series.replace(regex=r'pic.twitter.com\S+', value='')
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