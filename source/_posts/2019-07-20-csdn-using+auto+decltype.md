---
title: using+auto+decltype
date: '2019-07-20 15:31:00'
permalink: 2019/07/20/csdn/using+auto+decltype/
categories:
- 编程语言
- C与C++
tags:
- c++11 auto decltype
---

类型别名(`type alias`)

1. `typedef double *p`,`p`是`double*`的同义词  
   `typedef char *pstring`,`pstring`是`char*`的同义词  
   `const pstring cstr = 0;//`**一个常量指针**  
   `const char *p;//` **一个指向char常量的指针**

- `const pstring cstr != const char *cstr`. **别将别名替换成原本样子来理解**  
  `const char *cstr`:编译器理解为`const char`**变为一种数据类型**.**cstr指向一个char常量**,**而类型别名 const pstring 的数据类型是指针**,所以是**指针常量**.

2. c++11:`using pd = double*`,`pd`是`double*`的同义词

auto类型说明符

- 编译器通过初始值来推算变量的类型,**所以auto声明时要初始化,且多变量时类型不相同时编译器会适当改变**
  ```angelscript
int a=1;
double b=2.1;
auto autonum = a + b;
cout << autonum; //3.1
```
- 当**引用**作为初始化的值时,其实**是引用绑定对象的值**来初始化.  
  编译器以**引用绑定对象的类型**作为**auto**类型.
  ```angelscript
int i=0;
int &r = i;
auto c = r;//c类型是int,(&引用本身不是一个对象)
```
- `auto`**会忽略顶层`const`**.

```nim
const int i = 1;
const int& r = i;
auto b = i;// b 为 int,顶层const被忽略掉了
auto c = r; //c是int,r绑定的i的顶层const被忽略
auto *p = &i; //p是指向常量的指针,常量i取地址是底层的const
```

- `auto`的**引用不会忽略顶层const**,
  ```cpp
const int i = 1;
auto &c = i; //c是对int常量的引用
```

decltype类型说明符

- `decltype(f()) variable = x; //编译器不调用函数f,而是函数f被调用时的返回类型作为variable的类型`
- `decltype()`参数是一个**变量**,返回该变量的类型.对比`auto`不取消顶层`const`
  ```cpp
const int i = 0;
const &j = i;
decltype(i) x = 0;// const int x = 0;
decltype(j) y = x;// const int& y = x;
decltype(j) z; //错误,引用必须初始化
```
- 当参数为**表达式时**,返回**表达式结果对应的类型**
  ```cpp
int i = 2,*p = &i,&r = i;
decltype(r) a = i;//int &a = i;
decltype(r+0) a;//表达式r+0结果时int,所以int a;
```
- 当参数为**表达式,且为赋值语句的左值**,**返回的类型是引用**,`*p`解引用表达式.**为赋值语句的左值:指针指向的对象能被赋值改变,变量作为表达式时也是左值,因为也能被复制改变**
  ```nix
int a=1,*p = &a;
int b=2;
decltype(*p) c=b; // int &c = b;
decltype((a)) d=b;-> decltype((a=1)) d=b;-> int &d = b;
```

1. 给变量加1或多层括号编译时把它作为表达式  
   结论: `decltype((variable))`一般结果都是返回**引用**.
