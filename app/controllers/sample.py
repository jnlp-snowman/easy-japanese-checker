# -*- coding: utf-8 -*-

import json
from bottle import route, template, post, get, request, HTTPResponse

import your_tool
from easy_japanese import EasyJapanese, MecabTagger

TAGGER_DIR = "-d /Users/takahashi/work/mecab_systemdic"
easy_japanese = EasyJapanese(TAGGER_DIR)

@route('/')
def index():
    """
    Welcome page
    """
    return template("sample")

@get('/api/analyzer')
def return_analysis_result():
    """
    Example of analyzer API(GET)
    """
    # Get submitted contents.
    text = request.query.input_text
    # Analyze.
    _text = your_tool.lowercase(text)

    # Make a request.
    body = json.dumps(_text)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/tokenize')
def tokenize():
    """
    """
    text = request.query.input_text
    # wakati_text = tagger.parse2wakati(text)
    result = easy_japanese.parse2web_register(text)

    body = json.dumps(result)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r
