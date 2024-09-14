import tornado

# import SparkApi
# from flask_cors import CORS
# from flask import Flask, request, jsonify, Response
# from fileIo import read_tou_tiao_hot, write_tou_tiao_hot
# from datetime import datetime
import threading
from Task import run_scheduler
from WbsocketServer import make_app




if __name__ == '__main__':
    # 在单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app = make_app()
    app.listen(30999)  # 在 8888 端口启动服务
    print("WebSocket server is running on ws://localhost:30999/ws")
    # 在 5 秒后，主动发送消息给所有客户端
    # def send_periodic_message():
    #     MyWebSocketHandler.send_message_to_clients("Hello from server")
    # tornado.ioloop.PeriodicCallback(send_periodic_message, 5000).start()
    tornado.ioloop.IOLoop.current().start()
