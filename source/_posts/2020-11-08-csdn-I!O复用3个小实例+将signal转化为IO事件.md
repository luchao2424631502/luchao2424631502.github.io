---
title: I/O复用3个小实例+将signal转化为IO事件
date: '2020-11-08 21:59:00'
permalink: 2020/11/08/csdn/I!O复用3个小实例+将signal转化为IO事件/
categories:
- 计算机网络
tags:
- socket
---

I/O复用3个小实例:

1. nonblock connect():**利用error:EINPROGRESS**

   > **非阻塞connect()**
   >
   > man手册connect()
   >
   > The socket is nonblocking and the connection cannot be completed immediately. (UNIX domain sockets failed with EAGAIN instead.) It is possible to select(2) or poll(2) for completion by selecting the socket for writing. After select(2) indicates writability, use getsockopt(2) to read the SO\_ERROR option at level SOL\_SOCKET to determine whether connect() completed successfully (SO\_ERROR is zero) or unsuccessfully (SO\_ERROR is one of the usual error codes listed here, explaining the reason for the failure).
   >
   > 非阻塞socket发起连接不能立马完成,利用io多路的写事件,然后用getsocketopt拿到socket的error,判断error是否==0,=0表示连接成功

   ```c
#include "me.h"
#define BUFFER_SIZE 1023

int setnonblocking(int fd)
{
    int old_option = fcntl(fd,F_GETFL);
    int new_option = old_option | O_NONBLOCK;
    fcntl(fd,F_SETFL,new_option);
    return old_option;
}

//Linux下nonblock-connect()
int unblock_connect(const char *ip,int port,int time)
{
    struct sockaddr_in addr;
    memset(&addr,0,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET,ip,&addr.sin_addr);

    int sockfd = socket(AF_INET,SOCK_STREAM,0);
    int fdopt = setnonblocking(sockfd);//fdopt保存的是原来的fd status
    int ret = connect(sockfd,(struct sockaddr*)&addr,sizeof(addr));
    // 非阻塞connect直接连接成功
    if (ret == 0)
    {
        printf("connect with server immediately\n");
        fcntl(sockfd,F_SETFL,fdopt);
        return sockfd;
    }
    else if (errno != EINPROGRESS)
    {
        printf("unblock connect not support\n");
        return -1;
    }
    //select使用
    fd_set readfds;
    fd_set writefds;
    struct timeval timeout;

    FD_ZERO(&readfds);
    FD_SET(sockfd,&writefds);
    
    timeout.tv_sec = time;
    timeout.tv_usec = 0;

    ret = select(sockfd + 1,&readfds,&writefds,NULL,&timeout);
    if (ret <= 0)
    {
        //超时未发生,或者有错误
        printf("connection time out\n");
        close(sockfd);
        return -1;
    }

    //或者sockfd不在返回的writefds表中
    if (!FD_ISSET(sockfd,&writefds))
    {
        printf("no events on sockfd found\n");
        close(sockfd);
        return -1;
    }

    //E IN PROGRESS 情况,
    int error = 0;
    socklen_t length = sizeof(error);
    //获得SOL_SOCKET的SO_ERROR选项
    if (getsockopt(sockfd,SOL_SOCKET,SO_ERROR,&error,&length) < 0)
    {
        printf("get socket option failed\n");
        close(sockfd);
        return -1;
    }

    //error!=0说明不连接不成功,(出现其他错误
    if (error != 0)
    {
        printf("connection failed after select with the error: %d\n",error);
        close(sockfd);
        return -1;
    }
    //连接成功
    printf("connection ready after select with the socket: %d\n",sockfd);
    fcntl(sockfd,F_SETFL,fdopt);//恢复成 block fd
    return sockfd;
}

int main(int argc,char* argv[])
{
    if (argc <= 2)
        error_handle("argc <= 2")
    const char* ip = argv[1];
    int port = atoi(argv[2]);
    
    int sockfd = unblock_connect(ip,port,10);
    if (sockfd < 0)
        return 1;
    close(sockfd);
    return 0;
}
```

   在\*inx下不具有移植性
2. epoll实现监听同一端口的tcp和udp服务

   ```c
#include "me.h"

#define MAX_EVENT_NUMBER 1024
#define TCP_BUFFER_SIZE 512
#define UDP_BUFFER_SIZE 1024

int setnonblocking(int fd)
{
    int old_option = fcntl(fd,F_GETFL);
    int new_option = old_option | O_NONBLOCK;
    fcntl(fd,F_SETFL,new_option);
    return old_option;
}

void addfd(int epollfd,int fd)
{
    struct epoll_event event;
    event.data.fd = fd;
    event.events = EPOLLIN | EPOLLET;//边沿触发模式
    epoll_ctl(epollfd,EPOLL_CTL_ADD,fd,&event);
    setnonblocking(fd);
}

int main(int argc,char* argv[])
{
    if (argc <= 2)
        error_handle("argc <= 2")
    const char *ip = argv[1];
    int port = atoi(argv[2]);
    
    struct sockaddr_in addr;
    memset(&addr,0,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET,ip,&addr.sin_addr);

    //创建TCP SOCKET并且bind and listen
    int listenfd = socket(AF_INET,SOCK_STREAM,0);
    assert(listenfd >= 0);

    int ret = bind(listenfd,(struct sockaddr*)&addr,sizeof(addr));
    assert(ret != -1);

    ret = listen(listenfd,5);
    assert(ret != -1);

    //创建UDP SOCKET
    memset(&addr,0,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET,ip,&addr.sin_addr);

    int udpfd = socket(AF_INET,SOCK_DGRAM,0);
    assert(udpfd >= 0);

    //监听相同端口
    ret = bind(udpfd,(struct sockaddr*)&addr,sizeof(addr));
    assert(ret != -1);

    struct epoll_event events[MAX_EVENT_NUMBER];
    int epollfd = epoll_create(5);
    assert(epollfd != -1);

    //注册TCP UDP 监听socket上的可读事件
    addfd(epollfd,listenfd);
    addfd(epollfd,udpfd);

    while(1)
    {
        int number = epoll_wait(epollfd,events,MAX_EVENT_NUMBER,-1);//一直阻塞到有事件发生
        if (number < 0)
        {
            printf("epoll failure\n");
            break;
        }

        for (int i=0; i<number; i++)
        {
            int sockfd = events[i].data.fd;
            if (sockfd == listenfd)
            {
                struct sockaddr_in client;
                socklen_t client_addrlength = sizeof(client);
                int connfd = accept(sockfd,(struct sockaddr*)&client,&client_addrlength);
                addfd(epollfd,connfd);
            }
            //udp socket有EPOLLIN事件应该是可读
            else if (sockfd == udpfd)
            {
                char buf[UDP_BUFFER_SIZE];
                memset(buf,'\0',UDP_BUFFER_SIZE);
                struct sockaddr_in client;
                socklen_t client_addrlength = sizeof(client);
                ret = recvfrom(sockfd,buf,UDP_BUFFER_SIZE-1,0,(struct sockaddr*)&client,&client_addrlength);
                if (ret > 0)//echo服务
                    sendto(sockfd,buf,UDP_BUFFER_SIZE-1,0,(struct sockaddr*)&client,client_addrlength);
            }
            else if (events[i].events & EPOLLIN)
            {
                //建立TCP连接的新加入的TCP SOCKET
                char buf[TCP_BUFFER_SIZE];
                //ET模式不重复触发,循环读取完毕
                while(1)
                {
                    memset(buf,'\0',TCP_BUFFER_SIZE);
                    ret = recv(sockfd,buf,TCP_BUFFER_SIZE-1,0);
                    if (ret < 0)
                    {
                        if (errno == EAGAIN || errno == EWOULDBLOCK)
                            break;//下次再处理
                        close(sockfd);//其他的error,
                        epoll_ctl(epollfd,EPOLL_CTL_DEL,sockfd,NULL);
                        break;
                    }
                    else if (ret == 0)
                    {
                        close(sockfd);
                        epoll_ctl(epollfd,EPOLL_CTL_DEL,sockfd,NULL);
                        break;
                    }
                    else {//正常接收,正常发送
                        send(sockfd,buf,ret,0);
                    }
                }
            }
            else {
                printf("something else happened \n");
            }
        }
    }

    close(listenfd);
    return 0;
}
```
3. poll实现的聊天室server,

   ```c
#define _GNU_SOURCE
#include "me.h"

#define USER_LIMIT 50
#define BUFFER_SIZE 64
#define FD_LIMIT 65535

//保存client的数据
typedef struct {
    struct sockaddr_in addr;
    char* write_buf;
    char buf[BUFFER_SIZE];
}client_data;

int setnonblocking(int fd)
{
    int old_option = fcntl(fd,F_GETFL);
    int new_option = old_option | O_NONBLOCK;
    fcntl(fd,F_SETFL,new_option);
    return old_option;
}

int main(int argc,char* argv[])
{
    if (argc <= 2)
        error_handle("argc <= 2")
    const char* ip = argv[1];
    int port = atoi(argv[2]);

    struct sockaddr_in addr;
    memset(&addr,0,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET,ip,&addr.sin_addr);

    int listenfd = socket(AF_INET,SOCK_STREAM,0);
    assert(listenfd >= 0);

    int ret = bind(listenfd,(struct sockaddr*)&addr,sizeof(addr));
    assert(ret != -1);

    ret = listen(listenfd,5);
    assert(ret != -1);

    client_data* users = malloc(sizeof(client_data) * FD_LIMIT);
    struct pollfd fds[USER_LIMIT + 1];//最多监听USER_LIMIT个用户
    int user_counter = 0;
    for (int i=0; i <= USER_LIMIT; i++)
    {
        fds[i].fd = -1;
        fds[i].events = 0;
    }

    //把listenfd首先加入到poll事件中
    fds[0].fd = listenfd;
    fds[0].events = POLLIN | POLLERR;
    fds[0].revents = 0;
    
    while(1)
    {
        ret = poll(fds,user_counter+1,-1);
        if (ret < 0)
        {
            printf("poll failure\n");
            break;
        }
        
        //poll会返回所有注册的事件,要遍历一次所有的事件
        for(int i=0; i<user_counter+1; i++)
        {
            //处理新连接
            if ((fds[i].fd == listenfd) && (fds[i].revents & POLLIN))
            {
                struct sockaddr_in client;
                socklen_t client_addrlength = sizeof(client);
                int connfd = accept(listenfd,(struct sockaddr*)&client,&client_addrlength);
                if (connfd < 0)
                {
                    printf("errno is: %d\n",errno);
                    continue;
                }

                /*请求超过连接限制*/
                if (user_counter >= USER_LIMIT)
                {
                    const char* info = "too many users\n";
                    printf("%s",info);
                    send(connfd,info,strlen(info),0);
                    close(connfd);
                    continue;
                }
                
                //保存新连接connfd的信息 
                user_counter++;
                users[connfd].addr = client;
                setnonblocking(connfd);//设置连接sock是non block的
                fds[user_counter].fd = connfd;
                fds[user_counter].events = POLLIN | POLLRDHUP | POLLERR;
                fds[user_counter].revents = 0;
                printf("comes a new user,now have %d users\n",user_counter);
            }
            //fd发生error事件
            else if (fds[i].revents & POLLERR)
            {
                printf("get an error from %d\n",fds[i].fd);
                char errors[100];
                memset(errors,'\0',sizeof(errors));
                socklen_t length = sizeof(errors);
                if (getsockopt(fds[i].fd,SOL_SOCKET,SO_ERROR,errors,&length) < 0)
                    printf("get socket option failed\n");
                continue;
            }
            //客户端关闭连接
            else if (fds[i].revents & POLLRDHUP)
            {
                //客户端资源 / 监听事件 2者移动到i处
                users[fds[i].fd] = users[fds[user_counter].fd];
                fds[i] = fds[user_counter--]; 
                close(fds[i--].fd);
                printf("a client left\n");
            }
            //客户端发来信息
            else if (fds[i].revents & POLLIN)
            {
                int connfd = fds[i].fd;
                memset(users[connfd].buf,'\0',BUFFER_SIZE);
                ret = recv(connfd,users[connfd].buf,BUFFER_SIZE-1,0);
                printf("get %d bytes of client data %s from %d \n",ret,users[connfd].buf,connfd);
                if (ret < 0)
                {
                    if (errno != EAGAIN)//如果是其他错误,则关闭此连接,释放监听事件
                    {
                        close(connfd);
                        users[fds[i].fd] = users[fds[user_counter].fd];
                        fds[i--] = fds[user_counter--];
                    }
                }
                else if (ret == 0)
                {}
                else {//接收到客户端发来的数据,
                    for (int j=1; j<=user_counter; j++)
                    {
                        if (fds[j].fd == connfd)//不需要将信息发送给自己
                            continue;
                        // fds[j].events |= ~POLLIN;
                        fds[j].events &= ~POLLIN;//取消原POLLIN事件
                        fds[j].events |= POLLOUT;//在有接受数据的fd上注册POLLOUT事件
                        users[fds[j].fd].write_buf = users[connfd].buf;
                    }
                }
            }
            //发送待发送的数据
            else if (fds[i].revents & POLLOUT)
            {
                int connfd = fds[i].fd;
                if (!users[connfd].write_buf)
                    continue;
                ret = send(connfd,users[connfd].write_buf,strlen(users[connfd].write_buf),0);
                users[connfd].write_buf = NULL;//清除带发送数据
                // fds[i].events |= ~POLLOUT;
                fds[i].events &= ~POLLOUT;//取消原POLLOUT事件
                fds[i].events |= POLLIN;
            }
        }
    }

    free(users);
    close(listenfd);
    return 0;
}
```

   可以用下面的client来测试聊天室的效果:

   ```c
#include <me.h>
#define BUF_SIZE 100
#define NAME_SIZE 20

void *send_msg(void*);
void *recv_msg(void*);

char name[NAME_SIZE] = "[DEFAULT]";
char msg[BUF_SIZE];

int main(int argc,char *argv[])
{
  int sock;
  struct sockaddr_in serv_adr;
  pthread_t snd_thread,rcv_thread;
  void *thread_return;
  if (argc != 4)
  {
    printf("Usage : %s <IP> <port> <name>\n",argv[0]);
    exit(1);
  }

  sprintf(name,"[%s]",argv[3]);//将名字加入到待发送的buf中 
  sock = socket(AF_INET,SOCK_STREAM,0);

  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
  serv_adr.sin_port = htons(atoi(argv[2]));

  if (connect(sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)) == -1)
    error_handle("connect() error")

  //创建发送和接受消息的线程 
  pthread_create(&snd_thread,NULL,send_msg,(void*)&sock);
  pthread_create(&rcv_thread,NULL,recv_msg,(void*)&sock);

  pthread_join(snd_thread,&thread_return);
  pthread_join(rcv_thread,&thread_return);
  close(sock);
  return 0;
}

void* send_msg(void *arg)
{
  int sock = *((int *)arg);
  char name_msg[NAME_SIZE + BUF_SIZE];
  while(1)
  {
    fgets(msg,BUF_SIZE,stdin);
    if (!strcmp(msg,"q\n") || !strcmp(msg,"Q\n"))
    {
      close(sock);
      exit(0);
    }
    sprintf(name_msg,"%s %s",name,msg);
    write(sock,name_msg,strlen(name_msg));
  }
  return NULL;
}

void* recv_msg(void *arg)
{
  int sock = *((int*)arg);
  char name_msg[NAME_SIZE + BUF_SIZE];
  int str_len;
  while(1)//服务器发送消息到所有客户端 
  {
    str_len = read(sock,name_msg,NAME_SIZE+BUF_SIZE-1);
    if (str_len == -1)
      return (void*)-1;
    name_msg[str_len] = 0;
    fputs(name_msg,stdout); //接受消息,打印到客户端 
  }
  return NULL;
}
```

---

#### 将信号通过全双工pipe转化为IO事件 然后 由IO多路统一处理信号和IO事件

> 利用signal的SA\_RESTART flags,系统调用被信号处理函数中断后能够重新被调用
>
> 这里仅修改了4个信号的默认处理函数,
>
> 通过kill -signo pid测试是否成功转换为IO事件

```c
#include "me.h"
#define MAX_EVENT_NUMBER 1024

int pipefd[2];
int setnonblocking(int fd)
{
    int old_option = fcntl(fd,F_GETFL);
    int new_option = old_option | O_NONBLOCK;
    fcntl(fd,F_SETFL,new_option);
    return old_option;
}

void addfd(int epollfd,int fd)
{
    struct epoll_event event;
    event.data.fd = fd;
    event.events = EPOLLIN | EPOLLET;//边沿触发模式
    epoll_ctl(epollfd,EPOLL_CTL_ADD,fd,&event);
    setnonblocking(fd);//边沿模式下,fd需要nonblock,避免触发后一直被block
}

//信号处理函数
void sig_handler(int signo)
{
    int save_errno = errno;
    int msg = signo;
    send(pipefd[1],(char*)&msg,1,0);//1Byte大小足够表示所有信号了
    errno = save_errno;
}

//注册信号signo的处理函数
void addsig(int signo)
{
    struct sigaction sa;
    memset(&sa,0,sizeof(sa));
    sa.sa_handler = sig_handler;
    sa.sa_flags |= SA_RESTART;//重启被中断的系统调用
    sigfillset(&sa.sa_mask);
    assert(sigaction(signo,&sa,NULL) != -1);
}

int main(int argc,char* argv[])
{
    if (argc <= 2)
        error_handle("argc <= 2")
    printf("pid = %d\n",getpid());
    const char *ip = argv[1];
    int port = atoi(argv[2]);

    struct sockaddr_in addr;
    memset(&addr,0,sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET,ip,&addr.sin_addr);

    int listenfd = socket(AF_INET,SOCK_STREAM,0);
    assert(listenfd >= 0);

    int ret = bind(listenfd,(struct sockaddr*)&addr,sizeof(addr)); 
    if (ret == -1)
    {
        printf("errno is %d\n",errno);
        return 1;
    }
    ret = listen(listenfd,5);
    assert(ret != -1);

    struct epoll_event events[MAX_EVENT_NUMBER];
    int epollfd = epoll_create(5);
    assert(epollfd != -1);
    addfd(epollfd,listenfd);

    //全双工,本地,unnamed socket
    ret = socketpair(AF_UNIX,SOCK_STREAM,0,pipefd);
    assert(ret != -1);
    setnonblocking(pipefd[1]);
    addfd(epollfd,pipefd[0]);

    addsig(SIGHUP);
    addsig(SIGCHLD);
    addsig(SIGTERM);
    addsig(SIGINT);
    bool stop_server = false;

    while(!stop_server)
    {
        int number = epoll_wait(epollfd,events,MAX_EVENT_NUMBER,-1);
        //函数执行错误的原因不是被信号处理程序中断了
        if ((number < 0) && (errno != EINTR))
        {
            printf("epoll failure\n");
            break;
        }

        for (int i=0; i<number; i++)
        {
            int sockfd = events[i].data.fd;
            if (sockfd == listenfd)
            {
                struct sockaddr_in client;
                socklen_t client_addrlength = sizeof(client);
                int connfd = accept(sockfd,(struct sockaddr*)&client,&client_addrlength);
                addfd(epollfd,connfd);
            }
            //本地socket有EPOLLIN事件发生
            else if((sockfd == pipefd[0]) && (events[i].events & EPOLLIN)) 
            {
                int signo;
                char signals[1024];//给每个signal排队
                ret = recv(pipefd[0],signals,sizeof(signals),0);
                if (ret == -1)
                    continue;
                else if (ret == 0)
                    continue;
                else 
                {
                    //接收到由ret个信号处理程序发过来的signo
                    for (int i=0; i<ret; i++)
                    {
                        switch(signals[i])
                        {
                        case SIGCHLD:
                        case SIGHUP:
                            printf("receive SIGCHLD / SIGHUP\n");
                            continue;
                        case SIGTERM:
                        case SIGINT:
                            stop_server = true;
                        }
                    }
                }
            }
            else{}
        }
    }
    printf("close fds\n");
    close(listenfd);
    close(pipefd[0]);
    close(pipefd[1]);
    return 0;
}
```
