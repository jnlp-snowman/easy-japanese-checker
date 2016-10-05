# -*- coding: utf-8 -*-

import MeCab

TAGGER_DIR = "/Users/takahashi/work/mecab_systemdic"

class EasyJapanese(object):
    def __init__(self, tagger_dir=""):
        self.tagger = MecabTagger(tagger_dir)

    def parse2web_register(self, sentence):
        """
        Web上で表示するためのフォーマット
        [[やさしい, boedh], []]
        """
        morphemes = self.tagger.parse2morphemes(sentence)
        # ToDo:辞書型に変更。javascriptから扱いやすくなる。
        return [(morph.surface, morph.unidic_id) for morph in morphemes]


class MecabTagger(object):
    def __init__(self, tagger_dir=""):
        self.tagger = MeCab.Tagger(tagger_dir)
        self.tagger.parse("おまじない")

    def parse2morphemes(self, sentence):
        morphems = []

        node = self.tagger.parseToNode(sentence)
        node = node.next
        while node.next:
            morph = Morpheme()
            morph.load_unidic_node(node)
            morphems.append(morph)
            node = node.next
        return morphems

    def parse2wakati(self, sentence):
        morphemes = self.parse2morphemes(sentence)
        surfaces = [morpheme.surface for morpheme in morphemes]
        return " ".join(surfaces)

class Morpheme(object):
    def __init__(self):
        pass

    def load_ipadic_node(self):
        pass

    def load_unidic_node(self, unidic_node):
        surface = unidic_node.surface
        feature = unidic_node.feature.split(',')

        self.surface = surface
        self.unidic_id = feature[17]
