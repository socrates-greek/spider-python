import tornado
import threading

import yaml

from Task import run_scheduler
from src.WbsocketServer import make_app, fetch_emails_163, fetch_emails_simba
from src.configs import Config
from src.mysql.mysqldb import Database, load_file


def check_email_loop_163():
    fetch_emails_163()
    tornado.ioloop.IOLoop.current().call_later(60 * 10, check_email_loop_163)


def check_email_loop_simba():
    fetch_emails_simba()
    tornado.ioloop.IOLoop.current().call_later(30, check_email_loop_simba)


if __name__ == '__main__':
    # 这里可以加载配置
    Config.load('./config.yaml')
    # 访问配置项
    host = Config.get('host')
    port = Config.get('port')

    # 邮件发送配置
    url = Config.get('mysql')['url']
    username = Config.get('mysql')['username']
    password = Config.get('mysql')['password']
    database = Config.get('mysql')['database']

    Database.connect(url, username, password, database)
    # 在单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app = make_app()
    app.listen(port)  # 在 8888 端口启动服务
    print("WebSocket server is running on ws://localhost:30999/ws")

    # 在 IOLoop 中开始定时任务
    tornado.ioloop.IOLoop.current().call_later(0, check_email_loop_163)
    tornado.ioloop.IOLoop.current().call_later(0, check_email_loop_simba)
    tornado.ioloop.IOLoop.current().start()
