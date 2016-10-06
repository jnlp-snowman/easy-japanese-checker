# -*- coding: utf-8 -*-

import MeCab
from orm import *


class EasyJapanese(object):
    """
    """
    def __init__(self, tagger_dir=""):
        self.tagger = MecabTagger(tagger_dir)

    def parse2web_register(self, sentence):
        """
        Web上で表示するためのフォーマット
        [[やさしい, boedh], []]
        """
        morphemes = self.tagger.parse2morphemes(sentence)
        # ToDo:辞書型に変更。javascriptから扱いやすくなる。
        return [(morph.surface, morph.unidic_id, self.get_morph_type(morph.unidic_id)) for morph in morphemes]

    def get_morph_type(self, unidic_id):
        row = db_session.query(EasyUniDic).filter(EasyUniDic.unidic_id == unidic_id).one_or_none()

        if row is None:
            return "none"
        else:
            return "easy"

    def change_easy(self, unidic_id, surface):
        morph = EasyUniDic()
        morph.unidic_id = unidic_id
        morph.surface = surface

        row = db_session.query(EasyUniDic).filter(EasyUniDic.unidic_id == unidic_id).one_or_none()

        if row is None:
            db_session.merge(morph)
            db_session.commit()
            return "easy"
        else:
            db_session.delete(row)
            db_session.commit()
            return "none"

class MecabTagger(object):
    def __init__(self, tagger_dir=""):
        if tagger_dir != "":
            tagger_dir = "-d " + tagger_dir
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
