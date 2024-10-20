#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import requests
import json
import uuid
import random

args = sys.argv
host = os.getenv('DATASTORE_HOST')
port = os.getenv('DATASTORE_PORT')
url = 'http://' + str(host) + ':' + str(port) + '/'
ids = []

#
# キャッシュへロード バッチ処理
#
if __name__ == '__main__':

    idx = 1000
    f = open(args[1], 'r')
    line = f.readline()
    while line:
        line = f.readline()
        line = line[:-1]
        payload = {'id': idx, 'val': line }
        json_str = requests.post(url, params=payload)
        json_dict = json.loads(json_str.text)
        print(idx,line)
        idx += 1
    f.close()

    
    






