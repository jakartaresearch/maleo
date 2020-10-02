import pandas as pd

from maleo.scanner.scanner import scan
from maleo.cleansing.cleansing import remove
from maleo.preprocessing.preprocessing import encode_email, encode_date, encode_phone_num
from maleo.preprocessing.preprocessing import convert_slang_formal, word2number, extract_price


class Wizard:
    def __init__(self):
        self.tes = 'tes'
    
    def scan_text(self, dataframe, text_column):
        df_scan = scan(dataframe, text_column)
        return df_scan
    
    
    def clean_text(self, text):
        series = self.convert_dtype(text)
        series = remove(series)
        return series
    
    
    def encode_text(self, text):
        series = encode_email(text)
        series = encode_date(series)
        series = encode_phone_num(series)
        return series
    
    
    def preprocessing(self, text):
        series = convert_slang_formal(text)
        return series
    
    
    def price_parser(self, text):
        df = extract_price(text)
        return df
    
    
    def convert_dtype(self, text):
        if type(text) == list or type(text) == str:
            text = pd.Series(text)
        elif type(text) != pd.core.series.Series :
            print('Data Type not supported')
        return text