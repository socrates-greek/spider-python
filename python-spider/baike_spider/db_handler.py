#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
class Dbhandler(object):

    age = 0

    def __init__(self, age=22):
        self.age = age

    def dbconnect(self):

        # 打开数据库连接
        conn = pymysql.connect("localhost", "root", "root", "godzilla", charset='utf8')
        # 使用cursor()方法获取操作游标
        return conn

    def dbclose(self,conn):
        if conn is not None:
            conn.close()
