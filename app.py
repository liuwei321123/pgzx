import time
import json
import hashlib
from js import tokens, ua  # 从JavaScript环境获取变量
from js import print as js_print

def print(text):
    js_print(str(text))

from pyodide.http import pyfetch

async def make_request(url, method="GET", headers=None, data=None):
    try:
        response = await pyfetch(
            url,
            method=method,
            headers=headers,
            data=data
        )
        return await response.string()
    except Exception as e:
        print(f'网络请求出错：{str(e)}')
        return None

print('环境初始化完成，开始执行任务...')
