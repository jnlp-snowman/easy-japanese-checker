# -*- coding: utf-8 -*-

import MeCab
from orm import *
import db_snow

class EasyJapanese(object):
    """
    やさしい日本語の解析
    """
    def __init__(self, tagger_dir=""):
        """
        MeCabの初期化
        """
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
        """
        やさしい日本語かどうかを付与
        """
        row = db_session.query(EasyUniDic).filter(EasyUniDic.unidic_id == unidic_id).one_or_none()

        if row is None:
            return "none"
        else:
            return "easy"

    def change_easy(self, unidic_id, surface):
        """
        やさしい日本語かそうでないかのチェックを切り替える
        """
        morph = EasyUniDic()
        morph.unidic_id = unidic_id
        morph.surface = surface
        # 対象の語がデータベースに存在すれば、その行が戻り値となる。ない場合はNone
        row = db_session.query(EasyUniDic).filter(EasyUniDic.unidic_id == unidic_id).one_or_none()

        if row is None:
            db_session.merge(morph)
            # db_session.flush()
            # db_session.commit()
            return "easy"
        else:
            db_session.delete(row)
            # db_session.flush()
            # db_session.commit()
            return "none"

    def get_number_of_easy_morph(self):
        """
        """
        return db_session.query(EasyUniDic).count()

    def get_register_words(self):
        unidic_ids = db_session.query(EasyUniDic.unidic_id).all()
        unidic_ids = [unidic_id[0] for unidic_id in unidic_ids]
        return db_snow.db_session.query(db_snow.UniDic).filter(db_snow.UniDic.ID.in_(unidic_ids)).order_by(db_snow.UniDic.POS).all()

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
