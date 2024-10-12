import os
import tornado.web
import json
from src.config.Configs import Config
from src.minios.minios import MinioStorage


def read_tou_tiao_hot():
    # 读取 CSV 文件
    file_name = '../data.json'
    # 检查文件是否存在
    if not os.path.isfile(file_name):
        print(f"{file_name} 不存在，正在创建...")
        # 创建一个示例 DataFrame
        my_map_read = {}
        write_tou_tiao_hot(my_map_read)
        print(f"{file_name} 已创建并写入数据。")
        return my_map_read
    else:
        print(f"{file_name} 已存在。")
        # 从 JSON 文件读取数据
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 打印恢复后的数据
        print("从 'data2.json' 读取的数据:")
        print(data)
        # 如果需要解析 JSON 字符串为列表
        # data['2024-08-06'] = json.loads(data['2024-08-06'])
        # print("解析后的数据:")
        # print(data)
        return data


def write_tou_tiao_hot(my_map):
    # 保存字典到 JSON 文件
    with open('../data.json', 'w', encoding='utf-8') as f:
        json.dump(my_map, f, ensure_ascii=False, indent=4)
    print("字典已保存到 'data.json'")


# 设置上传文件的保存路径
UPLOAD_FOLDER = 'uploads'
# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 上传文件
class EmailUploadHandler(tornado.web.RequestHandler):
    # 处理 POST 请求
    def post(self):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        # 读取 JSON 数据
        try:
            if 'file' not in self.request.files or not self.request.files['file']:
                self.write({"code": 400, "message": "No file provided"})
                self.flush()
                return

            file = self.request.files['file'][0]  # 获取上传的文件

            if file.filename == '':
                self.write({"code": 400, "message": "No file selected"})
                self.flush()
                return

            if allowed_file(file.filename):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                with open(file_path, 'wb') as f:
                    f.write(file.body)
                self.write({"code": 200, "message": "File uploaded successfully"})
            else:
                self.write({"code": 400, "message": "File type not allowed"})
            self.flush()

        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    # 处理 OPTIONS 请求（CORS 预检请求）
    def options(self):
        # 设置 CORS 头
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        # 返回状态码 204 表示成功但无内容
        self.set_status(204)
        self.finish()


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'txt', 'sql', 'md', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


# 上传文件
class MinioUploadHandler(tornado.web.RequestHandler):
    # 处理 POST 请求
    def post(self):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        # 读取 JSON 数据
        try:
            if 'file' not in self.request.files or not self.request.files['file']:
                self.write({"code": 400, "message": "No file provided"})
                self.flush()
                return

            file = self.request.files['file'][0]  # 获取上传的文件

            if file.filename == '':
                self.write({"code": 400, "message": "No file selected"})
                self.flush()
                return

            if allowed_file(file.filename):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                with open(file_path, 'wb') as f:
                    f.write(file.body)

                endpoint = Config.get('minio')['url']
                access_key = Config.get('minio')['userName']
                secret_key = Config.get('minio')['password']
                storage = MinioStorage(endpoint, access_key, secret_key)

                # 创建存储桶
                storage.create_bucket('my-bucket-picture')
                # 上传文件并获取可访问 URL
                url = storage.upload_file('my-bucket-picture', file_path, file.filename)
                if url:
                    print(f"可访问的 URL: {url}")
                self.write({"errno": 0, "message": "File uploaded successfully", "data": {"url": url}})
            else:
                self.write({"code": 400, "message": "File type not allowed"})
            self.flush()

        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    # 处理 OPTIONS 请求（CORS 预检请求）
    def options(self):
        # 设置 CORS 头
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        # 返回状态码 204 表示成功但无内容
        self.set_status(204)
        self.finish()
