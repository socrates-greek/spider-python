import tornado
import threading

import yaml

from Task import run_scheduler
from WbsocketServer import make_app, fetch_emails_163, fetch_emails_simba
from src.mysql.mysqldb import Database, load_file


def check_email_loop_163():
    fetch_emails_163()
    tornado.ioloop.IOLoop.current().call_later(60 * 10, check_email_loop_163)


def check_email_loop_simba():
    fetch_emails_simba()
    tornado.ioloop.IOLoop.current().call_later(30, check_email_loop_simba)


with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
# 邮件发送配置
url = config['mysql']['url']
username = config['mysql']['username']
password = config['mysql']['password']
database = config['mysql']['database']


if __name__ == '__main__':
    Database.connect(url, username, password, database)
    # 在单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app = make_app()
    app.listen(30999)  # 在 8888 端口启动服务
    print("WebSocket server is running on ws://localhost:30999/ws")

    # 在 IOLoop 中开始定时任务
    tornado.ioloop.IOLoop.current().call_later(0, check_email_loop_163)
    tornado.ioloop.IOLoop.current().call_later(0, check_email_loop_simba)
    tornado.ioloop.IOLoop.current().start()
