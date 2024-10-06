# @app.route('/v1/dailyInsight', methods=['GET'])
from datetime import datetime
import tornado.web
import tornado.websocket

from src.FileIo import read_tou_tiao_hot


# HTTP 处理器
class DaliyHotHandler(tornado.web.RequestHandler):
    # 处理 GET 请求
    def get(self):
        result = daily_insight()
        self.write(result)
        self.flush()

def daily_insight():
    my_map = read_tou_tiao_hot()
    key, data = find_max_date_element(my_map)
    # 检查请求是否成功
    if len(data) > 0:
        # 解析响应内容
        return {
            "message": "Successfully bought stock",
            "response": data
        }
    else:
        return {
            "message": "Failed",
            "response": "",
        }


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

