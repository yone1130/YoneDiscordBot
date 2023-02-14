#
# main.py | Yone Discord Bot
#
# (c) 2022-2023 よね/Yone
# licensed under the Apache License 2.0
#

import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from dislash import InteractionClient, Option, OptionType
from data import config, config_global

# -------------------- Init -------------------- #
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

print(
    f"Yone Discord Bot  Ver {config.version}\n"+\
    f"(c) 2022 よね/Yone\n\n"+\
    f"discord.py  Ver {discord.__version__}\n\n"+\
    f"--------------------\n"
)

intents = discord.Intents.all()
bot     = commands.Bot(command_prefix = '/', intents=intents)
slash   = InteractionClient(bot)

class Isday:
    def __init__(self, url):
        self.url = url

    def get(self):
        res = requests.get(self.url)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")

            elemName = soup.select('#dateDtl > dt > span')
            elemDes = soup.select('#dateDtl > dd')
            name = elemName[0].contents[0]
            des = elemDes[0].contents[0]

            return True, name, des

        else:
            print(f"Cannot get. HTTP {res.status_code}")
            return False, None, None

cooldownTime = 10
cmdUseLast   = -1

# -------------------- Functions -------------------- #
# ---------- On ready ---------- #
@bot.event
async def on_ready():
    print(">Ready.  Waiting for any command and message\n")

# ---------- Commands ---------- #
def chkCooldown():
    global cmdUseLast

    nowTime = time.time()

    if not(nowTime - cmdUseLast <= cooldownTime):
        cmdUseLast = nowTime
        return True, None

    else:
        return False, int(cooldownTime - (nowTime - cmdUseLast))

# ----- Too many ----- #
async def tooMany(inter, time):
    await inter.reply(
        embed=discord.Embed(
            title="エラーが発生しました",
            color= 0xff4040,
            description= "コマンドの実行頻度が多すぎます。\n"+
                        f"約{time}秒間お待ちください。"
        )
        .set_footer(
            text=f"エラーコード: 0x0201"
        )
    )
    return

# ----- info ----- #
@slash.slash_command(
    name = 'info',
    description = '情報表示',
)
async def info(inter):
    isCooldown, time = chkCooldown()

    if isCooldown:
        embed = discord.Embed(
        title="Yone Bot",
            color= 0x40ff40,
            description=""
        )
        embed.add_field(
            name=f'Ver {config.version}',
            value='(c) 2022 よね/Yone\n'+
                    '不具合等の連絡は <@892376684093898772> までお願いいたします。'
        )
        await inter.reply(embed=embed)

        return

    else:
        await tooMany(inter, time)
        return

# ----- Embed ----- #
@slash.slash_command(
    name = 'embed',
    description = 'embedメッセージを生成',
    options=[
        Option("title", "タイトル（任意）", OptionType.STRING),
        Option("description", "概要（任意）", OptionType.STRING),
        Option("name", "タイトル（必須）", OptionType.STRING),
        Option("value", "本文（必須）", OptionType.STRING),
        Option("color", "16進数RGB型（例: 40ff40）（任意）", OptionType.STRING),
    ]
)
async def embed(inter, title=None, description=None, name=None, value=None, color=None):
    isCooldown, time = chkCooldown()

    if isCooldown:
        if title == None:
            title = ""

        if description == None: 
            description = ""

        if color == None:
            color="40ff00"

        if name == None:
            await inter.reply("引数name は必須項目です。")
            return

        if value == None:
            await inter.reply("引数value は必須項目です。")
            return

        try:
            color = int(color, 16)

        except Exception as e:
            await inter.reply("引数color が16進数RGB型ではありません。（例: 40ff40）")
            return

        embed = discord.Embed(
            title=title,
            color=color,
            description=description
        )
        embed.add_field(
            name=name,
            value=value
        )
        await inter.reply(embed=embed)

        return

    else:
        await tooMany(inter, time)
        return

# ----- messages ----- #
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ---------- Global Chat ---------- #
    if message.channel.id in config_global.globalChannels:
        if message.author.id in config_global.globalBanList:
            await message.reply("あなたはグローバルチャット内においてBANされているため送信できません。")
            return

        for chan in config_global.globalChannels:
            if message.channel.id == chan:
                continue

            channel = bot.get_channel(chan)
            color   = 0x40ff40

            embed = discord.Embed(
                title="",
                color=color,
                description=message.content
            )
            embed.set_author(
                name=message.author.name,
                # url="",
                icon_url=message.author.avatar_url
            )
            embed.set_footer(text=message.guild.name, icon_url=message.guild.icon_url)

            if message.attachments != []:
                embed.description += "\n(添付ファイル)"
                embed.set_image(url=message.attachments[0].proxy_url)

            try:
                await channel.send(embed=embed)

            except Exception as e:
                await message.reply("送信エラーが発生しました。")
                print(chan)
                print(e)

    elif message.guild.id in config_global.globalChannels:
        await message.reply("このサーバーはグローバルチャット内においてBANされているため送信できません。")
        return

    return

# ----- isday ----- #
@slash.slash_command(
    name = 'isday',
    description = '今日は何の日かを送信します。',
)
async def isday(inter):
    bs = Isday(url="https://kids.yahoo.co.jp/today/")
    status, name, des = bs.get()

    if status:
        print(f"{name}\n{des}")

        nowDate = datetime.datetime.now()
        nowDate = nowDate.strftime('%Y年%m月%d日')

        embed = discord.Embed(
        title="今日は何の日",
            color= 0x40ff40,
            description=f"{nowDate}\n"
        )
        embed.add_field(
            name=f"今日は {name}\n\n",
            value=f"{des}"
        )
        await inter.reply(embed=embed)

        return

    else:
        embed = discord.Embed(
            title="エラーが発生しました。",
            color= 0xff4040,
            description="取得に失敗しました。"
        )
        embed.set_footer(
            text=f"エラーコード: 0x0201"
        )
        await inter.reply(embed=embed)

        return

# ----------------------------------------------------- #
# -------------------- Global Chat -------------------- #
# ----------------------------------------------------- #

# ----- Init ----- #
@slash.slash_command(
  name = 'global-init',
  description = 'グローバルチャットの登録',
  options=[
    Option("category_id", "グローバルチャットのチャンネルを作成するカテゴリID", OptionType.STRING),
    Option("channel_name", "作成するグローバルチャットのチャンネル名", OptionType.STRING)
  ]
)
async def initGlobal(inter, category_id=None, channel_name=None):
    isCooldown, time = chkCooldown()

    if isCooldown:
        if category_id == None or channel_name == None:
            await inter.reply(f"すべての引数を入力してください。")
            return

        category_id = int(category_id)
        category    = bot.get_channel(category_id)

        if category == None:
            await inter.reply("カテゴリIDを正しく入力してください。")
            return

        if inter.guild != category.guild:
            await inter.reply("他のサーバーを登録することはできません。")
            return

        try:
            ch = await category.create_text_channel(name=channel_name)

        except Exception as e:
            await inter.reply(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color= 0xff4040,
                    description= "チャンネルを作成できませんでした。"
                )
                .set_footer(
                    text=f"エラーコード: 0x0301"
                )
            )
            return

        await inter.reply(f"グローバルチャットのチャンネルが登録されました。{ch.mention}")

        print(
            "[新規チャンネル登録]\n"+\
            f"chan ID   : {ch.id}\n"+\
            f"chan name : {ch.name}\n"+\
            f"sever name: {ch.guild.name}\n"
        )
        config_global.globalChannels.append(ch.id)

        for chan in config_global.globalChannels:
            channel = bot.get_channel(chan)
            color   = 0x40ff40

            embed = discord.Embed(
                title="新しいチャンネルが登録されました。",
                color=color,
                description=f"サーバー名　: {ch.guild.name}\n"+
                            f"チャンネル名: {ch.name}\n"
            )

            try:
                await channel.send(embed=embed)

            except Exception as e:
                await inter.reply("一部のサーバーに送信できませんでした。")
                continue

    else:
        await tooMany(inter, time)
        return

# ----- Check ----- #
@slash.slash_command(
  name = 'global-chk',
  description = 'グローバルチャットの登録数の確認'
)
async def initGlobal(inter):
    isCooldown, time = chkCooldown()

    if isCooldown:
        content = ""
        color   = 0x40ff40

        embed = discord.Embed(
            title=f"グローバルチャットの登録数：{str(len(config_global.globalChannels))}",
            color=color,
            description=content
        )

        for chan in config_global.globalChannels:
            channel = bot.get_channel(chan)

            embed.add_field(
                name=channel.guild.name,
                value=channel.name
            )

        await inter.reply(embed=embed)

        return

    else:
        await tooMany(inter, time)
        return

# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
