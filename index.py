# -*- coding: utf8 -*-
from auto_sign import main
def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    main()
    return("签到成功")
