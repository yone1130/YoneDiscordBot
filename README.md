
# Yone Discord Bot

## Overview

Yone Discord Bot (Python版) のオープンソース版です。

## Usage

1. インストール

`requirements.txt` に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストールします。

```
pip install -r requirements.txt
```

2. Configを設定

`src/data/config.py` の `"discordBotConfig" {"Token": "Your Token"}` にDiscord Botトークンを指定します。正しく指定されていない場合は動作しません。必要に応じて、その他の定数も指定します。

3. 実行

以下のコマンドを使用してプロジェクトを実行します。

```
python -m YoneDiscordBot
```

## LICENSE

Licensed under the [Apache License 2.0](https://github.com/yone1130/YoneDiscordBot/blob/main/LICENSE).

Copyright (c) よね/Yone
