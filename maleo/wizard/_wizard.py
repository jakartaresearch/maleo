from maleo.cleansing import rm_multiple_space, rm_link, rm_punc, rm_char
from maleo.cleansing import rm_html, rm_non_ascii, rm_stopword, rm_emoticon
from maleo.preprocessing import word_to_number, get_hashtag, get_price, email_to_tag, date_to_tag
from maleo.preprocessing import phone_to_tag, slang_to_formal, emoji_to_word, emoji_to_tag, custom_regex
from maleo.scanner import scanner


class Wizard:
    """Wrapper for all functions a.k.a magic class"""
    def __init__(self):
        self.scanner = scanner
        self.rm_multiple_space = rm_multiple_space
        self.rm_link = rm_link
        self.rm_punc = rm_punc
        self.rm_char = rm_char
        self.rm_html = rm_html
        self.rm_non_ascii = rm_non_ascii
        self.rm_stopword = rm_stopword
        self.rm_emoticon = rm_emoticon
        self.word_to_number = word_to_number
        self.get_hashtag = get_hashtag
        self.get_price = get_price
        self.email_to_tag = email_to_tag
        self.date_to_tag = date_to_tag
        self.phone_to_tag = phone_to_tag
        self.slang_to_formal = slang_to_formal
        self.emoji_to_word = emoji_to_word
        self.emoji_to_tag = emoji_to_tag
        self.custom_regex = custom_regex