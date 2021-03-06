import smtplib
import json
import requests
from email.mime.text import MIMEText
from conf import *

mail_pre = mail["mail_host"] and mail["mail_password"] and mail["mail_user"] and mail['email']
server_pre = server["SCKEY"]
dingding_pre = dingding["dingding_hook"]


def send(content):
    if mail_pre:
        send_mail(content)
    else:
        print("No mailbox configured")
    if server_pre:
        send_server(content)
    else:
        print("No ServerChan configured")
    if dingding_pre:
        send_dingding(content)
    else:
        print("No dingding bot hook configured")


def send_mail(content):
    '''单用户邮件发送函数'''
    title = '超星自动签到系统'  # 邮件主题
    message = MIMEText(str(content), 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(mail["mail_user"])
    message['To'] = mail['email']
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(
            mail["mail_host"], 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail["mail_user"], mail["mail_password"])  # 登录验证
        smtpObj.sendmail(mail["mail_user"], mail['email'],
                         message.as_string())  # 发送
        print('================================')
        print('||                            ||')
        print("||       Have send mail       ||")
        print('||                            ||')
        print('================================')
    except smtplib.SMTPException as e:
        print(e, "邮件发送失败")
        pass


def send_server(content):
    '''server酱'''
    api = 'https://sc.ftqq.com/'
    data = {"text": content}
    url = api+server["SCKEY"]+'.send'
    res = requests.post(url=url, data=data)
    print(res.text)


def send_dingding(content):
    '''钉钉机器人推送'''
    key_word = "超星学习通签到"
    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    webhook = dingding["dingding_hook"]
    message_body = {
        "msgtype": "markdown",
        "markdown": {
            "title": key_word,
            "text": content
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    send_data = json.dumps(message_body)
    send_result = requests.post(url=webhook, data=send_data, headers=headers)
    if send_result.json()["errmsg"] == "ok":
        print("dingding send success")
    else:
        print("dingding send faild")
