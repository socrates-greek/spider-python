import tornado
import threading
from Task import run_scheduler
from WbsocketServer import make_app, fetch_emails_163, fetch_emails_simba


def check_email_loop_163():
    fetch_emails_163()
    tornado.ioloop.IOLoop.current().call_later(60 * 10, check_email_loop_163)


def check_email_loop_simba():
    fetch_emails_simba()
    tornado.ioloop.IOLoop.current().call_later(30, check_email_loop_simba)


if __name__ == '__main__':
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
