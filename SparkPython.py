import SparkApi
from flask_cors import CORS
from flask import Flask, request, jsonify, Response
import threading
from datetime import datetime

from Task import run_scheduler
from fileIo import read_tou_tiao_hot, write_tou_tiao_hot

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

ganswer = []
answerLen = 0
# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "5ad1cf2f"  # 填写控制台中获取的 APPID 信息
api_secret = "5fa688019c7eef19f159b90f68195a15"  # 填写控制台中获取的 APISecret 信息
api_key = "b329304e215f13d57369a0a7f2ffa1a8"  # 填写控制台中获取的 APIKey 信息
domain = "general"  # v3.0版本
Spark_url = 'wss://spark-api.xf-yun.com/v1.1/chat'  # v3.5环服务地址


# 主动买
@app.route('/chat', methods=['POST'])
def ask():
    print(request)
    data = request.json
    question = data.get('message')
    print(question)
    question = SparkApi.checklen(SparkApi.getText("user", question))
    SparkApi.answer = ""
    print("星火:", end="")
    thread = threading.Thread(target=SparkApi.main, args=(appid, api_key, api_secret, Spark_url, domain, question))
    thread.start()

    # SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    def generate():
        global ganswer
        ganswer = []
        cut = False
        try:
            while True:
                if cut:
                    break
                for item in SparkApi.string_set:
                    if item in ganswer:
                        continue
                    else:
                        if item != 'quit' and len(item) > 0:
                            ganswer.append(item)
                            yield f"{item}"
                    if item == 'quit':
                        cut = True
                        break
            # print('\n'+SparkApi.answer)
            SparkApi.getText("assistant", SparkApi.answer)
        except GeneratorExit:
            print("Client closed connection")
        except Exception as e:
            print(f"An error occurred: {e}")

    return Response(generate(), mimetype='text/event-stream')

    # return jsonify({
    #     "message": "Successfully bought stock",
    #     "response": SparkApi.answer,
    # }), 200


@app.route('/v1/dailyInsight', methods=['GET'])
def daily_insight():
    print(request)
    my_map = read_tou_tiao_hot()
    key, data = find_max_date_element(my_map)
    # 检查请求是否成功
    if len(data) > 0:
        # 解析响应内容
        return jsonify({
            "message": "Successfully bought stock",
            "response": data
        }), 200
    else:
        return jsonify({
            "message": "Failed",
            "response": "",
        }), 500


# 将日期字符串转换为 datetime 对象，并找到最大日期
def find_max_date_element(data_dict):
    # 解析日期字符串为 datetime 对象
    date_format = '%Y-%m-%d'
    dates = {datetime.strptime(key, date_format): key for key, date_str in data_dict.items()}
    # 找到最大日期
    max_date = max(dates.keys())
    # 获取最大日期对应的字典键
    max_date_key = dates[max_date]
    # 返回最大日期和对应的值
    return max_date_key, data_dict[max_date_key]

if __name__ == '__main__':
    # 在单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # 启动Flask应用
    app.run(host='0.0.0.0', port=30999)
