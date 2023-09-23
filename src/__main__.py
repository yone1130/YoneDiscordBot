
"""

__main__.py | Yone Discord Bot

(c) 2022-2023 よね/Yone

Licensed under the Apache License 2.0

"""

import datetime
import math
import os
import sqlite3

import discord
import requests
from bs4 import BeautifulSoup

from data import config
from database import BotDatabase

# -------------------- Init -------------------- #
clearConsole = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")
clearConsole()

print(
    f"Yone Discord Bot  Ver {config.appConfig['version']}\n"
    + f"(c) 2022-2023 よね/Yone\n\n"
    + f"discord.py  Ver {discord.__version__}\n\n"
    + f"--------------------\n"
)

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
cmdTree = discord.app_commands.CommandTree(client=client)

database = BotDatabase()


class Isday:
    def __init__(self, url):
        self.url = url

    def get(self):
        res = requests.get(self.url)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")

            elemName = soup.select("#dateDtl > dt > span")
            elemDes = soup.select("#dateDtl > dd")
            name = elemName[0].contents[0]
            des = elemDes[0].contents[0]

            return True, name, des

        else:
            print(f"Cannot get. HTTP {res.status_code}")
            return False, None, None


# -------------------- Functions -------------------- #
# ---------- On ready ---------- #
@client.event
async def on_ready():
    await cmdTree.sync()
    print(">Ready.  Waiting for any command and message\n")
    return


# ---------- Commands ---------- #
@discord.app_commands.guilds(discord.Object(id=1053378444781703339))


# ----- info ----- #
@cmdTree.command(
    name="info",
    description="情報表示",
)
async def info(inter):
    embed = discord.Embed(title="Yone Discord Bot", color=0x40FF40, description="")
    embed.add_field(
        name=f"Ver {config.appConfig['version']}",
        value="Copyright (c) 2022-2023 よね/Yone\n" + "不具合等の連絡は <@892376684093898772> までお願いいたします。",
    )
    await inter.response.send_message(embed=embed)

    return


@cmdTree.command(
    name="guilds",
    description="Botが参加しているサーバーを表示"
)
async def guilds(inter: discord.Interaction):
    try:
        num_servers = len(client.guilds)
        embed = discord.Embed(
            title=f"Yone Discord Bot",
            description=f"導入サーバー数: {num_servers}",
            color=0x40f040
        )
        
        for guild in client.guilds:
            embed.add_field(
                name=guild.name,
                value=f"オーナー: {guild.owner.mention} ({guild.owner.name})"
            )

        await inter.response.send_message(embed=embed)

        return

    except Exception as error:
        embed = discord.Embed(
            title="エラー",
            description=f"ハンドルされない例外が発生しました。\n```{error}```",
            color=0xf04040
        )

        await inter.response.send_message(
            embed=embed,
            ephemeral=True
        )
        return


# ----- Embed ----- #
@cmdTree.command(name="embed", description="embedメッセージを生成")
@discord.app_commands.describe(
    title="タイトル", description="概要", color="16進数RGB型（例: 40ff40）"
)
async def embed(
    inter: discord.Interaction, description: str, title: str = None, color: str = None
):
    if title == None:
        title = ""

    if description == None:
        description = ""

    if color == None:
        color = "40ff00"

    try:
        color = int(color, 16)

    except Exception as e:
        await inter.response.send_message(
            "引数color が16進数RGB型ではありません。（例: 40ff40）", ephemeral=True
        )
        return

    embed = discord.Embed(title=title, color=color, description=description)

    await inter.response.send_message(embed=embed)

    return


# ----- messages ----- #
@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # ---------- Ranking ---------- #
    if message.guild.id in [1053378444781703339, 1053360115417354401]:
        try:
            data = database.get_rank(user=message.author.id)

            if (not data) or (data is None):
                database.insert_rank(user=message.author.id)

            level = int(data[0][1])
            point = int(data[0][3])
            msg_cnt = int(data[0][4])
            letter_cnt = int(data[0][5])

            addPoint = math.floor(1 + len(message.content) / 20)
            total_point = int(data[0][2]) + addPoint
            point = point + addPoint
            msg_cnt = msg_cnt + 1
            letter_cnt = letter_cnt + len(message.content)

            if point >= (level**2):
                level = level + 1
                point = 0

            database.update_rank(
                user=message.author.id,
                level=level,
                total_point=total_point,
                point=point,
                msg_cnt=msg_cnt,
                letter_cnt=letter_cnt
            )

        except Exception as e:
            print(f"[ERROR] {e}")

    return


# ----- isday ----- #
@cmdTree.command(
    name="isday",
    description="今日は何の日かを送信",
)
async def isday(inter: discord.Interaction):
    bs = Isday(url="https://kids.yahoo.co.jp/today/")
    status, name, des = bs.get()

    if status:
        print(f"{name}\n{des}")

        nowDate = datetime.datetime.now()
        nowDate = nowDate.strftime("%Y年%m月%d日")

        embed = discord.Embed(
            title="今日は何の日", color=0x40FF40, description=f"{nowDate}\n"
        )
        embed.add_field(name=f"今日は {name}\n\n", value=f"{des}")
        await inter.response.send_message(embed=embed)

        return

    else:
        embed = discord.Embed(
            title="エラーが発生しました。", color=0xFF4040, description="取得に失敗しました。"
        )
        embed.set_footer(text=f"エラーコード: 0x0201")
        await inter.response.send_message(embed=embed)

        return


# ----- lv ----- #
@cmdTree.command(
    name="lv",
    description="指定ユーザーの現在のレベルとポイントを表示",
)
async def rank(inter: discord.Interaction, user: discord.Member):
    try:
        data = database.get_rank(user=user)

    except Exception as e:
        await inter.response.send_message(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xFF4040,
                description=f"データベースの読み込みに失敗しました。```{e}```",
            ).set_footer(text=f"エラーコード: 0x0301"),
            ephemeral=True,
        )
        return

    if not data:
        await inter.response.send_message(
            embed=discord.Embed(
                title="Level", color=0x40FF40, description=f"{user.mention}\n"
            )
            .add_field(name="レベル", value="1")
            .add_field(name="ポイント", value="0")
        )
    else:
        level = int(data[0][1])
        total_point = int(data[0][2])
        point = int(data[0][3])

        await inter.response.send_message(
            embed=discord.Embed(
                title="Level", color=0x40FF40, description=f"{user.mention}\n"
            )
            .add_field(name="レベル", value=f"{level}")
            .add_field(
                name="ポイント (レベルごと)",
                value=f"{point} / {level ** 2}\n"
                + f"(レベルアップまであと: {(level ** 2) - point}ポイント)",
            )
            .add_field(name="累計ポイント", value=total_point)
        )

    return


# ---------- RUN ---------- #
client.run(config.discordBotConfig["Token"])  # Login
