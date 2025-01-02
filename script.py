import time
import json
import hashlib
from js import tokens, ua  # 从JavaScript环境获取变量
from js import print as js_print
from pyodide.http import pyfetch
import asyncio

def print(text):
    js_print(str(text))

print("Python环境加载成功...")

async def make_request(url, method="GET", headers=None, data=None):
    try:
        print(f"发送请求到: {url}")
        response = await pyfetch(
            url,
            method=method,
            headers=headers,
            body=data if data else None,
        )
        print("请求成功，正在解析响应...")
        return await response.json()
    except Exception as e:
        print(f'网络请求出错：{str(e)}')
        return None

async def sha256_encrypt(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

async def signzfb(t, url, token):
    data = f'appSecret=Ew+ZSuppXZoA9YzBHgHmRvzt0Bw1CpwlQQtSl49QNhY=&channel=alipay&timestamp={t}&token={token}&version=1.59.3&{url[25:]}'
    return await sha256_encrypt(data)

async def sign(t, url, token):
    data = f'appSecret=nFU9pbG8YQoAe1kFh+E7eyrdlSLglwEJeA0wwHB1j5o=&channel=android_app&timestamp={t}&token={token}&version=1.59.3&{url[25:]}'
    return await sha256_encrypt(data)

async def qd(token):
    url = 'https://userapi.qiekj.com/signin/signInAcList'
    t = str(int(time.time() * 1000))
    signs = await sign(t, url, token)
    
    headers = {
        'Authorization': token,
        'Version': '1.59.3',
        'channel': 'android_app',
        'phoneBrand': 'Redmi',
        'timestamp': t,
        'sign': signs,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'userapi.qiekj.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': ua
    }
    data = {'token': token}
    
    res_json = await make_request(url=url, method='POST', headers=headers, data=data)
    
    if res_json and res_json.get("code") == 0:
        url = "https://userapi.qiekj.com/signin/doUserSignIn"
        t = str(int(time.time() * 1000))
        signs = await sign(t, url, token)
        
        headers['timestamp'] = t
        headers['sign'] = signs
        
        data = {'activityId': '600001', 'token': token}
        res_json = await make_request(url=url, method='POST', headers=headers, data=data)
        
        if res_json and "data" in res_json:
            print(f"签到成功，获得积分 {res_json['data']['totalIntegral']}")
        else:
            print("签到失败")
    else:
        print("获取签到列表失败")

async def taskrequests(ua, url, token, data):
    t = str(int(time.time() * 1000))
    signs = await sign(t, url, token)
    
    headers = {
        'Authorization': token,
        'Version': '1.59.3',
        'channel': 'android_app',
        'phoneBrand': 'Redmi',
        'timestamp': t,
        'sign': signs,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'userapi.qiekj.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': ua
    }
    
    return await make_request(url=url, method='POST', headers=headers, data=data)

async def tx(ua, token, tc):
    url = 'https://userapi.qiekj.com/task/completed'
    data = {'taskCode': tc, 'token': token}
    return await taskrequests(ua, url, token, data)

async def appvideo(ua, token, i):
    url = 'https://userapi.qiekj.com/task/completed'
    data = {'taskCode': 2, 'token': token}
    res_json = await taskrequests(ua, url, token, data)
    if res_json and res_json['code'] == 0:
        print(f'第{i}次APP视频任务完成')
    else:
        print('出错，跳过')
        if res_json:
            print(res_json)

async def chaAD(ua, token, i):
    url = 'https://userapi.qiekj.com/task/completed'
    data = {'taskCode': '18893134-715b-4307-af1c-b5737c70f58d', 'token': token}
    res_json = await taskrequests(ua, url, token, data)
    if res_json and res_json['code'] == 0:
        print(f'第{i}次APP视频任务完成')
    else:
        print('出错，跳过')
        if res_json:
            print(res_json)

async def sytask(ua, token):
    url = 'https://userapi.qiekj.com/task/completed'
    tasks = [
        {'taskCode': '8b475b42-df8b-4039-b4c1-f9a0174a611a', 'subtaskCode': '4a86e8b5-e46c-4dac-9e73-c6e3cf39c7d6'},
        {'taskCode': '8b475b42-df8b-4039-b4c1-f9a0174a611a', 'subtaskCode': '73310f73-b076-40d5-a53f-c79c48f14d64'},
        {'taskCode': '8b475b42-df8b-4039-b4c1-f9a0174a611a', 'subtaskCode': 'f3814d95-38f0-4778-8da3-6b8e3fc113d0'}
    ]
    
    for task in tasks:
        task['token'] = token
        res_json = await taskrequests(ua, url, token, task)
        try:
            if res_json and res_json['code'] == 0 and res_json['data'] == True:
                if task['subtaskCode'] == '4a86e8b5-e46c-4dac-9e73-c6e3cf39c7d6':
                    print("首页浏览5s成功，获得5积分")
                elif task['subtaskCode'] == '73310f73-b076-40d5-a53f-c79c48f14d64':
                    print("首页浏览10s成功，获得7积分")
                elif task['subtaskCode'] == 'f3814d95-38f0-4778-8da3-6b8e3fc113d0':
                    print("首页浏览30s成功，获得10积分")
        except:
            print("首页浏览出错❌")
        await asyncio.sleep(1)

async def ladderTask(ua, token):
    url = f'https://userapi.qiekj.com/ladderTask/ladderTaskForDay?token={token}'
    t = str(int(time.time() * 1000))
    signs = await sign(t, 'https://userapi.qiekj.com/ladderTask/ladderTaskForDay', token)
    
    headers = {
        'Authorization': token,
        'Version': '1.57.4',
        'channel': 'android_app',
        'phoneBrand': 'Redmi',
        'timestamp': t,
        'sign': signs,
        'Host': 'userapi.qiekj.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': ua
    }
    
    res_json = await make_request(url=url, method='GET', headers=headers)
    
    if res_json and res_json['code'] == 0:
        ladderRewardList = res_json['data']['ladderRewardList']
        for item in ladderRewardList:
            if item['isApplyReward'] == 1:
                data = {'rewardCode': item['rewardCode'], 'token': token}
                success = await taskrequests(ua, 'https://userapi.qiekj.com/ladderTask/applyLadderReward', token, data)
                print(success)
                await asyncio.sleep(2)
        print('阶梯任务领奖完成')
    else:
        print('阶梯任务领取失败')
        if res_json:
            print(res_json)

async def main():
    print('开始执行任务...')
    print(f'检测到 {len(tokens.split("&"))} 个账号')
    token_list = tokens.split("&")
    notfin = ["7328b1db-d001-4e6a-a9e6-6ae8d281ddbf", "e8f837b8-4317-4bf5-89ca-99f809bf9041",
              "65a4e35d-c8ae-4732-adb7-30f8788f2ea7", "73f9f146-4b9a-4d14-9d81-3a83f1204b74"]
    
    for tk in token_list:
        try:
            print(f"\n开始处理账号: {tk[:10]}...")
            
            # 执行首页浏览任务
            print("\n开始首页浏览任务")
            await sytask(ua, tk)
            await asyncio.sleep(2)
            
            # 执行签到
            print("开始签到任务")
            await qd(tk)
            await asyncio.sleep(3)
            
            # 获取任务列表
            url = 'https://userapi.qiekj.com/task/list'
            data = {'token': tk}
            res_json = await taskrequests(ua, url, tk, data)
            
            if res_json and res_json['code'] == 0:
                items = res_json['data']['items']
                for item in items:
                    if item['completedStatus'] == 0 and item["taskCode"] not in notfin:
                        print("\n------任务分割线-----\n")
                        print(f"开始执行任务  ——  {item['title']}")
                        for _ in range(item["dailyTaskLimit"]):
                            res = await tx(ua, tk, item["taskCode"])
                            if res and res["code"] == 0:
                                await asyncio.sleep(1)
                        print(f"{item['title']}  ——  任务完成")
                    await asyncio.sleep(3)
                
                # 执行视频任务
                print("\n开始执行视频任务")
                for i in range(5):
                    await appvideo(ua, tk, i + 1)
                    await asyncio.sleep(1)
                
                # 执行支付宝视频任务
                print("\n开始执行支付宝视频任务")
                for i in range(5):
                    res = await tx(ua, tk, '9')
                    if res and res["code"] == 0:
                        print(f"第{i + 1}次支付宝视频完成")
                    await asyncio.sleep(1)
                
                # 执行阶梯任务
                await ladderTask(ua, tk)
                
                # 获取余额
                url = 'https://userapi.qiekj.com/user/balance'
                data = {'token': tk}
                res_json = await taskrequests(ua, url, tk, data)
                if res_json:
                    print(f"总积分：{res_json['data']['integral']}")
                
            else:
                print("获取任务列表失败")
                
        except Exception as e:
            print(f"处理账号 {tk[:10]} 时出错: {str(e)}")
        finally:
            print("开始下一个账号\n\n")
            await asyncio.sleep(3)

# 启动主函数
asyncio.ensure_future(main())
