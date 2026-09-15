---
title: Time_wait状态端口重利用
date: '2020-08-24 16:44:00'
permalink: 2020/08/24/csdn/Time_wait状态端口重利用/
categories:
- 计算机网络
tags:
- socket
---

##### 连接断开的过程:

主机A发起请求断开连接,主机B回应ACK,FIN包,当主机A收到FIN包时,TIME\_WAIT定时器开始启动,然后A向B发送ACK包,**因为B没有收到ACK包,所以B不知道自己的FIN包是否发送成功**

1. B成功收到ACK包,连接断开
2. B没有收到ACK包,**认为自己发送的FIN包出现问题,则重新发送FIN包**,

##### 为什么有Time\_wait状态?

1. 如果没有Time\_wait状态,A向B发送完ACK包后套接字完全终止,但是ACK包中途丢失,则B认为发送给A的FIN包丢失了,继续重传,**但主机A已经处于完全终止状态**,永远收不到来自A的消息,
2. 如果TIME\_WAIT状态存在,那么A**可以再次重传ACK消息**连接可以正常终止.

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200824164351605.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

---

服务器程序如果Ctrl+c杀掉后,立马重启,因为端口位于Time\_wait状态下的套接字,所以`bind() error`,

> 谁先发起断开连接请求TIME\_WAIT在这一端,一般不关注客户端的Time\_wait，客户端的端口都是随机动态分配

---

#### 地址再分配(端口重用):

Time\_wait状态下的套接字端口号可以重新分配给新的套接字.**在使用前**修改SOL\_SOCKET中的SO\_REUSEADDR状态(=1可重用).

```c
#include <me.h>

#define TRUE  1
#define FALSE 0

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  char message[30];
  int option,str_len;
  socklen_t optlen,clnt_adr_sz;
  struct sockaddr_in serv_adr,clnt_adr;
  if (argc != 2)
  {
    printf("Usage : %s <port>\n",argv[0]);
    exit(1);
  }
  
  serv_sock = socket(PF_INET,SOCK_STREAM,0); //创建TCP套接字
  if (serv_sock == -1)
    error_handle("socket() error");
   
  optlen = sizeof(option);
  option = TRUE;
  setsockopt(serv_sock,SOL_SOCKET,SO_REUSEADDR,(void*)&option,optlen);
  
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family       = AF_INET;
  serv_adr.sin_addr.s_addr  = htonl(INADDR_ANY);//服务器端监听所有网卡 
  serv_adr.sin_port         = htons(atoi(argv[1]));

  if (bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)))
    error_handle("bind() error");
  if (listen(serv_sock,5) == -1)
    error_handle("listen() error");

  //接收客户端请求
  clnt_adr_sz = sizeof(clnt_adr);
  clnt_sock   = accept(serv_sock,(struct sockaddr*)&clnt_adr,&clnt_adr_sz);
  while((str_len = read(clnt_sock,message,sizeof(message))) != 0)
  {
    write(clnt_sock,message,str_len);
    write(1,message,str_len);//标准输出
  }
  close(clnt_sock);
  close(serv_sock);

  return 0;
}
```

---

```c
//后面用到
#ifndef _ME_H_
#define _ME_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>

#define error_handle(message) \
  {fputs(message,stderr);\
  fputc('\n',stderr);\
  exit(1);}

#endif
```
> 来自<<TCP/IP 网络编程 尹圣雨>>
