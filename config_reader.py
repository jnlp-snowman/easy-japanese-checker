# -*- coding: utf-8 -*-
import configparser
import os

def read_config():
    """
    コンフィグファイルの読み込み
    """
    # 絶対パスを取得
    base = os.path.dirname(os.path.abspath(__file__))
    path_to_configfile = os.path.join(base, 'config.ini')

    # コンフィグファイルを読み込み、返す
    config = configparser.ConfigParser()
    config.sections()
    config.read(path_to_configfile)

    return config
