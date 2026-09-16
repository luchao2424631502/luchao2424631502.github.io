---
title: apue中多文件makefile关于err_等函数重定义报错
date: '2020-03-15 17:33:00'
permalink: 2020/03/15/csdn/apue中多文件makefile关于err_等函数重定义报错/
categories:
- 系统与底层
- Unix系统编程
tags:
- unix
---

### apue中多文件`makefile`关于`err_*`等函数重定义报错

原因: 守护进程这一章中多个`.c`文件编译,然后在模块`a`编译成功后,另一个模块编译报错,本书作者写的所有`err＿`函数都报错,表明第一次定义在`a`,然后现在又重定义

1. 首先以为是`apue.h`关于条件编译之类的错误(`#ifndef #endif`),于是无论如何修改头文件组织方法都不正确,(**我忽略了编译器的报错是关于error函数的,我本来应该首先定位到重复出现的位置**)

#### #ifndef条件编译的作用:

- **首先理解头文件的作用(再次清晰一下编译流程第一步预处理)**:头文件没啥作用,只是声明源文件函数的接口,不然你`.c`编译成静态动态库后,谁又知道你代码的作用呢?所以头文件只是一个用来放置函数声明的地方,

  `#ifndef`使用场景:

  > **宏名有效范围仅限与单个`.c`源文件**

  在`.h`定义了全局变量,如果多次包含此`.h`,或者另一个`.h`包含了该`.h`(交叉包含),就会造成变量重复定义错误,**通过条件编译来避免此错误**

  当然:头文件定义全局变量这种做法不好(反正我不做)

#### 查看`apue.h`发现最后一行`#include "error.c"`

#### 错误原因:

在`.h`文件中包含`include ".c"`文件,单文件编译时并没有体现出来,及时你多文件下`apue.h`使用了条件编译,但是他的作用域只是单个`.c`,那么每个模块都对`error.c`编译了一次,造成函数定义重复

#### 处理方法:

1. 在`apue.h`中删除`#include "error.c"`
2. 编译时自己加上去

---

- 第13章`13-8`我的`makefile`

```makefile
file=/usr/include/error.c
a:a.o error.o daemonize.o already_running.o 
	gcc a.o error.o daemonize.o already_running.o -o a -lpthread
a.o:a.c
	gcc -c a.c
error.o:$(file)
	gcc -c  $(file)
daemonize.o:daemonize.c
	gcc -c daemonize.c
already_running.o:already_running.c
	gcc -c already_running.c

clean:
	rm a.o error.o daemonize.o already_running.o
```

- `lockfile函数原型`

```c
int
lockfile(int fd) {
	struct flock f1;
	f1.l_type = F_WRLCK;
	f1.l_start = 0;
	f1.l_whence = SEEK_SET;
	f1.l_len = 0;
	return fcntl(fd,F_SETLK,&f1);
}
```
