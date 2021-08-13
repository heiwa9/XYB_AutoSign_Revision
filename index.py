# -*- coding: utf-8 -*-
import requests
import sys
import json
from datetime import datetime, timedelta, timezone
import time
import hashlib

urls = {
    # 'login': 'https://xcx.xybsyw.com/login/login!wx.action',
    'login': 'https://xcx.xybsyw.com/login/login.action',
    'loadAccount': 'https://xcx.xybsyw.com/account/LoadAccountInfo.action',
    'ip': 'https://xcx.xybsyw.com/behavior/Duration!getIp.action',
    'trainId': 'https://xcx.xybsyw.com/student/clock/GetPlan!getDefault.action',
    # 'position':'https://xcx.xybsyw.com/student/clock/GetPlan!detail.action',
    'sign': 'https://app.xybsyw.com/behavior/Duration.action',
    'autoSign': 'https://xcx.xybsyw.com/student/clock/Post!autoClock.action',
    'newSign': 'https://xcx.xybsyw.com/student/clock/PostNew!updateClock.action',
    'status': 'https://xcx.xybsyw.com/student/clock/GetPlan!detail.action'
}


host1 = 'xcx.xybsyw.com'
host2 = 'app.xybsyw.com'


def getTimeStr():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")


def str2md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()


def log(content):
    print(getTimeStr() + ' ' + str(content))
    sys.stdout.flush()


# 获取Header
def getHeader(host):
    userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'
    contentType = 'application/x-www-form-urlencoded'
    headers = {
        'user-agent': userAgent,
        'content-type': contentType,
        'host': host,
        'Connection': 'keep-alive'
    }
    return headers


# 获取账号和密码
def getuser(userInfo):
    data = {
        'username': userInfo['token']['username'],
        'password': str2md5(userInfo['token']['password'])
    }
    return data


# 登录获取sessionId和loginerId
def login(userInfo):
    data = getuser(userInfo)
    headers = getHeader(host1)
    url = urls['login']
    resp = requests.post(url=url, headers=headers, data=data).json()
    if('成功' in resp['msg']):
        ret = {
            'sessionId': resp['data']['sessionId'],
            'loginerId': resp['data']['loginerId']
        }
        log(f"sessionId:{resp['data']['sessionId']}")
        log(f"loginerId:{resp['data']['loginerId']}")
        return ret
    else:
        log(resp['msg'])
        exit(-1)


# 获取姓名
def getUsername(sessionId):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['loadAccount']
    resp = requests.post(url=url, headers=headers).json()
    if('成功' in resp['msg']):
        ret = resp['data']['loginer']
        log(f"姓名:{ret}")
        return ret
    else:
        log('获取姓名失败')
        exit(-1)


# 获取ip
def getIP(sessionId):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['ip']
    resp = requests.post(url=url, headers=headers).json()
    if('success' in resp['msg']):
        ret = resp['data']['ip']
        log(f'ip:{ret}')
        return ret
    else:
        log('ip获取失败')
        exit(-1)


# 获取trainID
def getTrainID(sessionId):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['trainId']
    resp = requests.post(url=url, headers=headers).json()
    if('成功' in resp['msg']):
        ret = resp['data']['clockVo']['traineeId']
        log(f'traineeId:{ret}')
        return ret
    else:
        log('trainid获取失败')
        exit(-1)


# 获取经纬度\签到地址
def getPosition(sessionId, trainId):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['status']
    data = {
        'traineeId': trainId
    }
    resp = requests.post(url=url, headers=headers, data=data).json()
    if('成功' in resp['msg']):
        address = resp['data']['postInfo']['address']
        lat = resp['data']['postInfo']['lat']
        lng = resp['data']['postInfo']['lng']
        ret = {
            'lat': lat,
            'lng': lng
        }
        log(f'经度:{lng}|纬度:{lat}')
        log(f'签到地址:{address}')
        return ret
    else:
        log('经纬度获取失败')
        exit(-1)


def getSignForm(data, user):
    timeStamp = int(time.time())
    form = {
        'login': '1',
        'appVersion': '1.5.75',
        'operatingSystemVersion': '10',
        'deviceModel': 'microsoft',
        'operatingSystem': 'android',
        'screenWidth': '415',
        'screenHeight': '692',
        'reportSrc': '2',
        'eventTime': timeStamp,
        'eventType': 'click',
        'eventName': 'clickSignEvent',
        'clientIP': data['ip'],
        'pageId': data['pageId'],  # 30
        'itemID': 'none',
        'itemType': '其他',
        'stayTime': 'none',
        'deviceToken': '',
        'netType': 'WIFI',
        'app': 'wx_student',
        'preferName': '成长',
        'pageName': '成长-签到',
        'userName': data['userName'],
        'userId': data['loginerId'],
        'province': user['location']['province'],
        'country': user['location']['country'],
        'city': user['location']['city'],
    }
    return form


# 签到请求
def signReq(sessionId, data):
    headers = getHeader(host2)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['sign']
    resp = requests.post(url=url, headers=headers, data=data).json()
    if ('success' in resp['msg']):
        log(f'签到请求执行成功')
    else:
        log('签到请求执行失败')
        exit(-1)


# 执行签到
def autoSign(sessionId, data):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['autoSign']
    resp = requests.post(url=url, headers=headers, data=data).json()
    log(resp['msg'])
    return resp['msg']


# 重新签到
def newSign(sessionId, data):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['newSign']
    resp = requests.post(url=url, headers=headers, data=data).json()
    log(resp['msg'])
    return resp['msg']


# 获取签到状态
def getSignStatus(sessionId, trainId):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['status']
    data = {
        'traineeId': trainId
    }
    resp = requests.post(url=url, headers=headers, data=data).json()
    # if(resp['data']['clockInfo']['status'] == 0):
    if(len(resp['data']['clockInfo']['inTime']) > 0):
        return True
    else:
        return False


# Qmsg酱通知
def sendQmsgChan(msg):
    time.sleep(1.5)
    log('正在发送Qmsg酱……')
    config = readJsonInfo()
    if config['qmsg_key'] =="":
        log('不发送通知……')
        return
    res = requests.post(url='https://qmsg.zendee.cn:443/group/{0}'.format(config['qmsg_key']),
                            data={'msg': '校友邦签到通知\n时间：' + getTimeStr() + "\n消息：" + str(msg),'qq':'879618038'})
    code = res.json()['success']
    if code:
        log('发送Qmsg酱通知成功……')
    else:
        log('发送Qmsg酱通知失败……')
        log('Qmsg酱返回结果'+str(code))


def signHandler(userInfo):
    sessions = login(userInfo)
    sessionId = sessions['sessionId']
    loginerId = sessions['loginerId']
    trainId = getTrainID(sessionId)
    userName = getUsername(sessionId)
    ip = getIP(sessionId)
    position = getPosition(sessionId, trainId)
    lng = position['lng']
    lat = position['lat']
    data = {
        'pageId': '30',
        'userName': userName,
        'loginerId': loginerId,
        'ip': ip
    }
    formData = getSignForm(data, userInfo)
    signReq(sessionId, formData)
    signFormData = {
        'traineeId': trainId,
        'adcode': userInfo['location']['adcode'],
        'lat': lat,
        'lng': lng,
        'address': userInfo['location']['address'],
        'deviceName': 'microsoft',
        'punchInStatus': '1',
        'clockStatus': '2',
        'imgUrl': '',
        'reason': userInfo['reason']
    }
    if(getSignStatus(sessionId, trainId)):
        log('已签到,执行重新签到')
        newSign(sessionId, signFormData)
    else:
        autoSign(sessionId, signFormData)
    if (getSignStatus(sessionId, trainId)):
        sendQmsgChan(userName+'签到成功')
        log('校友邦实习任务签到成功\n\n')
    else:
        sendQmsgChan(userName+'签到失败')
        log('校友邦实习任务签到失败!')


# 读取user.json
def readJsonInfo():
    with open('user.json', 'r', encoding='utf8') as fp:
        users = json.load(fp)
    fp.close()
    return users


# 腾讯云函数使用
def main_handler(event, context):
    users = readJsonInfo()
    for user in users['user']:
        signHandler(user)
        time.sleep(1.5)


if __name__ == '__main__':
    users = readJsonInfo()
    for user in users['user']:
        signHandler(user)
        time.sleep(1.5)
