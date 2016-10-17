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
        morph_id = db_snow.db_session.query(db_snow.CharMorph.CharId).filter(db_snow.CharMorph.UniDicId == unidic_id).one_or_none()

        if morph_id is None:
            return "unk"
        else:
            morph_id = morph_id[0]

        row = db_session.query(EasyMorph).filter(EasyMorph.id == morph_id).one_or_none()

        if row is None:
            return "none"
        else:
            return "easy"

    def change_easy(self, unidic_id, surface):
        """
        やさしい日本語かそうでないかのチェックを切り替える
        """
        if unidic_id.startswith("zz"):
            return "unk"

        morph = EasyMorph()
        morph.id = db_snow.db_session.query(db_snow.CharMorph.CharId).filter(db_snow.CharMorph.UniDicId == unidic_id).one()[0]
        morph.org2_kanji = db_snow.db_session.query(db_snow.UniDic.org2_kanji).filter(db_snow.UniDic.ID == unidic_id).one()[0]

        # 対象の語がデータベースに存在すれば、その行が戻り値となる。ない場合はNone
        row = db_session.query(EasyMorph).filter(EasyMorph.id == morph.id).one_or_none()

        if row is None:
            db_session.merge(morph)
            return "easy"
        else:
            db_session.delete(row)
            return "none"

    def get_number_of_easy_morph(self):
        """
        """
        return db_session.query(EasyMorph).count()

    def get_register_words(self):
        morph_ids = db_session.query(EasyMorph.id).all()
        morph_ids = [morph_id[0] for morph_id in morph_ids]

        unidic_ids = db_snow.db_session.query(db_snow.UniDic.ID).join(db_snow.CharMorph, db_snow.UniDic.ID==db_snow.CharMorph.UniDicId).filter(db_snow.CharMorph.CharId.in_(morph_ids)).all()
        unidic_ids = [unidic_id[0] for unidic_id in unidic_ids]

        return db_snow.db_session.query(db_snow.UniDic).filter(db_snow.UniDic.ID.in_(unidic_ids)).group_by(db_snow.UniDic.org2_kanji).order_by(db_snow.UniDic.POS).all()


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
