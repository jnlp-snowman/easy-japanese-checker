# -*- coding: utf-8 -*-

import json
import logging
from bottle import route, template, post, get, request, HTTPResponse
from easy_japanese import EasyJapanese, MecabTagger
from config_reader import read_config

# ロガー
logging.basicConfig(level=logging.DEBUG)
# コンフィグファイルの読み込み
config = read_config()
TAGGER_DIR = config.get('settings', 'mecab_systemdic')
# やさしい日本語インスタンスの生成
easy_japanese = EasyJapanese(TAGGER_DIR)
logging.debug(TAGGER_DIR)

@route('/')
def index():
    """
    Welcome page
    """
    return template("checker")

@route('/register')
def index():
    """
    """
    return template("sample")

@route('/checker')
def page_checker():
    return template("checker")

@route('/words')
def show_words_from_db():
    from collections import defaultdict

    try:
        easy_unidic_view_words=easy_japanese.get_register_words()
    except Exception as e:
        logging.debug(type(e))
        logging.debug(e.args)
        return "データベースエラー"

    word_dic = defaultdict(list)

    if easy_unidic_view_words is None:
        return template("show_words", word_dic=word_dic)

    for word in easy_unidic_view_words:
        if word.POS == None:
            word.POS = "未知語"
        word_dic[word.POS].append(word)

    return template("show_words", word_dic=word_dic)

@get('/api/tokenize')
def tokenize():
    """
    GETリクエストで送られてきた単語を分割し、返す
    """
    text = request.query.input_text
    if text == "":
        result = ""
    else:
        result = easy_japanese.parse2web_register(text)

    body = json.dumps(result)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/check_easy')
def check_easy():
    """
    形態素を選択した際に、記録を反映する。
    """
    unidic_id = request.json['unidic_id']
    surface = request.json['surface']

    morph_type = easy_japanese.change_easy(unidic_id, surface)

    body = json.dumps(morph_type)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/easy_morph_count')
def get_number_of_easy_morph():
    """
    """
    number = easy_japanese.get_number_of_easy_morph()
    body = json.dumps(number)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r
