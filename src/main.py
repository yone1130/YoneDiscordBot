#
# main.py | Yone Discord Bot
#
# (c) 2022 よね/Yone
# licensed under the Apache License 2.0
#

import os

import discord
from discord.ext import commands
from dislash import InteractionClient, Option, OptionType

from data import config, config_global


# -------------------- Init -------------------- #

os.system('cls')
print(
  f"Yone Discord Bot\n"+\
  f"(c) 2022 よね/Yone\n\n"+\
  f"discord.py  Ver {discord.__version__}\n\n"+\
  f"--------------------\n"
)

#discord インスタンス生成
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '/', intents=intents)

#dislash インスタンス生成
slash = InteractionClient(bot)


# -------------------- Functions -------------------- #
# ---------- On ready ---------- #
@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Game(name=""))
    print(">Ready.  Waiting for any command and message\n")


# ---------- Commands ---------- #
# ----- info ----- #
@slash.slash_command(
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
    name='Ver 1.0.0',
    value='(c) 2022 よね/Yone\n'+
          '不具合等の連絡は <@892376684093898772> までお願いいたします。'
  )
  await inter.reply(embed=embed)
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

  #引数が指定されていない場合
  if title == None:
    title = ""
  if description == None: 
    description = ""
  if color == None:
    color="40ff00"

  #必須引数が指定されていない場合
  if name == None:
    await inter.reply("引数name は必須項目です。")
    return
  if value == None:
    await inter.reply("引数value は必須項目です。")
    return

  #変数colorを16進数に変換
  try:
    color = int(color, 16)
  except Exception as e:
    await inter.reply("引数color が16進数RGB型ではありません。（例: 40ff40）")
    return

  #embed生成
  embed = discord.Embed(
    title=title,
    color=color,
    description=description
  )
  embed.add_field(
    name=name,
    value=value
  )

  #送信
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

  #引数が不足している場合
  if category_id == None or channel_name == None:
    await inter.reply(f"すべての引数を入力してください。")
    return

  #カテゴリの取得
  category_id = int(category_id)
  category = bot.get_channel(category_id)

  #引数カテゴリIDに誤りがある場合
  if category == None:
    await inter.reply("カテゴリIDを正しく入力してください。")
    return

  #引数カテゴリがコマンド実行時のサーバーでない場合
  if inter.guild != category.guild:
    await inter.reply("他のサーバーを登録することはできません。")
    return

  #チャンネルの作成
  try:
    ch = await category.create_text_channel(name=channel_name)

  #チャンネルの作成 失敗時
  except Exception as e:
    await inter.reply("チャンネルを作成できませんでした。")
    return

  #完了メッセージの送信
  await inter.reply(f"グローバルチャットのチャンネルが登録されました。{ch.mention}")

  #リストに追加
  print(
    "[新規チャンネル登録]\n"+\
    f"chan ID   : {ch.id}\n"+\
    f"chan name : {ch.name}\n"+\
    f"sever name: {ch.guild.name}\n"
  )
  config_global.globalChannels.append(ch.id)

  #すべての登録されているチャンネルへ送信
  for chan in config_global.globalChannels:

    channel = bot.get_channel(chan)

    # --- 送信部分 --- #

    #embed color
    color = 0x40ff40

    #embed生成
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
      return


# ----- messages ----- #
@bot.event
async def on_message(message):

  #送信者がbotの場合は処理しない
  if message.author.bot:
    return

  #グローバルチャット内での送信の場合
  if message.channel.id in config_global.globalChannels:

    #BANされている場合
    if message.author.id in config_global.globalBanList:
      await message.reply("あなたはグローバルチャット内においてBANされているため送信できません。")
      return

    #すべての登録されているチャンネルへ送信
    for chan in config_global.globalChannels:

      print(chan)
      print(message.channel.id)
      print("\n")

      # 送信元には送信しない
      if message.channel.id == chan:
        continue

      channel = bot.get_channel(chan)

      # --- 送信部分 --- #

      #embed color
      color = 0x40ff40

      #embed生成
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

      #添付ファイルが含まれる場合
      if message.attachments != []:
        embed.description += "\n(添付ファイル)"
        embed.set_image(url=message.attachments[0].proxy_url)

      try:
        await channel.send(embed=embed)  # 送信
      except Exception as e:
        await message.reply("送信エラーが発生しました。")
        print(chan)
        print(e)

  return


# ----- Check ----- #
@slash.slash_command(
  name = 'global-chk',
  description = 'グローバルチャットの登録数の確認'
)
async def initGlobal(inter):

  content = ""

  #embed color
  color = 0x40ff40

  #embed生成
  embed = discord.Embed(
    title=f"グローバルチャットの登録数：{str(len(config_global.globalChannels))}",
    color=color,
    description=content
  )

  #すべての登録されているチャンネルをスクレイピング
  for chan in config_global.globalChannels:

    channel = bot.get_channel(chan)

    embed.add_field(
      name=channel.guild.name,
      value=channel.name
    )

  await inter.reply(embed=embed)
  return


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
