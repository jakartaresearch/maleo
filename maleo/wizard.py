import pandas as pd

from maleo.scanner.scanner import scan
from maleo.cleansing.cleansing import remove
from maleo.preprocessing.preprocessing import encode_email, encode_date, encode_phone_num
from maleo.preprocessing.preprocessing import convert_slang_formal, word2number
from maleo.preprocessing.preprocessing import extract_price, extract_hashtag


class Wizard:
    def __init__(self):
        self.tes = 'tes'

    def scan_text(self, df, text_column):
        return scan(df, text_column)

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
        return extract_price(text)

    def hashtag_parser(self, text):
        return extract_hashtag(text)

    def convert_dtype(self, text):
        if isinstance(text, list) or isinstance(text, str):
            text = pd.Series(text)
        elif not isinstance(text, pd.core.series.Series):
            print('Data Type not supported')
        return text
