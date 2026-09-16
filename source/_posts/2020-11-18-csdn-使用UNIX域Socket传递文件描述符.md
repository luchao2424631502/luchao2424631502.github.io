---
title: 使用UNIX域Socket传递文件描述符
date: '2020-11-18 23:33:00'
permalink: 2020/11/18/csdn/使用UNIX域Socket传递文件描述符/
categories:
- 网络与服务
- 网络编程
---

#### [使用UNIX域Socket传递文件描述符]

> 使用sendmsg(),recvmsg()

1. fork后子进程继承父进程进程表象的描述符表(所有描述符项目),**所以子进程和父进程相同的fd都共享了相同文件表象.**

   ![1](https://img-blog.csdnimg.cn/20201118233138631.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

2. 不同进程打开相同路径文件的情况:

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201118233205715.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

操作文件的i节点是相同的,但是在内核文件表中维护了2个不同的文件表象(2个独立的进程),

#### 2个进程间传递fd的目的就是使2个进程的fd共享一个相同的文件表项

​ ![3](https://img-blog.csdnimg.cn/20201118233218235.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

fork实现了父进程->子进程的fd传递,

独立进程间通过sendmsg/recvmsg的cmsghdr实现

```c
struct msghdr{
	void *msg_name;
	socklen_t msg_namelen;
	struct iovec *msg_iov;
	int msg_iovlen;
	void *msg_control;
	socklen_t msg_controllen;
	int msg_flags;
};
```

msg\_control字段指向struct cmsghdr(控制信息头)结构

msg\_controllen=控制信息的字节数

```c
struct cmsghdr{
	socklen_t cmsg_len;
	int cmsg_level;
	int cmsg_type;
	//这里是跟随的额外数据
};
```

发送fd需要将:

1. cmsg\_len设为cmsghdr+int(描述符)长度
2. cmg\_level设置为SOL\_SOCKET
3. cmsg\_type设置为SCM\_RIGHTS(表明在传送访问权,SCM=’Socket-level Control Message’套接字级别控制消息) **访问权仅能通过UNIX域Socket传送**,fd在cmsg\_type字段之后存储,**通过CMSG\_DATA()获得次整形量的指针**

```c
#include <sys/socket.h>

unsigned char* CMSG_DATA(struct cmsghdr* cp);//返回指针,指向与cmsghdr结构相关联的数据
unsigned int CMSG_LEN(unsigned int nbytes);//返回为cmsghdr添加nbytes长的数据对象后的cmsghdr的长度
```

查看CMSG\_LEN返回的值大小

```c
#include "me.h"

int main()
{
  printf("[cmsghdr size] = %d\n[CMSG_LEN] = %d\n",sizeof(struct cmsghdr),CMSG_LEN(sizeof(int)));
  return 0;
}
```

#### 子进程向父进程传递fd

```c
#include "me.h"

int CONTROL_LEN = CMSG_LEN(sizeof(int));//返回为sizeof(int)长度的数据对象分配的长度

void send_fd(int fd,int fd_to_send)
{
  struct iovec iov[1];
  struct msghdr msg;
  char buf[2];

  iov[0].iov_base = buf;
  iov[0].iov_len = 1;
  msg.msg_name = NULL;
  msg.msg_namelen = 0;
  msg.msg_iov = iov;
  msg.msg_iovlen = 1;

  struct cmsghdr cm;
  cm.cmsg_len = CONTROL_LEN;
  cm.cmsg_level = SOL_SOCKET;
  cm.cmsg_type = SCM_RIGHTS;
  *(int*)CMSG_DATA(&cm) = fd_to_send;
  
  msg.msg_control = &cm;
  msg.msg_controllen = CONTROL_LEN;

  // printf("[cmsghdr size] = %d\n[send_fd CONTROL_LEN] = %d\n",sizeof(struct cmsghdr),CONTROL_LEN);

  sendmsg(fd,&msg,0);
}

int recv_fd(int fd)
{
  struct iovec iov[1];
  struct msghdr msg;
  char buf[2];

  iov[0].iov_base = buf;
  iov[0].iov_len = 1;
  msg.msg_name = NULL;
  msg.msg_namelen = 0;
  msg.msg_iov = iov;
  msg.msg_iovlen = 1;

  struct cmsghdr cm;
  msg.msg_control = &cm;
  msg.msg_controllen = CONTROL_LEN;
  printf("[recv_fd CONTROL_LEN] = %d\n",CONTROL_LEN);

  recvmsg(fd,&msg,0);
  int fd_to_read = *(int*)CMSG_DATA(&cm);
  return fd_to_read;//转化为此进程的最小可用fd了
}

int main()
{
  printf("[parent pid]: %d\n",getpid());
  int pipefd[2];
  int fd_to_pass = 0;
  int ret = socketpair(AF_UNIX,SOCK_DGRAM,0,pipefd);
  assert(ret != -1);

  pid_t pid = fork();
  assert(pid >= 0);
  
  if (pid == 0)
  {
    printf("[child pid]: %d\n",getpid());
    close(pipefd[0]);
    fd_to_pass = open("1.in",O_RDWR,0666);
    printf("[child process]: fd_to_pass = %d\n",fd_to_pass);
    send_fd(pipefd[1],(fd_to_pass > 0) ? fd_to_pass : 0);
    sleep(400);
    close(fd_to_pass);
    exit(0);
  }
  close(pipefd[1]);
  fd_to_pass = recv_fd(pipefd[0]);
  
  char buf[1024];
  memset(buf,'\0',1024);
  read(fd_to_pass,buf,1024);
  printf("[parent process]: fd_to_pass = %d\n",fd_to_pass);
  printf("I got fd %d and data %s \n",fd_to_pass,buf);
  sleep(500);
  close(fd_to_pass);
  exit(0);
}
```

查看当前目录下1.in文件

通过lsof查看传递过去的fd的num并不是和原来的一样的,但是传递成功(得到了文件内容)

lsof -p 父进程

![4](https://img-blog.csdnimg.cn/20201118233234929.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

lsof -p 子进程

![5](https://img-blog.csdnimg.cn/20201118233245213.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

可以看到传递过去后fd的num是不同的
