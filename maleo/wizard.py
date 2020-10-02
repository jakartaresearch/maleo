import pandas as pd

from maleo.cleansing.cleansing import remove
from maleo.scanner.scanner import scan


class Wizard:
    def __init__(self):
        self.tes = 'tes'
    
    def scan_text(self, dataframe, text_column):
        df_scan = scan(dataframe, text_column)
        return df_scan
        
    def apply(self, text):
        series = self.convert_dtype(text)
        series = remove(series)
        return series
    
    def convert_dtype(self, text):
        if type(text) == list or type(text) == str:
            text = pd.Series(text)
        elif type(text) != pd.core.series.Series :
            print('Data Type not supported')
        return text