---
title: linux下在进程中加载执行纯2进制可执行文件bin
date: '2020-09-19 21:04:00'
permalink: 2020/09/19/csdn/linux下在进程中加载执行纯2进制可执行文件bin/
categories:
- 系统与底层
- Unix系统编程
---

[此博客来自他人,下面是自己的见解,因为正好用到相关内容](https://blog.csdn.net/Pedroa/article/details/53842115)

> objdump对纯2进制文件(hello.bin)反汇编
>
> objdump -m i386 -b binary -D hello.bin
>
> -m:指出反汇编目标架构
>
> -b:文件格式

#### 在进程中加载执行纯2进制可执行文件bin

1. mmap把2进制文件映射到进程用户内存空间,
2. 将程序控制权交给bin

---

linux下用汇编通过中断调用api打印一个hello world (nasm版本),

```plain
[section .data]
output:	db "Hello World",0
length  db 12
[section .text]
global _start

_start:
	mov eax,4
	mov ebx,1
	mov ecx,output
	mov edx,[length] 
	int 0x80	;sys_write(1,buf,size)
	mov eax,1
	mov ebx,0	;sys_exit
	int 0x80
```
> 软中断调用api [参数意义](https://blog.csdn.net/xiaominthere/article/details/17287965)

```
1. 编译成.o可重定位文件 `nasm -f elf64 hello.s -o hello.o`
```

> 1. 因为bin文件被映射到进程内存空间,控制流jmp到映射的内存首地址就能够继续执行可执行二进制文件bin,
> 2. 因为编译的时候指定bin的text段入口地址是0x00000000,链接完后text段的符号重定位值是根据入口地址=0决定的,(对此hello.s文件而言)
> 3. 那么如果映射到虚拟内存空间地址A时,bin中的在链接期间可重定位符号的偏移量要加上A,

​ 查看hello.o中的重定位信息,`objdump -D -r hello.o`

​ ![1](https://img-blog.csdnimg.cn/20200919210211533.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

​ 看到的符号在section中的偏移量分别是0x0B和0x12,并且在link前值都是0

​ ![3](https://img-blog.csdnimg.cn/20200919210230265.PNG#pic_center)

2. 静态链接: 将.data和.text合成一个.text section

   link script `test.ld`

   ```plain
SECTIONS
{
. = 0x00000000;
.text : {
    *(.text) 
    *(.data)
 } 
}
```

   `ld -T test.ld hello.o -o hello.elf`

   ![2](https://img-blog.csdnimg.cn/20200919210246269.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

   原来的重定位符号之被link修改,(根据.text的入口地址

所以在进程中加上加载到的虚拟地址就能成功执行纯2进制代码

```c
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

int main()
{
	int fd;
	int ret;
	unsigned char *buf;
	struct stat stat;
	void *res;
	unsigned int ImageBase;
	int rebase[2] = {0x0B,0x12};
	unsigned char *temp;

	//ImageBase = 0x50000000;
	ImageBase = 0x00010000;

	fd = open("hello.bin",O_RDWR);
	if (fd < 0)
	{
		perror("fd");
		return -1;
	}

	ret = fstat(fd,&stat);
	if (ret < 0)
	{
		perror("fstat");
		return -1;
	}

	buf = (unsigned char *)malloc(stat.st_size);
	if (buf == NULL)
	{
		perror("allocate");
		return -1;
	}

	ret = read(fd,buf,stat.st_size);
	if (ret < 0 || ret != stat.st_size)
	{
		perror("read");
		return -1;
	}

	res = mmap((void*)ImageBase,stat.st_size,PROT_EXEC | PROT_WRITE | PROT_READ,MAP_PRIVATE,fd,0);
	if (res == MAP_FAILED)
	{
		perror("mmap");
		return -1;
	}

	printf("%p \n",res);
	
	for (int i=0; i<2; i++)
		*(unsigned int *)((char *)res + rebase[i]) += ImageBase;

	temp = (unsigned char *)res;
	for (int i=0; i<0x100; i++)
		printf("%02X%s",*temp++,(i+1)%0x10?" " : "\n");

//	__asm__ volatile ("\n\t"\
//			"movl $1,%%eax\n\t"\
//			"jmp *%0\n\t"\
//			::"mem"(res):
//			);
	__asm__ volatile ("\n\t"\
			"jmp *%0\n\t"\
			::"mem"(res):
			);
	printf("done\n");
	return 0;
}
```

![4](https://img-blog.csdnimg.cn/20200919210305437.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)
