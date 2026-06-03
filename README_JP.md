# Yone Discord Bot

[Read in English >](./README.md)

## 概要

Yone Discord Bot (Python版) のオープンソース版です。

## 利用方法

1. モジュールをインストールする

```
pip install -r requirements.txt
```

2. Configを設定する

- [必須] `src/data/config.py` の `"discordBotConfig" = {"Token": "Your Token"}` にDiscord Botトークンを指定します。正しく指定されていない場合は動作しません。  
- [推奨] 必要に応じて、その他の定数も指定します。

3. 実行

```
python -m src
```

## 開発

手動で依存モジュールをインストール:
```
uv sync
```

## ライセンス

[Apache License 2.0](./LICENSE) のもとでライセンスされます。

Copyright © よね/Yone
