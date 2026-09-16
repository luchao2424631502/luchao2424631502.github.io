---
title: Orange‘s:disp_str()字符串函数第二次调用乱码原因
date: '2020-07-14 23:08:00'
permalink: 2020/07/14/csdn/Orange‘s!disp_str()字符串函数第二次调用乱码原因/
categories:
- 系统与底层
- 自制操作系统
tags:
- 于渊    操作系统  Orange S
---

> 书上.c编译参数加上`-m32`,LD链接参数`-m elf_i386`

去掉此Bug后正好Makefile也完成了

---

第2次调用disp\_str()时乱码,Google后说是ebx没有进栈被保护的原因,果然没错,但是为什么呢？

断点打到kernel起始执行地址:`0x30400`

单步调试发现call cstart后  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200714230545316.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

如果第一次ebx被破坏后,第二次调用指向的参数地址错误,并且循环了多次

---

调试信息:

disp\_str()第一次执行完毕后物理地址 0x304fd

memcpy()执行完毕物理地址: 0x30524

disp\_str()入口地址 0x304c0
