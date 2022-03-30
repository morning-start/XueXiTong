import requests
import json
import urllib.parse
import datetime
import os
session = requests.session()
requests.packages.urllib3.disable_warnings()

# 用户配置！必须写！
setting = {
    "account": os.getenv("ACCOUNT"),  # 账号（手机号 ）「必填」
    "password": so.getenv("PASSWORD"),  # 密码 「必填」
    "sign": {
        "long": '1',  # 定位签到经纬度 「可空」
        "lat": '1',  # 定位签到经纬度 「可空」
        "address": os.getenv('ADDRESS'),  # 定位签到显示的地址 「必填」
        "name": os.getenv('NAME'),  # 签到姓名 「必填」
        # 图片自定义之后再写，这里可以自己填入objectId列表就可以了，默认上传的图片是「图片加载失败」用来迷惑老师
        "img": os.getenv("IMG"),
        "sign_common": True,  # 是否开启普通签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_pic": True,  # 是否开启照片签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_hand": True,  # 是否开启手势签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_local": True,  # 是否开启定位签到 「True 开启 False 关闭」 默认开启，无需修改
    },
    "other": {
        "count": 5,  # 每门课程只检测前N个活动 避免因课程活动太多而卡住
    }
}

# 乱七八糟的变量 不要动我
mycookie = ""
myuid = ""
courselist = []


def login(uname, code):
    """ 登录 """
    global mycookie, myuid
    url = "https://passport2-api.chaoxing.com/v11/loginregister?code="+code + \
        "&cx_xxt_passport=json&uname="+uname+"&loginType=1&roleSelect=true"
    res = session.get(url)
    data = requests.utils.dict_from_cookiejar(session.cookies)
    mycookie = ""
    for key in data:
        mycookie += key+"="+data[key]+";"
    d = json.loads(res.text)
    if(d['mes'] == "验证通过"):
        print(uname+"登录成功")
        url = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
        res = session.get(url)
        a = json.loads(res.text)
        if(a['result'] == 1):
            myuid = str(a['msg']['puid'])
            save_cookies(myuid, 2)
            return 1
        else:
            print("获取uid失败")
    return 0


def getheaders():
    """ 获取同意请求头 包含Cookie """
    headers = {"Accept-Encoding": "gzip",
               "Accept-Language": "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
               "Cookie": mycookie,
               "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 com.ssreader.ChaoXingStudy/ChaoXingStudy_3_4.8_ios_phone_202012052220_56 (@Kalimdor)_12787186548451577248", }
    return headers


def getcourse():
    """ 获取课程列表 """
    global courselist
    url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
    headers = getheaders()
    if(headers == 0):
        return 0
    res = requests.get(url, headers=headers)
    if('请重新登录' in res.text):
        print("Cookie已过期")
    else:
        d = json.loads(res.text)
        courselist = d['channelList']
        print("课程列表加载完成")


def sign1(aid, uid, name):
    """ 普通签到 """
    t = get_time()
    print(t+" 发现普通签到")
    name = urllib.parse.quote(name)
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+aid + \
        "&uid="+uid+"&clientip=&latitude=-1&longitude=-1&appType=15&fid=0&name="+name
    headers = getheaders()
    if(headers == 0):
        return 0
    res = requests.get(url, headers=headers)
    if(res.text == "success"):
        return 1
    else:
        return 0


def sign2(aid, uid, oid, name):
    """ 照片签到 """
    t = get_time()
    print(t+" 发现照片签到/手势签到")
    name = urllib.parse.quote(name)
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+aid+"&uid="+uid + \
        "&clientip=&useragent=&latitude=-1&longitude=-1&appType=15&fid=0&objectId="+oid+"&name="+name
    headers = getheaders()
    if(headers == 0):
        return 0
    res = requests.get(url, headers=headers)
    if(res.text == "success"):
        return 1
    else:
        return 0


def sign3(aid, uid, lat, long, name, address):
    """ 定位签到 """
    t = get_time()
    print(t+" 发现定位签到")
    name = urllib.parse.quote(name)
    address = urllib.parse.quote(address)
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?name="+name+"&address="+address + \
        "&activeId="+aid+"&uid="+uid+"&clientip=&latitude=" + \
        lat+"&longitude="+long+"&fid=0&appType=15&ifTiJiao=1"
    headers = getheaders()
    if(headers == 0):
        return 0
    res = requests.get(url, headers=headers)
    if(res.text == "success"):
        return 1
    else:
        return 0


def get_sign_type(aid):
    """ 获取签到类型 """
    url = "https://mobilelearn.chaoxing.com/newsign/signDetail?activePrimaryId="+aid+"&type=1&"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 (@Kalimdor)_11391565702936108810"
    }
    res = requests.get(url, verify=False)
    d = json.loads(res.text)
    if(d['otherId'] == 0):
        if(d['ifPhoto'] == 1):
            return 1
        else:
            return 2
    elif(d['otherId'] == 2):
        if(d['ifRefreshEwm'] == 1):
            return 3
        else:
            return 4
    elif(d['otherId'] == 3):
        return 6
    elif(d['otherId'] == 4):
        return 5
    else:
        return 0


def sign(aid, uid, name):
    """ 拍照签到 1 普通签到 2 定位签到 5 手势签到 6 """
    activeType = get_sign_type(aid)
    if(activeType == 1):
        images = setting['sign']['img']
        # 未配置图片
        if(len(images) == 0):
            signres = sign2(aid, uid, "", name)
        else:
            nowimg = init_img(images)
            signres = sign2(aid, uid, nowimg, name)
    elif(activeType == 2):
        signres = sign1(aid, uid, name)
    elif(activeType == 5):
        signres = sign3(aid, uid, setting['sign']['lat'],
                        setting['sign']['long'], name, setting['sign']['address'])
    elif(activeType == 6):
        signres = sign2(aid, uid, "", name)
    else:
        return -1
    print("签到结果"+str(signres))
    return signres


def gettask(courseId, classId, uid, cpi, name, sign_common, sign_pic, sign_hand, sign_local):
    """ 获取用户活动列表 """
    try:
        url = "https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId=" + \
            courseId+"&classId="+classId+"&uid="+uid+"&cpi="+cpi
        headers = getheaders()
        if(headers == 0):
            return 0
        res = requests.get(url, headers=headers)
        d = json.loads(res.text)
        if(d['result'] == 1):
            activeList = d['activeList']
            count = 0
            for active in activeList:
                status = active['status']
                activeType = active['activeType']
                aid = str(active['id'])
                if(status != 1):
                    return 0
                if(activeType == 1 and sign_pic == True):
                    sign(aid, uid, name)
                if(activeType == 2 and sign_common == True):
                    sign(aid, uid, name)
                if(activeType == 5 and sign_local == True):
                    sign(aid, uid, name)
                if(activeType == 6 and sign_hand == True):
                    sign(aid, uid, name)
                count += 1
                if(count >= setting['other']['count']):
                    break
    except Exception as e:
        print(e)


def get_time():
    """ 获取当前时间 """
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    second = today.second
    if(month < 10):
        month = "0"+str(month)
    if(day < 10):
        day = "0"+str(day)
    date = "["+str(year)+"."+str(month)+"."+str(day)+" " + \
        str(hour)+":"+str(minute)+":"+str(second)+"]"
    return date


def init_cookies():
    """ 初始化Cookies """
    try:
        with open('cookies.txt', 'r') as f:
            data = f.read()
            f.close()
            if(len(data) < 100):
                return 0
            return data
    except Exception as e:
        return 0


def init_uid():
    """ 获取uid """
    try:
        with open('uid.txt', 'r') as f:
            data = f.read()
            f.close()
            if(len(data) < 5):
                return 0
            return data
    except Exception as e:
        return 0


def download_img(url):
    response = requests.get(url)
    data = response.content
    with open('./img.jpg', 'wb') as f:
        f.write(data)

# 65bd1f7a9422da2fbf532610c528c5d6


def init_img(filename):
    """ 初始化图片 """
    if(filename.startswith('http')):
        download_img(filename)
        filename = './img.jpg'
    r_session = requests.session()
    url = 'https://pan-yz.chaoxing.com/upload?_token=5d2e8d0aaa92e3701398035f530c4155'
    mobile_header = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; MI 8 MIUI/20.2.27)'
                      ' com.chaoxing.mobile/ChaoXingStudy_3_4.3.6_android_phone_496_27 (@Kalimdor)'
                      '_994222229cb94d688c462b7257600006',
        'Host': 'pan-yz.chaoxing.com'
    }
    img = {}
    try:
        img = {"file": ("123.jpg", open(filename, "rb"))}
    except:
        print("找不到图片")
        return ""  # 空图片
    i_data = {'puid': "80421235"}
    response = r_session.post(
        url=url, headers=mobile_header, data=i_data, files=img)
    print("照片预览：http://pks3.ananas.chaoxing.com/star3/312_412c/" +
          response.json().get('objectId') + ".jpg")
    return response.json().get('objectId')


def save_cookies(data, type):
    """ 保存Cookies文件 """
    if(type == 1):
        with open('cookies.txt', 'w') as f:
            f.write(data)
            f.close()
    else:
        with open('uid.txt', 'w') as f:
            f.write(str(data))
            f.close()


def init():
    """ 初始化 """
    global mycookie, myuid
    if(setting['account'] == "" or setting['password'] == ""):
        print("未进行账号配置")
        return 0
    cookies = init_cookies()
    uid = init_uid()
    if(cookies == 0 or uid == 0):
        res = login(setting['account'], setting['password'])
        if(res == 0):
            print("登录失败，请检查账号密码")
        else:
            save_cookies(mycookie, 1)
            getcourse()
    else:
        mycookie = cookies
        myuid = uid
        getcourse()
    return 1


def check():
    """ 检测是否需要登录 """
    for course in courselist:
        if('roletype' in course['content']):
            roletype = course['content']['roletype']
        else:
            continue
        if(roletype != 3):
            continue
        classId = str(course['content']['id'])
        courseId = str(course['content']['course']['data'][0]['id'])
        cpi = str(course['content']['cpi'])
        gettask(courseId, classId, myuid, cpi, setting['sign']['name'], setting['sign']['sign_common'],
                setting['sign']['sign_pic'], setting['sign']['sign_hand'], setting['sign']['sign_local'])


if __name__ == "__main__":
    res = init()
    if(res == 1):
        print("初始化完成")
        check()
