---
title: GCC__attribute__部分使用方法
date: '2020-12-08 16:37:00'
permalink: 2020/12/08/GCC-attribute-部分使用方法/
categories:
- 编程语言
- 编译与链接
tags:
- GCC
---

### GNU `__attribute__(())`部分使用方法

> 一部分

1. 自定义段(将**全局变量或函数**放入自定义的段)

   例如:linux内核`__init__` `#define __init__ __attribute__((section(".init")))`

   3种写法都可以

   ```c
   #include <stdio.h>
   #define ps(str) printf("%s",str)
   
   int global __attribute__((section(".Data"))) = 42;
   
   __attribute__((section(".test"))) int b = 9;
   
   int __attribute__((section(".test2"))) c = 8;
   
   __attribute__((section(".func")))
   void globalfunc() {}
   
   int main()
   {
       return 0;
}
```

   `gcc -c test.c`

   查看`test.o`的section

   `readeld -a test.o`

   ![1](/images/Selection006.png)
2. `constructor/destructor`属性,如果函数设置`constructor`属性则在**main()之前被**执行,`destructor`同理

   ```c
#include <stdio.h>
#define ps(str) printf("%s\n",str)

__attribute__((constructor))
void constructor()
{
    ps("constructor");
}

__attribute__((destructor))
void destructor()
{
    ps("destructor");
}

int main()
{
    ps("begin");
    ps("end");
    return 0;
}
```

   属性写在返回类型前也可以

   ```c
#include <stdio.h>
#define ps(str) printf("%s\n",str)

void __attribute__((constructor)) constructor()
{
    ps("constructor");
}

void __attribute__((destructor)) destructor()
{
    ps("destructor");
}

int main()
{
    ps("begin");
    ps("end");
    return 0;
}
```
3. cleanup()属性修饰变量,在其作用域结束时执行指定函数

   ```c
#include <stdio.h>
#define ps(str) printf("%s\n",str)
#define pd(d) printf("%d\n",d);

void clean()
{
   ps("变量作用域结束的清理函数"); 
}

struct A
{
    int a;
    int b;
};

int main()
{
    ps("begin");
    {
        int b __attribute__((cleanup(clean))) = 1;
        struct A c __attribute__((cleanup(clean))) = {1,2};
    }
    ps("end");
    return 0;
}
```
