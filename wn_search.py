# A bad searcher that tries to find a target synset in WordNet
import nltk
import os
import shutil

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from nltk.corpus.reader.wordnet import Lemma
from wn_eval import Oracle
from typing import Union
from gensim.models import KeyedVectors
import numpy as np

from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec


def split_in_two(words):
    mid = len(words) // 2
    return words[:mid], words[mid:]


class Searcher:
    """
    Class to search WordNet through logical queries.
    """

    def __init__(self):
        dir = os.getcwd()
        glove_file = datapath(dir + '/glove.6B.100d.txt')
        word2vec_glove_file = get_tmpfile("glove.6B.100d.word2vec.txt")
        glove2word2vec(glove_file, word2vec_glove_file)
        self._searched = {}
        self.word_vectors = KeyedVectors.load_word2vec_format(word2vec_glove_file)
        self.centroid = self.word_vectors.vectors.mean(axis=0)
        self.similar_words = self.word_vectors.similar_by_vector(vector=self.centroid, topn=650000)

        self.closest_words = [word for word, score in self.similar_words]

    def check(self, oracle: Oracle, candidate: Synset) -> bool:
        """
        Convenience method to check whether two synsets are the same
        and storing the result.
        
        Keyword Arguments:
        oracle -- The oracle that can check whether the candidate matches
        candidate -- The synset to check
        """
        # print("Searching %s" % str(candidate))
        self._searched[candidate] = oracle.check(candidate)
        # self._not_searched.remove(candidate)
        return self._searched[candidate]

    def __call__(self, oracle: Oracle) -> Synset:
        """
        Given an oracle, return the synset that the oracle has as its target.
        
        Keyword Arguments:
        oracle -- The oracle being searched
        """

        # Feel free to change the code within
        # --------------------------------------

        # Start at the top, go breadth first
        self.check(oracle, wn.synset('entity.n.01'))
        remaining_synsets = self.closest_words
        # Keeps a track of whether we found Hypernym, Hyponym or Part-meronym in GloVe embedding
        wn_task = "hypernyms"
        i = 0
        while True:
            i += 1
            # print("Iteration number:", i)

            # Splitting the closest synsets in two
            left_closest_words, right_closest_words = split_in_two(self.closest_words)

            # Getting Synsets for the words
            synsets_for_left_close_words = [synset for word in left_closest_words for synset in wn.synsets(word)]
            synsets_for_right_close_words = [synset for word in right_closest_words for synset in wn.synsets(word)]

            # Removing blank synsets
            synsets_for_left_close_words = [synsets for synsets in synsets_for_left_close_words if synsets]
            synsets_for_right_close_words = [synsets for synsets in synsets_for_right_close_words if synsets]

            if wn_task == "hypernyms":
                if oracle.cnf_eval([["hypernyms"] * len(synsets_for_left_close_words)], [synsets_for_left_close_words]):
                    self.closest_words = left_closest_words
                elif oracle.cnf_eval([["hypernyms"] * len(synsets_for_right_close_words)], [synsets_for_right_close_words]):
                    self.closest_words = right_closest_words
                else:
                    wn_task = "hyponyms"

            if wn_task == "hyponyms":
                if oracle.cnf_eval([["hyponyms"] * len(synsets_for_left_close_words)], [synsets_for_left_close_words]):
                    self.closest_words = left_closest_words
                elif oracle.cnf_eval([["hyponyms"] * len(synsets_for_right_close_words)], [synsets_for_right_close_words]):
                    self.closest_words = right_closest_words
                else:
                    wn_task = "part_meronyms"

            if wn_task == "part_meronyms":
                if oracle.cnf_eval([["part_meronyms"] * len(synsets_for_left_close_words)], [synsets_for_left_close_words]):
                    self.closest_words = left_closest_words
                elif oracle.cnf_eval([["part_meronyms"] * len(synsets_for_right_close_words)], [synsets_for_right_close_words]):
                    self.closest_words = right_closest_words
                else:
                    wn_task = "none found"
                    break

            if len(self.closest_words) == 1:
                break
        print('ran {} iterations'.format(i))
        # ---------------------------------------
        found = None
        final_hypernym_synset = wn.synsets(self.closest_words[0])

        if wn_task == "hypernyms":
            for syn in final_hypernym_synset:
                for x in syn.hyponyms():
                    if oracle.check(x):
                        found = x
        elif wn_task == "hyponyms":
            for syn in final_hypernym_synset:
                for x in syn.hypernyms():
                    if oracle.check(x):
                        found = x
        elif wn_task == "part_meronyms":
            for syn in final_hypernym_synset:
                for x in syn.part_holonyms():
                    if oracle.check(x):
                        found = x
        else:
            assert "Searched all of WN without finding it!"

        return found


if __name__ == "__main__":
    oracle = Oracle(wn.synset('dog.n.01'))
    searcher = Searcher()
    print("Search result is:")
    print(searcher(oracle))
    print("Took %i steps to get there" % oracle.num_queries())
