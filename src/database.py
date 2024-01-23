"""

Yone Discord Bot

Copyright (c) よね/Yone

Licensed under the Apache License 2.0.

"""

import sqlite3
import discord
from data import config

class BotDatabase:
    def __init__(self) -> None:
        self.database_file = config.discordBotConfig['databaseFilePath']
        self.create_table()


    def connect(self) -> sqlite3.Connection:
        """データベース接続"""
        return sqlite3.connect(self.database_file)


    def cursor(
        self,
        *,
        connect: sqlite3.Connection
    ) -> sqlite3.Cursor:
        """データベースカーソルインスタンスを生成"""
        return connect.cursor()


    def save(
        self,
        *,
        connect: sqlite3.Connection
    ) -> None:
        """データベース保存

        データベース操作内容のコミットおよびクローズを行う
        """
        connect.commit()
        connect.close()


    def create_table(self) -> None:
        """データベースのテーブル作成"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute("CREATE TABLE IF NOT EXISTS rank(uid, level, totalPoint, point, msgCnt, ltrCnt)")
        self.save(connect=db_con)


    def get_rank(self, *, user: discord.User.id) -> list:
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(f"SELECT uid, level, totalPoint, point, msgCnt, ltrCnt FROM rank WHERE uid='{user}'")
        data = db_cur.fetchall()
        self.save(connect=db_con)
        return data
    

    def insert_rank(self, *, user: discord.User.id) -> None:
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        insertData = (str(user), 1, 0, 0, 0, 0)
        db_cur.execute("INSERT INTO rank VALUES(?, ?, ?, ?, ?, ?)", insertData)
        self.save(connect=db_con)


    def update_rank(self, *, user: discord.User.id, level: int, total_point: int, point: int, msg_cnt: int, letter_cnt: int) -> None:
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(f"UPDATE rank SET level='{level}', totalPoint='{total_point}', point='{point}', msgCnt='{msg_cnt}', ltrCnt='{letter_cnt}' WHERE uid='{str(user)}'")
        self.save(connect=db_con)