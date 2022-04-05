# -*- coding: utf8 -*-
from wsgiref import headers
import requests
import json


def run():
    payload = json.dumps({"ref": "main"})
    header = {"Authorization": "token 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",
              "Accept": "application/vnd.github.v3+json"}
    response_decoded_json = requests.post(
        f'https://api.github.com/repos/morning-start/auto_sign/actions/workflows/auto_sign/dispatches',
        data=payload, headers=header)
    return response_decoded_json.status_code

# 云函数入口


def main_handler(event, context):
    return run()


# if __name__ == '__main__':
#     print(run())
a = "23"
a += "2"
print(0 or 1)
