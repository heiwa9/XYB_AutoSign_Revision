# -*- coding: utf-8 -*-
import base64
import hmac
from urllib import parse
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
    if ('成功' in resp['msg']):
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
    if ('成功' in resp['msg']):
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
    if ('success' in resp['msg']):
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
    if ('成功' in resp['msg']):
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
    if ('成功' in resp['msg']):
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
def getSignStatus(sessionId, trainId, sence):
    headers = getHeader(host1)
    headers['cookie'] = f'JSESSIONID={sessionId}'
    url = urls['status']
    data = {'traineeId': trainId}

    resp = requests.post(url=url, headers=headers, data=data).json()
    if sence == '1':
        return True if len(resp['data']['clockInfo']['outTime']) > 0 else False
    else:
        return True if len(resp['data']['clockInfo']['inTime']) > 0 else False


# Server酱通知
def sendNoice(msg):
    log('正在发送通知')
    config = readJsonInfo()
    if config['server_send_key'] == "":
        log('不发送通知……')
        return
    resp = requests.post(url='https://sctapi.ftqq.com/{0}.send'.format(config['server_send_key']),
                         data={'title': '校友邦签到通知', 'desp': '时间：' + getTimeStr() + "\n消息：" + str(msg)})
    if resp.status_code == 200:
        log('推送成功')
    else:
        log('推送失败')


def dingTalkNoice(msg):
    log('正在发送通知')
    config = readJsonInfo()
    if config['ding_talk_secret'] == "":
        log('不发送通知……')
        return
    timestamp = str(round(time.time() * 1000))
    secret_enc = config['ding_talk_secret'].encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, config['ding_talk_secret'])
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    resp = requests.post(url='https://oapi.dingtalk.com/robot/send?access_token={0}&timestamp={1}&sign={2}'.
                         format(config["ding_talk_access_token"],
                                timestamp, sign,), headers={'content-type': 'application/json'}, data=json.dumps({
                                    "msgtype": "text",
                                    "text": {
                                        "content": '校友帮签到通知\n时间:' + getTimeStr() + '\n消息:' + str(msg),
                                    }
                                }))
    if resp.status_code == 200:
        log('推送成功')
    else:
        log('推送失败')


def signHandler(userInfo, sence):
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
        'clockStatus': sence,
        'imgUrl': '',
        'reason': userInfo['reason']
    }
    if sence == '1':
        autoSign(sessionId, signFormData)
        if getSignStatus(sessionId, trainId, sence):
            sendNoice(userName + '签退成功')
            dingTalkNoice(userName + '签退成功')
            log('校友邦实习任务签退成功\n\n')
        else:
            sendNoice(userName + '签退失败')
            dingTalkNoice(userName + '签退失败')
            log('校友邦实习任务签退失败!')
    else:
        if getSignStatus(sessionId, trainId, sence):
            log('已签到,执行重新签到')
            newSign(sessionId, signFormData)
        else:
            autoSign(sessionId, signFormData)
        if getSignStatus(sessionId, trainId, sence):
            sendNoice(userName + '签到成功')
            dingTalkNoice(userName + '签到成功')
            log('校友邦实习任务签到成功\n\n')
        else:
            sendNoice(userName + '签到失败')
            dingTalkNoice(userName + '签到失败')
            log('校友邦实习任务签到失败!')


# 读取user.json
def readJsonInfo():
    with open('user.json', 'r', encoding='utf8') as fp:
        users = json.load(fp)
    fp.close()
    return users


# 腾讯云函数使用
def main_handler(event, context):
    sence = 1 if event['Message'] == 'signout' else 0
    users = readJsonInfo()
    for user in users['user']:
        signHandler(user, sence)
        time.sleep(1.5)


if __name__ == '__main__':
    users = readJsonInfo()
    for user in users['user']:
        signHandler(user, sence=1)
        time.sleep(1.5)
