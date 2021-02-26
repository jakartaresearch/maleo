# Maleo
Wrapper library for text cleansing, preprocessing in NLP

## Overview of features
    - Scanner : get insight about your text dataset (ex: number of chars, words, emojis, etc)
    - Remove hyperlink, punctuation, stopword, emoticon, etc
    - Extract hashtags, price from text
    - Convert email, phone number, date to <TAG>
    - Convert Indonesian slang to formal word
    - Convert emoji to word or <TAG>
    - Convert word to number
    - Predict Part-of-Speech (POS) tags

## Installation
```
pip install maleo
```

## Getting Started
```python
from maleo.wizard import Wizard

wiz = Wizard()

wiz.scanner(df, 'text')
wiz.emoji_to_word(df.text)
wiz.slang_to_formal(df.text)

wiz.load_pos()
wiz.predict_pos('saya mau pergi beli makan siang dulu', output_pair=False)
```

## Instance Attribute
```
['scanner',
 'rm_multiple_space',
 'rm_link',
 'rm_punc',
 'rm_char',
 'rm_html',
 'rm_non_ascii',
 'rm_stopword',
 'rm_emoticon',
 'word_to_number',
 'get_hashtag',
 'get_price',
 'email_to_tag',
 'date_to_tag',
 'phone_num_to_tag',
 'slang_to_formal',
 'emoji_to_word',
 'emoji_to_tag',
 'custom_regex',
 'predict_pos']
```

## Universal POS tags
https://universaldependencies.org/u/pos/index.html

## Contributor:
- Ruben Stefanus
