from maleo.scanner.scanner import scan
from maleo.cleansing.cleansing import remove_link, remove_punctuation, remove_char, remove_html
from maleo.cleansing.cleansing import remove_non_ascii, remove_stopword, remove_emoticons
from maleo.cleansing.cleansing import remove_multiple_space
from maleo.preprocessing.preprocessing import encode_email, encode_date, encode_phone_num
from maleo.preprocessing.preprocessing import convert_slang_formal, word2number, convert_emojis_to_word, convert_emojis_to_tag
from maleo.preprocessing.preprocessing import extract_price, extract_hashtag, custom_regex


class Wizard:
    def __init__(self):
        self.scanner = scan
        self.rm_multiple_space = remove_multiple_space
        self.rm_link = remove_link
        self.rm_punc = remove_punctuation
        self.rm_char = remove_char
        self.rm_html = remove_html
        self.rm_non_ascii = remove_non_ascii
        self.rm_stopword = remove_stopword
        self.rm_emoticon = remove_emoticons
        self.word_to_number = word2number
        self.get_hashtag = extract_hashtag
        self.get_price = extract_price
        self.email_to_tag = encode_email
        self.date_to_tag = encode_date
        self.phone_num_to_tag = encode_phone_num
        self.slang_to_formal = convert_slang_formal
        self.emoji_to_word = convert_emojis_to_word
        self.emoji_to_tag = convert_emojis_to_tag
        self.custom_regex = custom_regex


