# -*- coding: utf-8 -*-

import json
import logging
from bottle import route, template, post, get, request, HTTPResponse, redirect
from easy_japanese import EasyJapanese, MecabTagger, EasyJapanese2
from config_reader import read_config

# ロガー
logging.basicConfig(level=logging.DEBUG)

# コンフィグファイルの読み込み
config = read_config()
TAGGER_DIR = config.get('settings', 'mecab_systemdic')

# やさしい日本語インスタンスの生成
# easy_japanese = EasyJapanese(TAGGER_DIR) # user1
easy_japanese_2 = EasyJapanese2(TAGGER_DIR) # user2

logging.debug(TAGGER_DIR)

# 公開用
@route('/')
def index():
    """
    やさしい日本語チェッカーにリダイレクト。
    """
    redirect("/checker")

## User2用
# tokenize_2
@route('/register2')
def register_page():
    """
    登録ページ
    """
    return template("register2")

@route('/checker')
def checker_page():
    """
    やさしい日本語チェッカー
    """
    return template("checker2")

@route('/words2')
def show_words_from_db():
    """
    やさしい日本語の単語一覧を出力
    """
    from collections import defaultdict

    try:
        easy_unidic_view_words=easy_japanese_2.get_register_words()
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

        # 名詞の分類
        if word.POS == "名詞":
            if word.POS_s1 == "普通名詞" and word.POS_s2 == "サ変可能":
                word.POS = "サ変名詞"
            elif word.POS_s1 == "普通名詞" and (word.POS_s2 == "形状詞可能" or word.POS_s2 == "サ変形状詞可能"):
                word.POS = "形状詞"

        word_dic[word.POS].append(word)

    return template("show_words", word_dic=word_dic)

@get('/api/tokenize_2')
def tokenize():
    """
    GETリクエストで送られてきた単語を分割し、返す
    """
    text = request.query.input_text
    if text == "":
        result = ""
    else:
        result = easy_japanese_2.parse2web_register(text)

    body = json.dumps(result)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/check_easy_2')
def check_easy():
    """
    形態素を選択した際に、記録を反映する。
    """
    unidic_id = request.json['unidic_id']
    surface = request.json['surface']

    morph_type = easy_japanese_2.change_easy(unidic_id, surface)

    body = json.dumps(morph_type)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/easy_morph_count_2')
def get_number_of_easy_morph():
    """
    """
    number = easy_japanese_2.get_number_of_easy_morph()
    body = json.dumps(number)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

## User1用
# @route('/register')
# def index():
#     """
#     """
#     return template("sample")

# @route('/checker')
# def page_checker():
#     return template("checker")

# @route('/words')
# def show_words_from_db():
#     from collections import defaultdict

#     try:
#         easy_unidic_view_words=easy_japanese.get_register_words()
#     except Exception as e:
#         logging.debug(type(e))
#         logging.debug(e.args)
#         return "データベースエラー"

#     word_dic = defaultdict(list)

#     if easy_unidic_view_words is None:
#         return template("show_words", word_dic=word_dic)

#     for word in easy_unidic_view_words:
#         if word.POS == None:
#             word.POS = "未知語"

#         # 名詞の分類
#         if word.POS == "名詞":
#             if word.POS_s1 == "普通名詞" and word.POS_s2 == "サ変可能":
#                 word.POS = "サ変名詞"
#             elif word.POS_s1 == "普通名詞" and (word.POS_s2 == "形状詞可能" or word.POS_s2 == "サ変形状詞可能"):
#                 word.POS = "形状詞"

#         word_dic[word.POS].append(word)

#     return template("show_words", word_dic=word_dic)

# @get('/api/tokenize')
# def tokenize():
#     """
#     GETリクエストで送られてきた単語を分割し、返す
#     """
#     text = request.query.input_text
#     if text == "":
#         result = ""
#     else:
#         result = easy_japanese.parse2web_register(text)

#     body = json.dumps(result)
#     r = HTTPResponse(status=200, body=body)
#     r.set_header('Content-Type', 'application/json')
#     return r

# @post('/api/check_easy')
# def check_easy():
#     """
#     形態素を選択した際に、記録を反映する。
#     """
#     unidic_id = request.json['unidic_id']
#     surface = request.json['surface']

#     morph_type = easy_japanese.change_easy(unidic_id, surface)

#     body = json.dumps(morph_type)
#     r = HTTPResponse(status=200, body=body)
#     r.set_header('Content-Type', 'application/json')
#     return r

# @get('/api/easy_morph_count')
# def get_number_of_easy_morph():
#     """
#     """
#     number = easy_japanese.get_number_of_easy_morph()
#     body = json.dumps(number)
#     r = HTTPResponse(status=200, body=body)
#     r.set_header('Content-Type', 'application/json')
#     return r



# # 文編集
# @route('/edit_sentence')
# def route_edit_sentence():
#     return template("edit_sentence", users=easy_japanese.get_users())
