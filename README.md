# XYB_AutoSign_Revision

校友邦_自动签到_修订版

项目来自[Python 项目](https://github.com/CncCbz/xybSign/)

# 修订内容

---

1.更改登录方式（账号密码登录）

2.多账号支持

3.支持自动签到，自动签退

***建议配合腾讯云函数使用。***

## 运行环境

**Python3.6**

## 运行方式

配置`user.json`内容，运行`index.py`

user.json

```json
{
  "server_send_key": "Server酱 不使用留空",
  "ding_talk_access_token": "钉钉机器人 不使用留空",
  "ding_talk_secret": "钉钉加签验证 不使用留空",
  "user": [
    {
      "token": {
        "username": "账号1",  //手机账号
        "password": "密码1"  //登录密码
      },
      "location": {
        "country": "中国",
        "province": "湖北省",
        "city": "武汉市",
        "adcode": "420111", //行政区代码
        "address": "位置1"  //签到地址
      },
      "reason": ""  //签到备注
    },
      {
      "token": {
        "username": "账号2",  //手机账号
        "password": "密码2"  //登录密码
      },
      "location": {
        "country": "中国",
        "province": "湖北省",
        "city": "武汉市",
        "adcode": "420111", //行政区代码
        "address": "位置2"  //签到地址
      },
      "reason": ""  //签到备注
    }
    ...多个用户...
  ]
}


```

## 腾讯云函数部署Python脚本

> 可以将脚本免费托管到腾讯云函数，实现全天自动运行。配合server酱或钉钉机器人实现打卡通知

前提：进入[腾讯云账号注册页面](https://cloud.tencent.com/register)注册账号，开通云函数服务

​	1.登录 [云函数控制台](https://cloud.tencent.com/login?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fscf)，点击左侧导航栏`函数服务`，在函数服务页面上方选择地域，单击`新建`，如下图所示：

![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/QQ截图20220310112728.jpg)

​	2.选择`从头开始`，运行环境选择`Python3.6`，如下图：

![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/QQ截图20220310114000.jpg)

​	3.在`函数代码`处选择在线编辑，新建`user.json`文件，

​	根据[user.json](https://github.com/heiwa9/XYB_AutoSign_Revision/blob/main/user.json)文件进行内容填写，并将[index.py](https://github.com/heiwa9/XYB_AutoSign_Revision/blob/main/index.py)中的所有代码复制到云函数`index.py`中，如下图

> **修改完成后，记得`CTRL+S`保存修改。**

![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/QQ截图20220310114324.jpg)

![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/QQ截图20220310114425.jpg)

4. 配置`触发器`，选择自定义创建，配置`corn`,corn表达式自行搜索格式规范

   ![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/202203101209590.jpg)

   > 如果需要配置自动签退，则必须配置两个触发器，签到的`附加信息`改成`signin`，签退的`附加信息`改成`signout`

​	5.多用户签到，函数会超时，所以还需要配置一下函数超时时间。

![](https://cdn.jsdelivr.net/gh/1134451886/blog/img/202203101212756.jpg)

---

   - Readme Author :  @Dimension
   - Update Time :  2022/3/10
