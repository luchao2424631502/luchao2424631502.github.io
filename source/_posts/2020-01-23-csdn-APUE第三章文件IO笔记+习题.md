---
title: APUE第三章文件IO笔记+习题
date: '2020-01-23 17:22:00'
permalink: 2020/01/23/csdn/APUE第三章文件IO笔记+习题/
categories:
- 操作系统
---

# 3 文件IO

> 非缓冲IO,属于POSIX,非IOS C标准
>
> - `stdin stdou stderr`与`STDIN_FILENO STDOUT_FILENO STDERR_FILENO`的关系
>   1. `stdin`等属于`FILE *`类型,在`<stdio.h>`中
>   2. `STDIN_FILENO`等是无符号整数，表示描述符,在`<unistd.h>`中

## 3.1 常用函数

1. open
   ```
#include <fcntl.h>
int open(const char *path,int oflag,.../*标志需要的参数*/)
成功返回fd,否则-1
```
   常见`oflag`:
   1. `O_RDONLY`:只读
   2. `O_WRONLY`:只写
   3. `O_RDWR`:读写
   4. `O_APPEND`:原子操作,(定位＋写)
   5. `O_CREAT`: 文件不存在则创建,后接参数`umask`
   6. `O_SYNC`: 每次`write`等待物理IO操作完成(同步),包括文件内容和文件属性,由于不在磁盘的同一处,那么会进行2次IO,

２. `lseek`

```c
#include <unistd.h>
off_t lseek(int fd,off_t offset,int whence);
```

- `offset`与`whence`有关

1.`SEEK_SET`,距离开始处的偏移量为`offset`  
2.`SEEK_CUR`,在当前文件偏移量处增加,(前面为空则`SEEK_CUR＝０`)  
3.`SEEK_END`,偏移量为文件长度 + `offset`

- 文件空洞:当文件偏移量大于文件长度,写入时,会在文件中构成一个空洞,**且空洞不要求在磁盘上占用存储区**,**新写入的数据需要磁盘块,但原文件尾端和新开始写入位置的空洞不需要分配磁盘块**
- 创建空洞文件,且`od -c file.hole`查看,和`ls -ls`查看文件大小
  ```c
// g++ test.cpp -o test
#include <bits/stdc++.h>
#include "apue.h"
#include <unistd.h>
#include <fcntl.h>  
char buf1[] = "abcdefghij";
char buf2[] = "ABCDEFGHIJ";
int main () {
	int fd;
	if ((fd = creat("file.hole",FILE_MODE)) < 0)
		err_sys("creat error");
	if (write(fd,buf1,10) != 10)
		err_sys("buf1 write error");

	if (lseek(fd,16384,SEEK_SET) == -1)
		err_sys("lseek error");

	if (write(fd,buf2,10) != 10)
		err_sys("buf2 write errro");
    return 0;
}
```

3.`close`

```c
#include <unistd.h> 
int close(int fd);
成功０,失败-1
```

- 进程终止时,内核自动关闭所有打开文件,
- 并且**关闭一个文件时还会释放该进程加在该文件上的所有记录锁(未理解)**

4.`read`

```c
#include <unistd.h>
ssize_t read(int fd,void *buf,size_t nbyte);
成功返回读入字节,0表示文件尾,-1出错
```

5.`write`

```c
＃include <unistd.h>
ssize_t write(int fd,const void *buf,size_t nbyte);
```

#### 文件空洞

- `od -c file.hole`查看文件且`ls -ls`查看文件大小

```c
// g++ test.cpp -o test
#include <bits/stdc++.h>
#include "apue.h"
#include <unistd.h>
#include <fcntl.h>

char buf1[] = "abcdefghij";
char buf2[] = "ABCDEFGHIJ";


int main () {
	int fd;
	if ((fd = creat("file.hole",FILE_MODE)) < 0)
		err_sys("creat error");
	if (write(fd,buf1,10) != 10)
		err_sys("buf1 write error");

	if (lseek(fd,16384,SEEK_SET) == -1)
		err_sys("lseek error");

	if (write(fd,buf2,10) != 10)
		err_sys("buf2 write errro");
    return 0;
}
```

- 当文件偏移量大于文件当前长度,下次写入会在文件中构成一个空洞,且**不占用磁盘空间**,新写入的数据需要分配磁盘块,**空洞:原文件尾端和新写入位置之间不需要分配磁盘空间**

#### 通过`read`和`write`函数复制文件

- 从标准输入读和写出标准输出,可以通过shell来重定向实现文件复制,
- 缓冲区的大小也能影响效率

```c
#include "apue.h"

#define BUFFSIZE 4 

int main () {
	int n;
	char buf[BUFFSIZE];
	while((n = read(STDIN_FILENO,buf,BUFFSIZE)) > 0) 
		if (write(STDOUT_FILENO,buf,n) != n)
			err_sys("write_error");
	if (n < 0)
		err_sys("read error");
	return 0;
}
// 执行
// g++ test.cpp -o test (or gcc
// ./test < 1.in > 1.out
```

## 3.11文件的原子操作

1. 记住多进程打开文件模型（３层）
   > 1.进程表中包含的**文件记录项（矢量）**，
   >
   > > fd是每一项的项号,每一项包括**文件描述符标志(close\_on\_exec)和指向文件表项的指针**
   >
   > 2.内核维护一张文件表,每个表项包括:
   >
   > ```
   > a.文件状态标志
   > b.文件偏移量
   > c.指向Ｖ节点表项的指针
   > ```
   >
   > 3.每个打开文件(或者设备)都有一个Ｖ节点(v-node)，包含了文件类型和对此文件进行各种操作函数的指针.
2. `O_APPEND`标志使得**每次在写入文件之前,都会修改当前偏移量**,将２个操作合并为１一个操作.避免２操作之间处理器会讲进程挂起导致数据被覆盖

## dup函数 (duplication 复制

- 复制现有文件描述符,那么**进程表中文件描述符中有２项的指针都指向相同的内核文件表项**
- 所以共享 1.文件状态标志,2.当前文件偏移量,3.v节点指针
  ```c
#include <unistd.h>
int dup(int fd);
返回复制fd,否则-1
```

  ## fcntl函数
- 读取文件状态标志 ( 其中有５个状态是互斥的,要与`O_ACCMODE`一起使用

```java
#include <bits/stdc++.h>
#include "apue.h"
#include <fcntl.h>
 
int main (int argc,char *argv[]) {
	int val;
	if (argc != 2)
		err_quit("usage: a.out <descriptor#>");

	if ((val = fcntl(atoi(argv[1]),F_GETFL,0)) < 0)
		err_sys("fcntl error for fd %d,",atoi(argv[1]));
	
	switch(val & O_ACCMODE) {
		case O_RDONLY:
			printf("read only");
			break;
		case O_WRONLY:
			printf("write only");
			break;
		case O_RDWR:
			printf("read write");
			break;
		default:
			err_dump("unknown access mode");
	}
	if (val & O_APPEND)
		printf(", append");
	if (val & O_NONBLOCK)
		printf(", nonblocking");
	if (val & O_SYNC)
		printf(", synchronous writes");
#if !defined(_POSIX_C_SOURCE) && defined(O_FSYNC) && (O_FSYNC != O_SYNC)
	if (val & O_FSYNC)
		printf(", synchronous writes");
#endif
	std::cout << "\n";

    return 0;
}
```

c++

```java
#include <bits/stdc++.h>
#include "apue.h"
#include <fcntl.h>
 
int main (int argc,char *argv[]) {
//	std::for_each(argv,argv + argc,[](const char *ch){
//			std::cout << ch << "\n";
//			});
	int val;
	if (argc != 2)
		err_quit("usage: a.out <descriptor#>");
	// 读取数字argv[1],表示文件描述符
	if ((val = fcntl(atoi(argv[1]),F_GETFL,1)) < 0)
		err_sys("fcntl error for fd %d",atoi(argv[1]));

	std::map<int,std::string> stat {
		{O_RDONLY,std::string("read only")},
		{O_WRONLY,std::string("write only")},
		{O_RDWR,std::string("read write")},
		{0x3f3f3f3f,std::string("unknown access mode")}
	};

	for(const auto& i : stat) {
		// 用O_ACCMODE 取得访问方式位,再来比较
		if (std::get<0>(i) == (val & O_ACCMODE)) {
			std::cout << std::get<1>(i); 
			break;
		}
		if (std::get<0>(i) == 0x3f3f3f3f) {
			err_dump(std::get<1>(i).c_str());
			break;
		}
	}
	//上面是互斥属性,下面的属性不互斥
	if (val & O_APPEND)
		std::cout << ", append";
	if (val & O_NONBLOCK)
		std::cout << ", nonblocking";
	if (val & O_SYNC)
		std::cout << ", synchronous writes";
#if !defined(__POSIX_C_SOURCE) && defined(O_FSYNC) && (O_FSYNC != O_SYNC)
	if (val & O_FSYNC)
		std::cout << ", synchronous writes";
#endif 
	std::cout << "\n";	
    return 0;
}
```

### 延迟写

> UNIX内核实现中设有**缓冲区高速缓存**和**页高速缓存**,磁盘IO都通过缓冲区进行.当向文件写入数据时,内核通常先将数据复制到缓冲区中,　　  
> 如果缓冲区尚未写满**等待写满或者当内核需要重用该缓冲区**这时才将缓冲排入输出队列中,直到实际的IO操作,

---

### 课后习题

3.2

```java
#include <bits/stdc++.h>
#include "apue.h"
#include <unistd.h>
 
struct Node {
	int fd;
	Node *next;
};

// 回收所有空间
void
free_fd(Node *head) 
{
	while(head != nullptr) {
		Node *temp = head;
		// 先关闭文件描述符,
		close(head->fd);
		std::cout << "close " << head->fd << "\n";
		//　关闭后回收内存
		free(head);
		head = temp->next;
	}
}

int
mydup2(int fd,int fd2) 
{
	if (fd == fd2)
		return fd;
	//如果fd2已经打开 则先关闭fd2
	close(fd2);
	
	int temp_fd;
	Node *head = (Node *)malloc(sizeof(Node));
	Node *cur = head;
	// fd2 这一个文件描述符没有存
	while((temp_fd = dup(fd)) != fd2) {
		std::cout << "dup " << temp_fd << "\n";
		// 首先判断是否返回出错
		if (temp_fd == -1) {
			// 清楚所有已经分配的fd
			free_fd(head);
			return -1;
		}
		// 分配空间保存多余的且打开的文件描述符
		Node *temp = (Node *)malloc(sizeof(Node));
		temp->next = nullptr;
		temp->fd = temp_fd;
		cur->next = temp;
		cur = temp;
	}
	
	//　回收fd2之前的所有内存
	free_fd(head);

	return fd2;
}

int 
main () 
{
	int fd = mydup2(STDOUT_FILENO,100);
	std::cout << fd;
    return 0;
}
```

3.5 关于dup2的调用顺序

> 调用1: `./a >outfile 2>&1`  
> 调用2: `./a 2>&1 >outfile`
>
> 1. `>`表示将**标准输出**重定向 (默认是1
> 2. `2>&1`表示将**标准错误输出**重定向到**标准输出**
> 3. `2>1`表示将**标准错误输出**重定向到**１**这个文件
> 4. 加入了`&`**应该就是说明要使用文件描述符**

> - 调用１  
>   先将文件描述符１中的指针指向了oufile的文件表项,然后将文件描述符２中的指针指向了文件描述符１的指针指向,所以最终都指向一个内核中的文件表项.
>   ```stylus
// dup2()的调用顺序
3 = open(file)
dup2(3,1)
dup2(1,2)
```

> - 调用２  
>   先将文件描述符2中的指针指向了文件描述符１所指向的内核文件表项,但是文件描述符１中的指针又指向了文件描述符３指向文件表项,最终,２输出在终端,1输出在文件
>   ```stylus
dup2(1,2)
// open的位置不太确定?,可能在第一个?
open(path) = 3
dup2(3,1)
```
>   [参考博客](https://www.cnblogs.com/caolisong/archive/2007/04/25/726896.html)

3.6

- 先创建好文件,测试结果:
  > 使用`O_APPEND`标志打开文件,`read`受到`lseek`的影响,但是`write`不受到`lseek`的影响,(`O_APPEND`标志的原因

```java
#include <bits/stdc++.h>
#include "apue.h"
#include <unistd.h>
#include <fcntl.h>

const int maxn = 1024;
char ReadBuf[maxn]; 
 
int main () {
	std::string path("/home/luchao/Documents/Apue/3/1.out");
	int fd = open(path.c_str(),O_APPEND|O_RDWR);
	std::string content = "abc";
	if (fd == -1)	
		err_sys("open failed");
	int offset = lseek(fd,0,SEEK_END);
	if (offset == -1)
		err_sys("lseek error");

	int ans = read(fd,ReadBuf,maxn);
//	int ans = write(fd,content.c_str(),content.size());
	if (ans == -1)
		err_sys("read error");
	std::cout << "\nread content\n" << ReadBuf;
    return 0;
}
```
