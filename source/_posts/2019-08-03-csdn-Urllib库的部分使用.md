---
title: Urllib库的部分使用
date: '2019-08-03 22:38:00'
permalink: 2019/08/03/csdn/Urllib库的部分使用/
---

### `Urllib`:`HTTP`请求库

4个模块

```css
urllib.request 请求
urllib.error 异常处理
urllib.parse url解析
urllib.robotparser rebot.txt解析
```

#### `urlopen()`

`urllib.request.urlopen(url,data=None,[timeout,]*,cafile=None,capath=None,cadefault=False,context=None)`

1. 将网页请求下来(`get请求,url里带参数`):
   ````qml
import urllib.request
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read().decode('utf-8'))
```  

2. 以`post`形式发送,`url`里不含参数,参数形成单独的字节发送
````
   import urllib.parse  
   import urllib.request  
   source = bytes(urllib.parse.urlencode({‘word’:’hello’},encoding=’utf-8’))  
   response = urllib.request.urlopen(‘<http://httpbin.org/post',source>)  
   print (response.read())
   ```autohotkey
3. 请求超时设置`timeout= `
```
   import urllib.requset  
   response = urllib.request.urlopen(‘<http://httpbin.org/get',timeout=1>)  
   print(response.read())
   ```autohotkey
4. 超时错误原因`socket.timeout`
```
   import socket  
   import urllib.request  
   import urllib.error  
   try:  
    response = urllib.request.urlopen(‘<http://httpbin.org/get',timeout=0.1>)  
   except urllib.error.URLError as e :  
   if isinstance(e.reason,socket.timeout):  
    print(“time out”)

```clean
#### `response` 响应
1. 响应类型
```

import urllib.request  
response = urllib.request.urlopen(‘[http://httpbin.org'](http://httpbin.org&/#39;))  
print(type(response))

```autohotkey
2. 状态码,响应头(`response headers`)
```

import urllib.request  
response = urllib.request.urlopen(‘[http://httpbin.org'](http://httpbin.org&/#39;))  
print (response.status)  
print (response.getheaders())  
print (response.getheader(‘Server’))

```plain
直接得到响应体内容,解码查看
```

import request  
response = urllib.request.urlopen(‘[http://httpbin.org'](http://httpbin.org&/#39;))  
print(response.read().decode(‘utf-8’)

```autohotkey
也可以先得到`Request`请求体.将`Request`通过`urlopen()`发送,得到响应体
```

import urllib.request  
request = urllib.request.Request(‘[http://python.org'](http://python.org&/#39;))  
response = urllib.request.urlopen(request)  
print(response.read().decode(‘utf-8’))

```autohotkey
#### `request`(请求)
通过`request`对象的传入参数来构造`get`/`post`类请求
```

from urllib import request,parse  
url = ‘<http://httpbin.org/post'>  
dict = {  
 ‘name’:’Germey’  
}  
data=bytes(parse.urlencode(dict),encoding=”utf8”)  
req=request.Request(url=url,data=data,method=’POST’)  
response=request.urlopen(req)  
print(response.read().encode(‘utf-8’))

````oxygene
```
from urllib import request,parse
url = 'http://httpbin.org/post'
dict = {
    'name':'Germey'
}
data=bytes(parse.urlencode(dict),encoding='utf8')
req=request.Request(url=url,data=data,method='POST')
req.add_header('User-Agent','Mozilla/4.0 (compatible;MSIE 5.5; Window NT)')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
````

#### `Handler`(代理,通过连接到代理服务器,用来隐藏自己的ip)

#### `cookie`:网站用来辨识用户身份存储在本地终端上的数据
