"""

__main__.py | Yone Discord Bot

(c) 2022-2023 よね/Yone
licensed under the Apache License 2.0

"""
import os
import datetime
import requests
from bs4 import BeautifulSoup
import discord
from data import config


# -------------------- Init -------------------- #
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

print(
    f"Yone Discord Bot  Ver {config.appConfig['version']}\n"+\
    f"(c) 2022 よね/Yone\n\n"+\
    f"discord.py  Ver {discord.__version__}\n\n"+\
    f"--------------------\n"
)

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
cmdTree = discord.app_commands.CommandTree(client=client)

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
    name = 'info',
    description = '情報表示',
)
async def info(inter):
    embed = discord.Embed(
        title="Yone Bot",
        color= 0x40ff40,
        description=""
    )
    embed.add_field(
        name=f'Ver {config.version}',
        value='(c) 2022-2023 よね/Yone\n'+
              '不具合等の連絡は <@892376684093898772> までお願いいたします。'
    )
    await inter.response.send_message(embed=embed)

    return


# ----- Embed ----- #
@cmdTree.command(
    name = 'embed',
    description = 'embedメッセージを生成'
)
@discord.app_commands.describe(
    title="タイトル",
    description="概要",
    color="16進数RGB型（例: 40ff40）"
)
async def embed(inter: discord.Interaction, description:str, title:str=None, color:str=None):
    if title == None:
        title = ""

    if description == None: 
        description = ""

    if color == None:
        color="40ff00"

    try:
        color = int(color, 16)

    except Exception as e:
        await inter.response.send_message("引数color が16進数RGB型ではありません。（例: 40ff40）", ephemeral=True)
        return

    embed = discord.Embed(
        title=title,
        color=color,
        description=description
    )

    await inter.response.send_message(embed=embed)

    return


# ----- messages ----- #
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # ---------- Global Chat ---------- #
    if message.channel.id in config.discordBotConfig['globalChannels']:
        if message.author.id in config.discordBotConfig['globalBanList']:
            await message.reply("あなたはグローバルチャット内においてBANされているため送信できません。")
            return

        for chan in config.discordBotConfig['globalChannels']:
            if message.channel.id == chan:
                continue

            channel = client.get_channel(chan)
            color   = 0x40ff40

            embed = discord.Embed(
                title="",
                color=color,
                description=message.content
            )
            embed.set_author(
                name=message.author.name,
                # url="",
                # icon_url=message.author.avatar_url
            )
            embed.set_footer(text=message.guild.name)#, icon_url=message.guild.icon_url)

            if message.attachments != []:
                embed.description += "\n(添付ファイル)"
                embed.set_image(url=message.attachments[0].proxy_url)

            try:
                await channel.send(embed=embed)

            except Exception as e:
                await message.reply("送信エラーが発生しました。")
                print(chan)
                print(e)

    elif message.guild.id in config.discordBotConfig['globalBanList']:
        await message.reply("このサーバーはグローバルチャット内においてBANされているため送信できません。")
        return

    return


# ----- isday ----- #
@cmdTree.command(
    name = 'isday',
    description = '今日は何の日かを送信します。',
)
async def isday(inter: discord.Interaction):
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
        await inter.response.send_message(embed=embed)

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
        await inter.response.send_message(embed=embed)

        return


# ----------------------------------------------------- #
# -------------------- Global Chat -------------------- #
# ----------------------------------------------------- #

# ----- Init ----- #
@cmdTree.command(
  name = 'global-init',
  description = 'グローバルチャットの登録'
)
@discord.app_commands.describe(
    category_id="グローバルチャットのチャンネルを作成するカテゴリID",
    channel_name="作成するグローバルチャットのチャンネル名"
)
async def initGlobal(inter: discord.Interaction, category_id:str, channel_name:str):
    category_id = int(category_id)
    category    = client.get_channel(category_id)

    if category == None:
        await inter.response.send_message("カテゴリIDを正しく入力してください。", ephemeral=True)
        return
    if inter.guild != category.guild:
        await inter.response.send_message("他のサーバーを登録することはできません。", ephemeral=True)
        return

    try:
        ch = await category.create_text_channel(name=channel_name)
    except Exception as e:
        await inter.response.send_message(
            embed=discord.Embed(
                title="エラーが発生しました",
                color= 0xff4040,
                description= "チャンネルを作成できませんでした。"
            )
            .set_footer(
                text=f"エラーコード: 0x0301"
            ),
            ephemeral=True
        )
        return

    await inter.response.send_message(f"グローバルチャットのチャンネルが登録されました。{ch.mention}")

    print(
        "[新規チャンネル登録]\n"+\
        f"chan ID   : {ch.id}\n"+\
        f"chan name : {ch.name}\n"+\
        f"sever name: {ch.guild.name}\n"
    )
    config.discordBotConfig['globalChannels'].append(ch.id)

    for chan in config.discordBotConfig['globalChannels']:
        channel = client.get_channel(chan)
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
            await inter.response.send_message("一部のサーバーに送信できませんでした。", ephemeral=True)
            continue


# ----- Check ----- #
@cmdTree.command(
  name = 'global-chk',
  description = 'グローバルチャットの登録数の確認'
)
async def initGlobal(inter: discord.Interaction):
    content = ""
    color   = 0x40ff40

    embed = discord.Embed(
        title=f"グローバルチャットの登録数：{str(len(config.discordBotConfig['globalChannels']))}",
        color=color,
        description=content
    )

    for chan in config.discordBotConfig['globalChannels']:
        channel = client.get_channel(chan)

        embed.add_field(
            name=channel.guild.name,
            value=channel.name
        )

    await inter.response.send_message(embed=embed)

    return


# ---------- RUN ---------- #
client.run(config.discordBotConfig['Token'])  # Login

