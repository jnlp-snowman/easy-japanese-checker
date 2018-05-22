# やさしい日本語チェッカーおよび語彙登録システム

![demonstration image](screen_shot.png)

# 概要
やさしい日本語チェッカーおよび語彙登録システムです。
入力された文を即座に解析し、辞書と照合を行います。
語がやさしい日本語辞書に含まれる場合は、青色で示されます。

やさしい日本語語彙登録モードもあり、ワンクリックにより語彙を追加することができます。

# 使い方

```sh
git clone https://github.com/jnlp-snowman/easy-japanese-checker.git
pip install -r requirements.txt
gunicorn -b 127.0.0.1:8000 -w 1 index:app
```

apacheで動かすときに、Proxyを使って転送しています。
現在さくらでは、[http://160.16.58.116/easy-japanese/](http://160.16.58.116/easy-japanese/)で利用できます。

- /, /checker
 - チェッカー
- /register
 - 登録モード
- /words
 - 登録した語の確認

## さくらサーバーでのコンフィグファイルの例
```ini
[settings]
mecab_systemdic = /snowmans/c_snowman/resources/mecab_systemdic/
mysql = mysql+pymysql://gakkai:gakkai@localhost/web_data?charset=utf8
```

# License
MIT License, see LICENSE for details.
