import base64
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.application import MIMEApplication
from email.header import Header
import tornado.web
import yaml
import os

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
# 邮件发送配置
smtp_server = config['simba']['smtp_server']
port = 465  # 使用 TLS 的端口
sender_email = config['simba']['username']
password = config['simba']['password']

# 设置上传文件的保存路径
UPLOAD_FOLDER = 'uploads'
# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def send_email(attachFile, bodyImage, body,tableContent, subject, receiver):
    receiver_emails = receiver.split(",")
    # 创建 MIMEMultipart 邮件对象
    message = MIMEMultipart()
    message['From'] = Header(sender_email, 'utf-8')  # 发件人
    print(receiver)
    message['To'] = Header(receiver, 'utf-8')  # 将多个收件人拼接为字符串
    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
    # 添加邮件正文
    image_html=""
    # 读取本地图片
    if bodyImage and os.path.exists(os.path.join(UPLOAD_FOLDER, bodyImage)):
        with open(os.path.join(UPLOAD_FOLDER, bodyImage), "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            # 生成HTML格式的图片
            image_html = f'<img src="data:image/png;base64,{img_data}" alt="Image" width="500" height="400" />'
    start, end = get_week_range()
    startDay = start.strftime("%Y/%m/%d")
    endDay = end.strftime("%Y/%m/%d")
    # 生成HTML内容
    # 修正后的 HTML 模板
    table = f"""
    """
    if tableContent.strip():
        html_string = tableContent.replace(",", "<br>")
        table = f"""
                <table>
                    <tr>
                        <th colspan="2">{startDay} ~ {endDay} 周报</th>
                    </tr>
                    <tr>
                        <td>{html_string}</td>
                    </tr>
                </table>
        """

    html_content = f"""
        <html>
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                table {{
                    border-collapse: collapse; 
                    margin: 20px auto; 
                    width: auto; /* 让表格宽度自动调整 */
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 5px;
                    text-align: left; 
                }}
                th {{
                    background-color: #d4edda;
                    font-size: 16px; 
                    font-weight: bold;
                }}
                td {{
                    font-size: 14px; 
                }}
            </style>
        </head>
        <body>
            {body}
            {table}
            <div>{image_html}</div>
        </body>
        </html>
        """
    # 将 HTML 内容添加到邮件中
    part = MIMEText(html_content, "html")
    print(part)
    message.attach(part)
    # 读取文件并添加到邮件中
    # 检查 attachFile 是否非空，且文件存在
    if attachFile and os.path.exists(os.path.join(UPLOAD_FOLDER, attachFile)):
        file_path = os.path.join(UPLOAD_FOLDER, attachFile)

        # 读取附件文件
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # 获取文件的 MIME 类型和子类型
        mime_type, encoding = mimetypes.guess_type(attachFile)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # 无法推断类型时，使用通用的二进制流类型
        maintype, subtype = mime_type.split('/', 1)

        # 创建 MIMEApplication 对象并附加到邮件中
        attachment = MIMEApplication(file_data, _subtype=subtype)
        attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        message.attach(attachment)
        print(f"Attachment {attachFile} added.")
    else:
        print("No attachment or file does not exist.")

    # 连接邮件服务器并发送邮件
    # 发送邮件
    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:  # 替换为你的 SMTP 服务器地址和端口
            server.login(sender_email, password)  # 登录你的 SMTP 服务器
            server.sendmail(sender_email, receiver_emails, message.as_string())  # 发送邮件
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


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


def get_week_range():
    # 获取当前时间
    today = datetime.today()
    # 计算当前周的周一（开始时间）
    start_of_week = today - timedelta(days=today.weekday())
    # 计算当前周的周日（结束时间）
    end_of_week = start_of_week + timedelta(days=6)

    # 返回开始和结束时间
    return start_of_week, end_of_week

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'xlsx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
