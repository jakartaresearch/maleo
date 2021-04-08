<img src="logo.png" alt="Maleo" width="150" height="150">

# Maleo
Wrapper library for text cleansing, preprocessing and POS Tagging in NLP

## Docs
https://jakartaresearch.github.io/maleo/

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
from maleo.pos_tag import POS

wiz = Wizard()
pos = POS()

wiz.scanner(df, 'text')
wiz.emoji_to_word(df.text)
wiz.slang_to_formal(df.text)

pos.predict('saya mau pergi beli makan siang dulu', output_pair=False)
```

## Universal POS tags
https://universaldependencies.org/u/pos/index.html

## Contributor:
- Ruben Stefanus
