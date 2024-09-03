# Yone Discord Bot

[→ English](./README.md)

## 概要

Yone Discord Bot (Python版) のオープンソース版です。

## 利用方法

1. インストール

`requirements.txt` に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストールします。

```
pip install -r requirements.txt
```

2. Configを設定

`src/data/config.py` の `"discordBotConfig" = {"Token": "Your Token"}` にDiscord Botトークンを指定します。正しく指定されていない場合は動作しません。  
必要に応じて、その他の定数も指定します。

3. 実行

```
python -m YoneDiscordBot
```

## ライセンス

[Apache License 2.0](./LICENSE) のもとでライセンスされます。

Copyright (C) よね/Yone
