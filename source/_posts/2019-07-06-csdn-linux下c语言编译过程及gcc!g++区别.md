---
title: linux下c语言编译过程及gcc/g++区别
date: '2019-07-06 09:24:00'
permalink: 2019/07/06/csdn/linux下c语言编译过程及gcc!g++区别/
categories:
- 工具与效率
- 构建与调试
---

gcc与g++分别是c/c++的编译器.  
区别:

1. 后缀为.c的文件,gcc当做c程序 g++当做c++程序,后缀为.cpp的两者都认为是c++程序.应为c++语法更严谨,所以g++可能编译不了c程序
2. gcc可以编译c/c++程序,但是gcc只能编译,不能自动和c++程序使用的库连接,所以通常使用g++来完成c++程序的编译和连接

- 有多个c源文件可用一下命令:  
  `gcc -o function main.c function.c`编译生成可执行文件  
  `-o 修改编译出来的文件名称`
- 调用g++命令 编译、连接并生成可执行文件  
  `g++ -o hello hello.c`

c语言编译过程分为4步:

1. 预处理: Preprocessing
2. 汇编/编译:Compilation
3. 集合/组合:Assemble
4. 链接:Linking  
   ![ZdypUH.png](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9zMi5heDF4LmNvbS8yMDE5LzA3LzA1L1pkeXBVSC5wbmc)

> 1. 预处理用于将所有的`#include头文件`以及宏定义替换成真正的内容  
>    预处理文件末尾:  
>    [外链图片转存失败(img-BBRuoMOV-1562376202402)(<https://s2.ax1x.com/2019/07/06/ZwEaKe.png)]>  
>    `gcc -E main.c -o test`

> 2. 第二步汇编是将预处理文件转为特定的汇编代码,(`assemble code`)  
>    `gcc -S main.c -o test.s`
> 3. 第三步 集合/组合 是将汇编代码转换成机器代码(`machine code`),叫做目标文件,二进制格式,`gcc` 调用 `as`命令来完成  
>    `as test.s -o test.o`  
>    `gcc -c test.s -o test.o`
>
> **每一个源文件 都会产生一个目标文件**  
> 4. 将多个目标文件和库文件链接成可执行文件(`executable file`)

总结:

- 编译c`gcc -o main main.c`
- 编译cpp`g++ -o main main.c`
  > 预处理:`gcc -E main.c -o test`  
  > 汇编: `gcc -S main.c -o test.s`  
  > 组合: `gcc -c test.s -o test.o`  
  >  \ \ \ `as test.s -o test.o`
