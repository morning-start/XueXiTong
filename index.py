# -*- coding: utf8 -*-
from auto_sign import auto_sign
from send import send
import json


def main_handler(event, context):
    '''云函数的主函数'''
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    res = auto_sign()
    if res:
        send(res)
    return("签到成功")


def main():
    res_sign = auto_sign()
    if res_sign:
        send(res_sign)
    return("签到成功")


# main()
