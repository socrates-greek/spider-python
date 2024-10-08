import base64
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.application import MIMEApplication
from email.header import Header
import os

from Configs import Config

def send_email(requestData):
    sender_email = Config.get('simba')['username']
    attachFile = requestData.get("attachFile")  # 获取 "sender" 字段
    bodyImage = requestData.get("bodyImage")  # 获取 "sender" 字段
    body = requestData.get("body")  # 获取 "sender" 字段
    subject = requestData.get("subject")  # 获取 "sender" 字段
    tableContent = requestData.get("workList")
    receiver = requestData.get("to")  # 获取 "sender" 字段
    receiver_emails = receiver.split(",")
    # 创建 MIMEMultipart 邮件对象
    message = MIMEMultipart()
    message['From'] = Header(sender_email, 'utf-8')  # 发件人
    print(receiver)
    message['To'] = Header(receiver, 'utf-8')  # 将多个收件人拼接为字符串
    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
    # 添加邮件正文
    image_html = ""
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
    if len(tableContent) > 0:
        html_string = "<br>".join(tableContent)
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
        <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                table {{
                    border-collapse: collapse; 
                    margin: 20px auto; 
                    width: 600px; /* 让表格宽度自动调整 */
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 5px;
                    text-align: left; 
                    width: 600px;
                }}
                th {{
                    background-color: #CBDFA9;
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

    # print(html_content)

    # 将 HTML 内容添加到邮件中
    part = MIMEText(html_content, "html")
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
        encoded_filename = Header(attachFile, 'utf-8').encode()
        attachment.add_header('Content-Disposition', f'attachment; filename="{encoded_filename}"')
        message.attach(attachment)
        print(f"Attachment {attachFile} added.")
    else:
        print("No attachment or file does not exist.")

    # 连接邮件服务器并发送邮件
    # 发送邮件
    try:
        # 邮件发送配置
        smtp_server = Config.get('simba')['smtp_server']
        port = 465  # 使用 TLS 的端口
        sender_email = Config.get('simba')['username']
        password = Config.get('simba')['password']
        with smtplib.SMTP_SSL(smtp_server, port) as server:  # 替换为你的 SMTP 服务器地址和端口
            server.login(sender_email, password)  # 登录你的 SMTP 服务器
            server.sendmail(sender_email, receiver_emails, message.as_string())  # 发送邮件
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_week_range():
    # 获取当前时间
    today = datetime.today()
    # 计算当前周的周一（开始时间）
    start_of_week = today - timedelta(days=today.weekday())
    # 计算当前周的周日（结束时间）
    end_of_week = start_of_week + timedelta(days=6)

    # 返回开始和结束时间
    return start_of_week, end_of_week


