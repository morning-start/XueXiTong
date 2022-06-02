# -*- coding: utf8 -*-
from auto_sign import sign
from auto_note import note
from auto_send import send
import json


def handler(event, context):
    '''云函数的主函数'''
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    auto_sign()


def auto_sign():
    res = sign()
    if res:
        send(res)
        return 'sign success'
    else:
        return 'sign error'


def auto_note():
    res = note()
    if res:
        send(res)
        return 'search success'
    else:
        return 'search error'
