# XYB_AutoSign_Revision
校友邦_自动签到_修订版

项目来自[Python 项目](https://github.com/CncCbz/xybSign/)  
# 修订内容
1.更改登录方式（账号密码登录）  
2.多账号支持

# 校友邦自动签到与签退

可以配合腾讯云函数使用，免去校友邦每日签到的麻烦

### 运行环境

python3

### 运行方式

配置`user.json`内容，运行`index.py`


user.json

```javascript
{
  "qmsg_key":"",//qmsg QQ消息推送
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

### 腾讯云函数部署python脚本

>腾讯云函数可以实现脚本自动运行，配合qmsg酱或server酱实现打卡通知

前提：进入[腾讯云账号注册页面](https://cloud.tencent.com/register)注册账号，开通云函数服务

1. 登录 [云函数控制台](https://cloud.tencent.com/login?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fscf)，点击左侧导航栏`函数服务`，在函数服务页面上方选择地域，单击`新建`，如下图所示：  
![1.jpg](https://ae01.alicdn.com/kf/U067134e2785948f5b05ccdb8bd582c16S.jpg)  
2. 选择`自定义创建`，运行环境选择`Python3.6`，修改函数名称，如下图：  
![2.jpg](https://ae01.alicdn.com/kf/U873a0be7a91442d5aff2948544605bfet.jpg)  
3. 在`函数代码`处选择在线编辑，新建`user.json`文件，根据[user.json](https://github.com/heiwa9/XYB_AutoSign_Revision/blob/main/user.json)文件进行内容填写，并将[index.py](https://github.com/heiwa9/XYB_AutoSign_Revision/blob/main/index.py)中的所有代码复制到云函数`index.py`中，如下图  
>记得`CTRL+S`保存函数  

![3.jpg](https://ae01.alicdn.com/kf/Uf8da1b423b004fb29a9de531ad0096a0M.jpg)  
![4.jpg](https://ae01.alicdn.com/kf/Ufd4ecc4576be4542814cbbd492a10796v.jpg)  
4. 配置`触发器`，选择自定义创建，配置`corn`  
> 图中表示每日9AM触发签到函数(`0 40 8 * * MON-SAT *`为周一到周六上午8：40)，详细配置策略请参考[corn相关文档](https://cloud.tencent.com/document/product/583/9708#cron-.E8.A1.A8.E8.BE.BE.E5.BC.8F)  

![5.jpg](https://ae01.alicdn.com/kf/U35a7a71247e04fdf8da58c794f854a40N.jpg)  
5. 点击完成，等待函数创建完成，选择刚刚创建的函数，点击测试，查看测试结果，若测试成功，则表示云函数部署完成  
![6.jpg](https://ae01.alicdn.com/kf/U5a8052c902dd4cc2b08b2b50d70270cfT.jpg)  
![7.jpg](https://ae01.alicdn.com/kf/Ubc0fd3f3036e430b9fe73f91e5df42a9S.jpg)  
6. 多用户签到，函数会超时，所以还需要配置一下函数超时时间。  
![8.jpg](https://user-images.githubusercontent.com/54386147/126591162-8677ecea-3a0e-4182-a60c-5d139325912c.png)  


