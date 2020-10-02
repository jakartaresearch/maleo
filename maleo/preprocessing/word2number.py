from number_parser import parse

def w2n(text, lang):
    if lang == 'eng':
        return parse(text)
    else:
        return text