import os
setting = {
    "account": os.getenv("ACCOUNT"),  # 账号（手机号 ）「必填」
    "password": os.getenv("PASSWORD"),  # 密码 「必填」
    "email": os.getenv("EMAIL"),  # 邮箱「必填」
    "sign": {
        "long": os.getenv("LONGITUDE"),  # 定位签到经度 「可空」
        "lat": os.getenv("LATITUDE"),  # 定位签到纬度 「可空」
        "address": os.getenv('ADDRESS'),  # 定位签到显示的地址 「必填」
        "name": os.getenv('NAME'),  # 签到姓名 「必填」
        # 图片自定义之后再写，这里可以自己填入objectId列表就可以了，默认上传的图片是「图片加载失败」用来迷惑老师
        "img": os.getenv("IMG"),
        "sign_common": 1,  # 是否开启普通签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_pic": 1,  # 是否开启照片签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_hand": 1,  # 是否开启手势签到 「True 开启 False 关闭」 默认开启，无需修改
        "sign_local": 1,  # 是否开启定位签到 「True 开启 False 关闭」 默认开启，无需修改
    },
    "other": {
        "count": 5,  # 每门课程只检测前N个活动 避免因课程活动太多而卡住
    }
}

conf = {"mail_host": os.getenv("MAIL_HOST"),
        "mail_user": os.getenv("MAIL_USER"),
        "mail_password": os.getenv("MAIL_PASSWORD"),
        }
