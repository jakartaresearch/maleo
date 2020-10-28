from maleo.stopword_remover.ArrayDictionary import ArrayDictionary
from maleo.stopword_remover.Remover import Remover
import pkg_resources


class RemoverFactory(object):
    """description of class."""

    def create_stop_word_remover(self):
        stopWords = self.get_stop_words()
        dictionary = ArrayDictionary(stopWords)
        stopWordRemover = Remover(dictionary)

        return stopWordRemover

    def get_stop_words(self):
        indo_stopwords_path = pkg_resources.resource_filename('maleo',
                                                              'stopword_remover/indo_stopwords.txt')
        with open(indo_stopwords_path, 'r') as file:
            tmp = file.readlines()
            stopword = [word.rstrip('\n') for word in tmp]
        return stopword
