import gdown
import pkg_resources

from os import path
from flair.data import Sentence
from flair.models import SequenceTagger


__all__ = ["POS"]

class POS:
    """A Part-of-Speech Tagging classifier.
    
    POST, also called grammatical tagging is the process of marking up a word in a text as 
    corresponding to a particular part of speech.
    
    References
    ----------
    https://universaldependencies.org/u/pos/index.html
    """
    def __init__(self):
        self.model = self.load_model()


    def check_model(self, model_filename):
        """Check existence of model, if not exist then will download the model."""
        if not path.exists(model_filename):
            url = 'https://drive.google.com/uc?id=1-C8RRM9c-IaGgN2jdzFtlwY7BuOAMY3W'
            print('Downloading model ...')
            gdown.download(url, model_filename, quiet=False)
            print('DONE ...')


    def load_model(self):
        """Load POST model"""
        model_path = pkg_resources.resource_filename('maleo','pos_tag/pos_model.pt')
        self.check_model(model_path)
        model = SequenceTagger.load(model_path)
        return model


    def predict(self, text:str, output_pair=False):
        """Inference POST model.

        Parameters
        ----------
        text: str
            Input text
        output_pair: boolean
            True -> list of tuples 
            False -> tuple
        Returns:
        -------
        out : tuple or list of tuples
            Inference result with format based on output_pair
        """
        input_text = Sentence(text)
        self.model.predict(input_text)
        output_text = input_text.to_tagged_string()

        item = output_text.split()
        out = [(item[idx], item[idx+1]) for idx in range(0, len(item), 2)]

        if not output_pair:
            sent, pos = zip(*out)
            out = (' '.join(sent), ' '.join(pos))
            return out
        else:
            return out