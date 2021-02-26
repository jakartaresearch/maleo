import gdown
import pkg_resources

from os import path
from flair.data import Sentence
from flair.models import SequenceTagger


def check_model(model_filename):
    if not path.exists(model_filename):
        url = 'https://drive.google.com/uc?id=1-C8RRM9c-IaGgN2jdzFtlwY7BuOAMY3W'
        print('Downloading model ...')
        gdown.download(url, model_filename, quiet=False)
        print('DONE ...')


def load_model():
    model_path = pkg_resources.resource_filename('maleo','pos_tag/pos_model.pt')
    check_model(model_path)
    model = SequenceTagger.load(model_path)
    return model


def pos_inference(model, text:str, output_pair=False):
    """Inference POS Tagging model
    
    Args:
        text: input text
        output_pair: True -> list of tuples, False -> tuple
    Returns:
        out: inference result with format based on output_pair
    """
    input_text = Sentence(text)
    model.predict(input_text)
    output_text = input_text.to_tagged_string()

    item = output_text.split()
    out = [(item[idx], item[idx+1]) for idx in range(0, len(item), 2)]

    if not output_pair:
        sent, pos = zip(*out)
        out = (' '.join(sent), ' '.join(pos))
        return out
    else:
        return out