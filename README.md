# Yone Discord Bot

[日本語で読む >](./README_JP.md)

## Overview

Open source version of Yone Discord Bot (for Python).

## Usage

1. Install modules

```
pip install -r requirements.txt
```

2. Setup Config

- [Required] Specify the Discord Bot token in `"discordBotConfig" = {"Token": "Your Token"}` in `src/data/config.py`. If not specified correctly, it will not work.  
- [Recommended] Specify other constants as needed.

3. Run

```
python -m src
```

## Development

Manually install dependencies:
```
uv sync
```

## License

Licensed under the [Apache License 2.0](./LICENSE).

Copyright © よね/Yone
