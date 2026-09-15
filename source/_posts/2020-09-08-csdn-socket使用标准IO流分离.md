---
title: socket使用标准IO流分离
date: '2020-09-08 15:45:00'
permalink: 2020/09/08/csdn/socket使用标准IO流分离/
categories:
- 计算机网络
---

#### fd和标准IO相互转换

1. fd->FILE\*

   `FILE * fdopen(int fd,const char *mode);`

   ```c
#include <me.h>

int main(void)
{
  FILE *fp;
  int fd = open("news.txt",O_RDWR);
  if (fd == -1)
  {
    fputs("file open error",stdout);
    return -1;
  }

  fp = fdopen(fd,"w");
  fputs("Network C programming \n",fp);
  fclose(fp);
  return 0;
}
```
2. FILE\*->fd

   `int fileno(FILE *fp);`

   ```c
#include <me.h>

int main(void)
{
  FILE *fp;
  int fd = open("news.txt",O_RDWR);
  if (fd == -1)
  {
    fputs("file open error",stdout);
    return -1;
  }

  printf("First file descriptor: %d \n",fd);
  fp = fdopen(fd,"w");//fd转FILE*
  fputs("TCP/IP SOCKET programming \n",fp);
  printf("Second file descriptor: %d\n",fileno(fp)); // FILE* 转 fd 
  fclose(fp);
  return 0;
}
```

#### 回声服务端客户端使用标准IO

server.c

```c
#include <me.h>
#define BUF_SIZE 1024

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  char message[BUF_SIZE];
  int str_len,i;

  struct sockaddr_in serv_adr,clnt_adr;
  socklen_t clnt_adr_sz;
  FILE *readfp,*writefp;
  if (argc != 2)
  {
    printf("Usage : %s <port> \n",argv[0]);
    exit(1);
  }

  serv_sock = socket(AF_INET,SOCK_STREAM,0);
  if (serv_sock == -1)
    error_handle("socket() error")

  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_adr.sin_port = htons(atoi(argv[1]));

  if (bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)) == -1)
    error_handle("bind() error")
  if (listen(serv_sock,5) == -1)
    error_handle("listen() error")

  clnt_adr_sz = sizeof(clnt_adr);
  for (i=0; i<5; i++)
  {
    clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&clnt_adr_sz);
    if (clnt_sock == -1)
      error_handle("accept() error")
    else 
      printf("Connected client %d\n",i+1);
    readfp = fdopen(clnt_sock,"r");
    writefp = fdopen(clnt_sock,"w");
    while(!feof(readfp))
    {
      fgets(message,BUF_SIZE,readfp);
      fputs(message,writefp);
      fflush(writefp);
    }

    fclose(readfp);
    fclose(writefp);
  }

  close(serv_sock);
  return 0;
}
```

---

client.c

```c
#include <me.h>
#define BUF_SIZE 1024
int main(int argc,char *argv[])
{
  int sock;
  char message[BUF_SIZE];
  struct sockaddr_in serv_adr;
  FILE *readfp,*writefp;
  if (argc != 3)
  {
    printf("Usage : %s <IP> <port> \n",argv[0]);
    exit(1);
  }

  sock = socket(AF_INET,SOCK_STREAM,0);
  if (sock == -1)
    error_handle("socket() error")

  //填写服务器信息 
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
  serv_adr.sin_port = htons(atoi(argv[2]));

  if (connect(sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)) == -1)
    error_handle("connect() error")
  else 
    puts("Connected ....");

  //将建立的fd转化成标准IO 
  readfp = fdopen(sock,"r");
  writefp = fdopen(sock,"w");
  while(1)
  {
    fputs("Input message (Q to quit): ",stdout);
    fgets(message,BUF_SIZE,stdin);//拿到数据 
    if (!strcmp(message,"q\n") || !strcmp(message,"Q\n"))
      break;

    fputs(message,writefp);//发送给服务器 
    fflush(writefp);
    fgets(message,BUF_SIZE,readfp);//从服务器接受数据 
    printf("Message from server: %s",message);
  }

  fclose(writefp);
  fclose(readfp);
  return 0;
}
```

---

#### 一个fd通过fdopen形成的2个FILE\*(分别是”r” 和 “w”)想调用fclose传递EOF形成半关闭状态是否可行?

serv.c

```c
#include <me.h>
#define BUF_SIZE 1024

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  FILE *readfp,*writefp;
  struct sockaddr_in serv_adr,clnt_adr;
  socklen_t clnt_adr_sz;
  char buf[BUF_SIZE] = {0,};

  serv_sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_adr.sin_port = htons(atoi(argv[1]));

  bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr));
  listen(serv_sock,5);
  clnt_adr_sz = sizeof(clnt_adr);
  clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&clnt_adr_sz);
  
  readfp = fdopen(clnt_sock,"r");
  writefp = fdopen(clnt_sock,"w");

  fputs("FROM SERVER: Hi~ client? \n",writefp);//向服务器发送 
  fputs("I love all of the world \n",writefp);
  fputs("You are awesome! \n",writefp);
  fflush(writefp);

  fclose(writefp);//认为是半关闭 ?
  //判断是否还能够接收到数据(目前认为是能够接受到数据的  
  fgets(buf,sizeof(buf),readfp);
  fputs(buf,stdout);//把接受到的数据给标准输出 
  fclose(readfp);
  return 0;
}
```

clnt.c

```c
#include <me.h>
#define BUF_SIZE 1024 

int main(int argc,char *argv[])
{
  int sock;
  char buf[BUF_SIZE];
  struct sockaddr_in serv_adr;
  FILE *readfp,*writefp;

  sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
  serv_adr.sin_port = htons(atoi(argv[2]));

  connect(sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr));

  readfp = fdopen(sock,"r");
  writefp = fdopen(sock,"w");

  //客户端连接成功后,开始传输数据 
  while(1)
  {
    //从服务器接受数据
    if (fgets(buf,sizeof(buf),readfp) == NULL)//第一次收到EOF,返回NULL
      break;
    fputs(buf,stdout);//将接收到的数据打印出来 
    fflush(stdout);
  }

  //判断是否是半关闭 
  fputs("FROM CLIENT: THANK you! \n",writefp);
  fflush(writefp);
  fclose(writefp);
  fclose(readfp);
  return 0;
}
```
> 运行后发现fclose后唯一fd关闭导致socket也关闭了
>
> 被关闭的原因是只有一个fd对应socket,fclose关闭导致fd关闭

#### dup复制fd

`int dup(int fd);`

### 实现关于标准IO流的半关闭

> 通过复制一个fd后,每一个FILE`*`对应一个fd,但是即使fclose关闭一个FILE\*后,唯一的一个fd也能同时IO,
>
> 那么要先设置socket,使其先半关闭(shutdown发送EOF进入半关闭)然后在fclose关闭FILE\*

```c
#include <me.h>
#define BUF_SIZE 1024 

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  FILE *readfp,*writefp;

  struct sockaddr_in serv_adr,clnt_adr;
  socklen_t clnt_adr_sz;
  char buf[BUF_SIZE] = {0,};

  serv_sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_adr.sin_port = htons(atoi(argv[1]));

  bind(serv_sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr));
  listen(serv_sock,5);

  clnt_adr_sz = sizeof(clnt_adr);
  clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&clnt_adr_sz);

  readfp = fdopen(clnt_sock,"r");
  writefp = fdopen(dup(clnt_sock),"w");

  fputs("FROM SERVER: Hi~ Client? \n",writefp);
  fputs("I love all of the world\n",writefp);
  fputs("You are awesome! \n",writefp);
  fflush(writefp);

  //开启半关闭 
  shutdown(fileno(writefp),SHUT_WR);
  // shutdown(fileno(readfp),SHUT_WR);
  fclose(writefp);

  fgets(buf,sizeof(buf),readfp);
  fputs(buf,stdout);
  fclose(readfp);
  return 0;
}
```
> 来自<<TCP/IP 网络编程 尹圣雨>>
