---
title: IO多路复用-select实现简单回声服务
date: '2020-09-04 18:00:00'
permalink: 2020/09/04/csdn/IO多路复用-select实现简单回声服务/
categories:
- 网络与服务
- 网络编程
tags:
- socket
---

### I/O多路复用-select函数

功能:将多个文件描述符统一监视,描述符是否能读写,以及是否发生异常?

```c
int select(int maxfd,fd_set* readfds,fd_set* writefds,fd_set* exceptfds,timeval* timeout);
```

1. fs\_set注册使用由系列宏来完成,将fd\_set看成bit map

   > FD\_ZERO(fd\_set\* fdset); //所有位置位成0
   >
   > FD\_SET(int fd,fd\_set\* fdset);//fd对应bit置位为1
   >
   > FD\_CLR(int fd,fd\_set\* fdset);//fd对应Bit置位为0
   >
   > FD\_ISSET(int fd,fd\_set\* fdset);//判断对应位是否置位
2. 参数

   > maxfd是 **最大描述符编号+1**
   >
   > 参数2-4分别表示监听要 读 / 写 / 异常 的描述符fd\_set,
   >
   > timeout指定超时时间 (可以避免无限阻塞)
   >
   > 返回值>0:表示3个描述符集合中准备好的描述符的个数和
   >
   > ​ =0:指定时间过了,并且无描述符准备好
   >
   > ​ <0:错误
   >
   > **函数返回后对应fd\_set中的bit仍为1表示准备好了,=0则未准备好**

---

#### select实现服务端

> 相比最初的多进程服务器,IO多路复用减少了进程开销

```c
#include <me.h>
#define BUF_SIZE 100

int main(int argc,char *argv[])
{
  int serv_sock,clnt_sock;
  struct sockaddr_in serv_adr,clnt_adr;
  struct timeval timeout;
  fd_set reads,cpy_reads;

  socklen_t adr_sz;
  int fd_max,str_len,fd_num,i;
  char buf[BUF_SIZE];
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

  FD_ZERO(&reads);//
  FD_SET(serv_sock,&reads);
  fd_max = serv_sock;

  while(1)
  {
    cpy_reads = reads;
    timeout.tv_sec = 5;
    timeout.tv_usec = 5000;
    
    if ((fd_num = select(fd_max+1,&cpy_reads,0,0,&timeout)) == -1)//监听读描述符
      break;
    if (fd_num == 0)//serv_sock无反应 
      continue;

    for (i=0; i<fd_max+1; i++)
    {
      if (FD_ISSET(i,&cpy_reads))
      {
        if(serv_sock == i)
        {
          //说明有客户端请求到来 
          adr_sz = sizeof(clnt_adr);
          //接受请求 
          clnt_sock = accept(serv_sock,(struct sockaddr*)&clnt_adr,&adr_sz);
          FD_SET(clnt_sock,&reads);//加入到下一次要监听的读描述符中 
          if (fd_max < clnt_sock)
            fd_max = clnt_sock;
          printf("connected client: %d \n",clnt_sock);
        }else//通过serv_sock加入到fd_set监听队列中的已连接客户端socket 
        {
          // while((str_len = read(i,buf,BUF_SIZE)) != 0)
            // write(i,buf,str_len);
          // FD_CLR(i,&reads);
          // close(i);
          // printf("closed client: %d \n",i);

          str_len = read(i,buf,BUF_SIZE);//这里仅仅回声一条消息(最大BUF_SIZE,但是while每次都会处理到此连接,因此直到处理完成
          if (str_len == 0)
          {
            FD_CLR(i,&reads);//从监听队列中去掉
            close(i);
            printf("closed client: %d \n",i);
          }else
          {
            write(i,buf,str_len);
          }
        }
      }
    }
  }
  close(serv_sock);
  return 0;
}
```
> 只监听了读fd\_set,并且区分serv\_sock,和clnt\_sock,当serv\_sock准备好后,说明有新的连接请求到来,那么accept()后加入到下次监听队列
>
> 如果是clnt\_sock准备好,说明客户端传来了消息,echo回去,因为是while()不断处理,所以不需要一次性等待客户端数据都传送过来并且处理

原始客户端

```c
#include <me.h>

#define BUF_SIZE 1024
int main(int argc,char *argv[])
{
  int sock;
  char message[BUF_SIZE];
  int str_len;
  struct sockaddr_in serv_adr;
  
  if (argc != 3)
  {
    printf("Usage : %s <IP> <port>\n",argv[0]);
    exit(1);
  }

  sock = socket(AF_INET,SOCK_STREAM,0);
  if (sock == -1)
    error_handle("socket() error");
  
  memset(&serv_adr,0,sizeof(serv_adr));
  serv_adr.sin_family       = AF_INET;
  serv_adr.sin_addr.s_addr  = inet_addr(argv[1]);
  serv_adr.sin_port         = htons(atoi(argv[2]));

  if (connect(sock,(struct sockaddr*)&serv_adr,sizeof(serv_adr)) == -1)
    error_handle("connect() error")
  else 
    puts("connected...");

  //已经连接上了服务器
  while(1)
  {
    fputs("Input message(Q to quit): ",stdout);
    fgets(message,BUF_SIZE,stdin);

    if (!strcmp(message,"q\n") || !strcmp(message,"Q\n"))
      break;

    write(sock,message,strlen(message));
    str_len = read(sock,message,BUF_SIZE-1);
    message[str_len] = 0;
    printf("Message from server: %s",message);
  }
  close(sock);
  return 0;
}
```

#### Windows上实现

select第一个参数无意义(因为fd->句柄),那么fd\_set也无顺序可言

```c
#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <WinSock2.h>

#define BUF_SIZE 1024

void ErrorHandling(char *message);

int main(int argc, char* argv[])
{
	WSADATA wsaData;
	SOCKET hServSock, hClntSock;
	SOCKADDR_IN servAdr, clntAdr;
	TIMEVAL timeout;
	fd_set reads, cpyReads; 

	int adrSz;
	int strLen, fdNum;
	unsigned int i;
	char buf[BUF_SIZE];

	if (argc != 2)
	{
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		ErrorHandling("WSAStartup() error");

	hServSock = socket(PF_INET, SOCK_STREAM, 0);
	memset(&servAdr, 0, sizeof(servAdr));
	servAdr.sin_family = AF_INET;
	servAdr.sin_addr.s_addr = htonl(INADDR_ANY);
	servAdr.sin_port = htons(atoi(argv[1]));

	if (bind(hServSock, (SOCKADDR*)&servAdr, sizeof(servAdr)) == SOCKET_ERROR)
		ErrorHandling("bind() error");
	if (listen(hServSock, 5) == SOCKET_ERROR)
		ErrorHandling("listen() error");

	FD_ZERO(&reads);
	FD_SET(hServSock, &reads);

	while (1)
	{
		cpyReads = reads;
		timeout.tv_sec = 5;
		timeout.tv_usec = 5000;
		
		if ((fdNum = select(0, &cpyReads, 0, 0, &timeout)) == SOCKET_ERROR)
			break;
		if (fdNum == 0)
			continue;
		for (i=0; i<reads.fd_count; i++)
		{
			
			if (FD_ISSET(reads.fd_array[i], &cpyReads))
			{
				
				if (reads.fd_array[i] == hServSock)
				{
					adrSz = sizeof(clntAdr);
					hClntSock = accept(hServSock,(SOCKADDR*)&clntAdr,&adrSz);
					
					FD_SET(hClntSock,&reads);
					printf("connected client: %d \n",hClntSock);
				}
				else
				{
					strLen = recv(reads.fd_array[i],buf,BUF_SIZE-1,0);
					if (strLen == 0)
					{
						FD_CLR(reads.fd_array[i],&reads);
						closesocket(cpyReads.fd_array[i]);
						printf("closed client: %d \n",cpyReads.fd_array[i]);
					}
					else
					{
						send(reads.fd_array[i],buf,strLen,0);//echo
					}
				}
			}
		}
	}
	closesocket(hServSock);
	WSACleanup();
	return 0;
}


void ErrorHandling(char* message)
{
	fputs(message,stderr);
	fputc('\n',stderr);
	exit(1);
}
```

客户端

```c
//#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <WinSock2.h>
#include <Ws2tcpip.h>

#define BUF_SIZE 1024
void ErrorHandling(char* message);

int main(int argc, char* argv[])
{
	WSADATA wsaData;
	SOCKET hSocket;
	char message[BUF_SIZE];
	int strLen;
	SOCKADDR_IN servAdr;

	if (argc != 3)
	{
		printf("Usage : %s <IP> <port>\n",argv[0]);
		exit(1);
	}

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		ErrorHandling("WSAStartup() error!");
	
	hSocket = socket(PF_INET,SOCK_STREAM,0);
	if (hSocket == INVALID_SOCKET)
		ErrorHandling("socket() error");

	memset(&servAdr,0,sizeof(servAdr));
	servAdr.sin_family = AF_INET;
	inet_pton(AF_INET, argv[1], &servAdr.sin_addr);
	servAdr.sin_port = htons(atoi(argv[2]));

	if (connect(hSocket, (SOCKADDR*)&servAdr, sizeof(servAdr)) == SOCKET_ERROR)
		ErrorHandling("connect() error!");
	else
		puts("Connected...");

	while (1)
	{
		fputs("Input message(Q to quit): ",stdout);
		fgets(message,BUF_SIZE,stdin);

		if (!strcmp(message,"Q\n") || !strcmp(message,"q\n"))
			break;
		
		send(hSocket,message,strlen(message),0); //������Ϣ
		strLen = recv(hSocket,message,BUF_SIZE-1,0);
		message[strLen] = 0;
		printf("Message from server: %s",message);
	}
	closesocket(hSocket);
	WSACleanup();
	return 0;
}

void ErrorHandling(char* message)
{
	fputs(message,stderr);
	fputc('\n',stderr);
	exit(1);
}
```
> 来自<<TCP/IP 网络编程 尹圣雨>>
