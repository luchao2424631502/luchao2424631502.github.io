---
title: recv函数MSG_PEEK|MSG_DONTWAIT|MSG_OOB选项
date: '2020-09-05 16:10:00'
permalink: 2020/09/05/csdn/recv函数MSG_PEEK!MSG_DONTWAIT!MSG_OOB选项/
categories:
- 网络与服务
- 网络编程
---

#### send recv函数

```c
ssize_t send(int sockfd,const void* buf,size_t nbytes,int flags);
ssize_t recv(int sockfd,void* buf,size_t nbytes,int flags);
```

之前一直在linux下使用read和write函数,

MSG\_OOB:TCP只有紧急模式,没有带外数据

MSG\_DONTWAIT:调用函数时不阻塞

MSG\_PEEK:只有recv能用,检测input缓冲区是否有数据,(缓冲区数据不变

#### 不阻塞检查输入缓冲:

peek\_recv.c

```c
#include <me.h>
#define BUF_SIZE 30 

int main(int argc,char *argv[])
{
  int acpt_sock,recv_sock;
  struct sockaddr_in acpt_adr,recv_adr;
  int str_len,state;
  socklen_t recv_adr_sz;
  char buf[BUF_SIZE];
  if (argc != 2)
  {
    printf("Usage : %s <port>\n",argv[0]);
    exit(1);
  }
  
  //绑定服务端套接字
  acpt_sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&acpt_adr,0,sizeof(acpt_adr));
  acpt_adr.sin_family = AF_INET;
  acpt_adr.sin_addr.s_addr = htonl(INADDR_ANY);
  acpt_adr.sin_port = htons(atoi(argv[1]));

  if (bind(acpt_sock,(struct sockaddr*)&acpt_adr,sizeof(acpt_adr)) == -1)
    error_handle("bind() error")

  listen(acpt_sock,5);


  recv_adr_sz = sizeof(recv_adr);
  recv_sock = accept(acpt_sock,(struct sockaddr*)&recv_adr,&recv_adr_sz);

  //以非阻塞的方式验证待读入的数据是否存在,不存在则一直询问?,存在则退出
  while(1)
  {
    str_len = recv(recv_sock,buf,sizeof(buf)-1,MSG_PEEK | MSG_DONTWAIT);
    if (str_len > 0)
      break;
  }
  buf[str_len] = 0;
  printf("Buffering %d bytes: %s \n",str_len,buf);//拿到缓冲区的数据,
  
  str_len = recv(recv_sock,buf,sizeof(buf)-1,0);//读入后会删除缓冲区
  buf[str_len] = 0;
  printf("Read again: %s \n",buf);
  close(acpt_sock);
  close(recv_sock);
  return 0;
}
```

peek\_send.c:

```c
#include <me.h>

int main(int argc,char *argv[])
{
  int sock;
  struct sockaddr_in send_adr;
  if (argc != 3)
  {
    printf("Usage: %s <IP> <port> \n",argv[0]);
    exit(1);
  }

  sock = socket(AF_INET,SOCK_STREAM,0);
  memset(&send_adr,0,sizeof(send_adr));
  send_adr.sin_family = AF_INET;
  send_adr.sin_addr.s_addr = inet_addr(argv[1]);
  send_adr.sin_port = htons(atoi(argv[2]));

  if (connect(sock,(struct sockaddr*)&send_adr,sizeof(send_adr)) == -1)
    error_handle("connect() error")

  write(sock,"1234",strlen("1234"));
  close(sock);
  return 0;
}
```

---

#### Windows下接受 out-of-band数据(MSG\_OOB)

> 利用select的第3个fd\_set,”异常”指的是不同寻常的程序执行流,Out-of-band数据也属于异常

```c
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <Ws2tcpip.h>

#define BUF_SIZE 30
void ErrorHandling(char*);

int main(int argc,char *argv[])
{
	WSADATA wsaData;
	SOCKET hAcptSock, hRecvSock;

	SOCKADDR_IN recvAdr;
	SOCKADDR_IN sendAdr;
	int sendAdrSize, strLen;
	char buf[BUF_SIZE];
	int result;

	fd_set read, except, readCopy, exceptCopy;
	struct timeval timeout;
	if (argc != 2)
	{
		printf("Usage: %s <port>\n",argv[0]);
		exit(1);
	}

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		ErrorHandling("WSAStartup() error!");

	hAcptSock = socket(AF_INET,SOCK_STREAM,0);
	memset(&recvAdr,0,sizeof(recvAdr));
	recvAdr.sin_family = AF_INET;
	recvAdr.sin_addr.s_addr = htonl(INADDR_ANY);
	recvAdr.sin_port = htons(atoi(argv[1]));

	if (bind(hAcptSock, (SOCKADDR*)&recvAdr, sizeof(recvAdr)) == SOCKET_ERROR)
		ErrorHandling("bind() error");

	if (listen(hAcptSock, 5) == SOCKET_ERROR)
		ErrorHandling("listen() error");

	sendAdrSize = sizeof(sendAdr);
	hRecvSock = accept(hAcptSock,(SOCKADDR*)&sendAdr,&sendAdrSize);
	FD_ZERO(&read);
	FD_ZERO(&except);
	FD_SET(hRecvSock,&read);
	FD_SET(hRecvSock,&except);

	while (1)
	{
		readCopy = read;
		exceptCopy = except;

		timeout.tv_sec  = 5;
		timeout.tv_usec = 0;

		result = select(0,&readCopy,0,&exceptCopy,&timeout);

		if (result > 0)//��SOCKET���׼����
		{
			if (FD_ISSET(hRecvSock, &exceptCopy))//�ж��Ƿ���յ�Out-of-band����
			{
				strLen = recv(hRecvSock,buf,BUF_SIZE-1,MSG_OOB);
				buf[strLen] = 0;
				printf("Urgent message: %s \n",buf);
			}

			if (FD_ISSET(hRecvSock, &readCopy))//�ж��Ƿ���յ���������
			{
				strLen = recv(hRecvSock,buf,BUF_SIZE-1,0);
				if (strLen == 0)
				{
					closesocket(hRecvSock);
					break;
				}
				else
				{
					buf[strLen] = 0;
					puts(buf);
				}
			}
		}
	}

	closesocket(hAcptSock);
	WSACleanup();
	return 0;
}
void ErrorHandling(char* message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}
```

---

send.c

```c
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <Ws2tcpip.h>

#define BUF_SIZE 30
void ErrorHandling(char *);

int main(int argc,char *argv[])
{//ʹ��send������Ϣ������һ����ͨ�Ŀͻ��˶���
	WSADATA wsaData;
	SOCKET hSocket;
	SOCKADDR_IN sendAdr;
	if (argc != 3)
	{
		printf("Usage: %s <IP> <port>\n",argv[0]);
		exit(1);
	}

	//ע��winsock��
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		ErrorHandling("WSAStartup() error!");

	hSocket = socket(AF_INET,SOCK_STREAM,0);
	memset(&sendAdr,0,sizeof(sendAdr));
	sendAdr.sin_family = AF_INET;
	//sendAdr.sin_addr.s_addr = inet_addr(argv[1]);
	inet_pton(AF_INET,argv[1],&sendAdr.sin_addr);
	sendAdr.sin_port = htons(atoi(argv[2]));

	if (connect(hSocket, (struct sockaddr*)&sendAdr, sizeof(sendAdr)) == SOCKET_ERROR)
		ErrorHandling("connect() error");

	send(hSocket,"123",3,0);
	send(hSocket,"4",1,MSG_OOB);
	send(hSocket,"567",3,0);
	send(hSocket,"890",3,MSG_OOB);

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
