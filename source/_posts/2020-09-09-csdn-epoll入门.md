---
title: epoll入门
date: '2020-09-09 20:14:00'
permalink: 2020/09/09/csdn/epoll入门/
categories:
- Linux学习
---

#### epoll

> 对比select不需要 自己向OS传递监视对象信息,epoll由OS负责保存 监视对象文件fd,通过`epoll_create()`向OS申请资源

`int epoll_create(int size);`

#### 在epoll实例中注册对象文件描述符

`int epoll_ctl(int epfd,int op,int fd,struct epoll_event *event);`

第二个参数option:

> 1. EPOLL\_CTL\_ADD:向epoll实例中添加事件
> 2. EPOLL\_CTL\_DEL:向epoll实例中删除事件,不需要传入event了
> 3. EPOLL\_CTL\_MOD:修改事件发生情况

---

#### event

```c
struct epoll_event
{
	__uint32_t events;
	epoll_data_t data;
};
typedef union epoll_data 
{
	void *ptr;
	int fd;
	__uint32_t u32;
	__uint64_t u64;
} epoll_data_t;
```

events表示注册事件类型

> 目前例子用到:
>
> EPOLLIN: 需要读取数据
>
> EPOLLET:改为边缘触发方式
>
> EPOLLOUT:可以写数据
>
> EPOLLERR:发生错误情况

data是事件类型的具体数据(union)

> 用于保存和注册发生变化的事件

---

#### epoll\_wait

`int epoll_wait(int epfd,struct epoll_event* events,int maxevents,int timeout);`

> events:**保存发生事件的集合的结构体地址,需要申请内存**
>
> maxevents:可以保存的最大事件数量
>
> timeout:和select类似,时间单位是**毫秒**,-1将一直 阻塞等待事件发生

#### 条件触发echo服务器

```c
#include <me.h>
#define BUF_SIZE 4
#define EPOLL_SIZE 50 

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  struct sockaddr_in serv_adr,clnt_adr;
  socklen_t adr_sz;
  int str_len,i;
  char buf[BUF_SIZE];
  
  struct epoll_event *ep_events;
  struct epoll_event event;
  int epfd,event_cnt;

  if (argc != 2)
  {
    printf("Usage : %s <port>\n",argv[0]);
    exit(1);
  }

  serv_sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_adr.sin_port = htons(atoi(argv[1]));

  if (bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)) == -1)
    error_handle("bind() error")

  if (listen(serv_sock,5) == -1)
    error_handle("listen() error")

  epfd = epoll_create(EPOLL_SIZE);
  ep_events = malloc(sizeof(struct epoll_event) * EPOLL_SIZE);
  
  event.events = EPOLLIN;
  event.data.fd = serv_sock;
  epoll_ctl(epfd,EPOLL_CTL_ADD,serv_sock,&event);

  while(1)
  {
    event_cnt = epoll_wait(epfd,ep_events,EPOLL_SIZE,-1);
    if (event_cnt == -1)
    {
      puts("epoll_wait() error");
      break;
    }

    puts("return epoll_wait");
    for (i=0; i<event_cnt; i++)
    {
      if (ep_events[i].data.fd == serv_sock)
      {
        adr_sz = sizeof(clnt_adr);
        clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&adr_sz);
        event.events = EPOLLIN;
        event.data.fd = clnt_sock;
        epoll_ctl(epfd,EPOLL_CTL_ADD,clnt_sock,&event);
        printf("connected client: %d \n",clnt_sock);
      }
      else
      {
        str_len = read(ep_events[i].data.fd,buf,BUF_SIZE);
        if (str_len == 0)
        {
          epoll_ctl(epfd,EPOLL_CTL_DEL,ep_events[i].data.fd,NULL);
          close(ep_events[i].data.fd);
          printf("closed client: %d \n",ep_events[i].data.fd);
        }
        else
        {
          write(ep_events[i].data.fd,buf,str_len);
        }
      }
    }
  }
  close(epfd);
  close(serv_sock);
  return 0;
}
```
> 条件触发:只要输入缓冲中有数据就会一直通知发生该事件
>
> 边缘触发:输入缓冲接收到数据后只注册1次事件,**因为只注册1次事件,那么需要读取缓冲区中全部数据,就需要验证缓冲区是否为空?**
>
> read/write以阻塞方式工作,在注册1次事件后调用它可能长时间阻塞,如何避免长时间阻塞和检测缓冲区大小??**设置read/write以非阻塞方式工作,并且通过errno检测缓冲区是否被读取完**

#### 边缘触发echo服务器

```c
#include <me.h>

#define BUF_SIZE 4
#define EPOLL_SIZE 50

void setnonblockingmode(int );

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  struct sockaddr_in serv_adr,clnt_adr;
  socklen_t adr_sz;
  int str_len,i;
  char buf[BUF_SIZE];

  struct epoll_event *ep_events,event;
  int epfd,event_cnt;
  if (argc != 2)
  {
    printf("Usage : %s <port>\n",argv[0]);
    exit(1);
  }

  serv_sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_adr.sin_port = htons(atoi(argv[1]));
  if (bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)))
    error_handle("bind() error")

  if (listen(serv_sock,5) == -1)
    error_handle("listen() error")

  epfd = epoll_create(EPOLL_SIZE);//申请epoll资源 
  ep_events = malloc(EPOLL_SIZE * sizeof(struct epoll_event));

  setnonblockingmode(serv_sock);
  event.events = EPOLLIN | EPOLLET;//默认是条件触发,修改为socket nonblocking + 边沿触发 
  event.data.fd = serv_sock;
  epoll_ctl(epfd,EPOLL_CTL_ADD,serv_sock,&event);

  while(1)
  {
    event_cnt = epoll_wait(epfd,ep_events,EPOLL_SIZE,-1);
    if (event_cnt == -1)
    {
      puts("epoll_wait() error");
      break;
    }

    puts("return epoll_wait");
    for (i=0; i<event_cnt; i++)
    {
      if (serv_sock == ep_events[i].data.fd) 
      {
        adr_sz = sizeof(clnt_adr);
        clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&adr_sz);//因为是nonblock,accept接收不到要检查errno错误 
        //设置连接的socket nonblock 
        setnonblockingmode(clnt_sock);
        event.events = EPOLLIN | EPOLLET;//设置事件是边沿触发 
        event.data.fd = clnt_sock;
        epoll_ctl(epfd,EPOLL_CTL_ADD,clnt_sock,&event);
        printf("connected client: %d \n",clnt_sock);
      }
      else
      {
        //因为是边沿触发,时间只注册1次,那么要一直读(nonblocking socket)然后根据errno错误来停止读下去 
        while(1)
        {
          str_len = read(ep_events[i].data.fd,buf,BUF_SIZE);
          if (str_len == 0)
          {
            epoll_ctl(epfd,EPOLL_CTL_DEL,ep_events[i].data.fd,NULL);
            close(ep_events[i].data.fd);
            printf("closed client: %d \n",ep_events[i].data.fd);
            break;
          }
          else if (str_len < 0) //nonblock 说明暂时无数据可读 
          {
            if (errno == EAGAIN)
              break;
          }
          else 
          {
            write(ep_events[i].data.fd,buf,str_len);
          }
        }
      }
    }
  }
  close(epfd);
  close(serv_sock);
  return 0;
}

void setnonblockingmode(int fd)
{
  int flags = fcntl(fd,F_GETFL,0);
  fcntl(fd,F_SETFL,flags | O_NONBLOCK);//设置socket为非阻塞 
}
```
> 其他的struct epoll\_event.events选项暂时没用到,

目前的`me.h`文件

```c
#ifndef _ME_H_
#define _ME_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/tcp.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/uio.h>
#include <sys/epoll.h>
#include <errno.h>

#define error_handle(message) \
  {fputs(message,stderr);\
  fputc('\n',stderr);\
  exit(1);}

#endif
```

---

> 来自<<TCP/IP 网络编程 尹圣雨>>
