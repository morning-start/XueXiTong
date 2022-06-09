from pyquery import PyQuery as pq
import requests
from conf import *

req = requests.Session()
content = ''


def login():
    req.headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 com.ssreader.ChaoXingStudy/ChaoXingStudy_3_4.8_ios_phone_202012052220_56 (@Kalimdor)_12787186548451577248"
    }
    url = f"https://passport2-api.chaoxing.com/v11/loginregister?code={setting['password']}&cx_xxt_passport=json&uname={setting['account']}&loginType=1&roleSelect=true"
    res = req.get(url)

    if res.json()['mes'] == "验证通过":
        # 获取Cookie
        cookie = requests.utils.dict_from_cookiejar(req.cookies)
        mycookie = ""
        for key, value in cookie.items():
            mycookie += f"{key}={value};"
        req.headers["Cookie"] = mycookie
        print("登录成功")


def home_notes():
    '''作业提醒'''
    homework = []
    res = req.get("http://mooc1-api.chaoxing.com/work/stu-work")
    doc = pq(res.text)
    for i in doc("ul.nav >li span[class=fr]").items():
        data = i.siblings().contents()
        if data[1] == "未提交":
            homework.append([data[0], data[2], i.text()])
    return homework


def exam_notes():
    '''考试提醒'''
    exam = []
    res2 = req.get("https://mooc1-api.chaoxing.com/exam/phone/examcode")
    doc2 = pq(res2.text)
    for i in doc2("li:has(dd)").items():
        data = i.text().split("\n")
        if data[2] == "未交":
            exam.append([data[0], data[1]])
    return exam


def write_content(header, context):
    '''写入文件'''
    global content
    content += f"{header}\n"
    for i in context:
        content += " ".join(i) + "\n"


def note():
    login()
    homework = home_notes()
    exam = exam_notes()
    write_content("作业提醒", homework)
    write_content("考试提醒", exam)
    return content


if __name__ == "__main__":
    print(note())
