
# Yone Discord Bot

## About

Open source version of Yone Discord Bot (Python version).
Yone Discord Bot (Python版) のオープンソース版です。

## Usage Technology

#### Langages / Libraries / Modules
- Python3
- discord.py v2.3

## How to Use

1. 必要なモジュールをインストール

[./requirements.txt](https://github.com/yone1130/YoneDiscordBot/blob/main/requirements.txt) に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストールする。

```
$ pip install -r requirements.txt
```

2. Configを設定

[./src/data/config.py](https://github.com/yone1130/YoneDiscordBot/blob/main/src/data/config.py) の `"discordBotConfig" {"Token": "Your Token"}` にDiscord Botトークンを指定する。正しく指定されていない場合は動作しない。必要に応じて、その他の定数も指定する。

3. プロジェクトを実行

```
$ python -m YoneDiscordBot
```

## LICENSE
Apache License 2.0
[License File](https://github.com/yone1130/YoneDiscordBot/blob/main/LICENSE)