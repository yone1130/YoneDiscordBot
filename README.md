
# Yone Discord Bot

## About

Yone Discord Bot (Python版) のオープンソース版です。

## Usage Technology

#### Languages & Libraries
- Python3
- discord.py v2.3

## How to Use

1. 必要なモジュールをインストールする

[./requirements.txt](https://github.com/yone1130/YoneDiscordBot/blob/main/requirements.txt) に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストールします。

```
$ pip install -r requirements.txt
```

2. Configを設定する

[./src/data/config.py](https://github.com/yone1130/YoneDiscordBot/blob/main/src/data/config.py) の `"discordBotConfig" {"Token": "Your Token"}` にDiscord Botトークンを指定します。正しく指定されていない場合は動作しません。必要に応じて、その他の定数も指定します。

3. プロジェクトを実行する

以下のコマンドを使用してプロジェクトを実行します。

```
$ python -m YoneDiscordBot
```

## LICENSE
Licensed under the Apache License 2.0.
[License File](https://github.com/yone1130/YoneDiscordBot/blob/main/LICENSE)