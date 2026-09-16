---
title: const限定符解析
date: '2019-07-17 20:35:00'
permalink: 2019/07/17/csdn/const限定符解析/
categories:
- 编程语言
- C与C++
tags:
- const
---

- `const`
  > 1. `const`对象一旦创建后就不能再改变,所以`const`对象必须初始化
  >    ```vala
const int i = get_size(); //运行时初始化
const int j = 10; // 编译时初始化
```
  > 2. 编译器在编译过程将该变量都替换成常量
  > 3. `const`引用,
  >    > 允许常量引用
  >
  >    ````stata
const int ci = 10;
const int &r1 = ci; 
r1 = 42; //无法通过对常量的引用修改其对象
int &r2 = ci; // 非常量引用无法指向常量引用
``` 
> 非常量引用不能指向常量对象  <br><br>
> 常量引用 可以 绑定**非常量的对象**
````
  >    int i = 42; // 1.  
  >    const int &r1 = i; // 2.允许用非常量来初始化  
  >    const int &r2 = 10; //常量初始化  
  >    const int &r2 = r1 \* 2; //常量初始化
  >    ```plain
第1行和2行编译器转化为
```
  >    const int i = 42;  
  >    const int &r1 = i;
  >    ```asciidoc
同理,常量引用绑定**不同类型的非常量**,编译器创建了一个临时量.
```
  >    double i = 10; // 编译器转化为 const int temp = i;  
  >    const int &r1 = i; // 转化为 const int &r1 = temp;
  >    ```markdown
--- 
* 当`ri`是**非常量引用**,`int &ri = i;`,此时`ri`绑定的对象是**编译器产生的临时量**,相当于`int &ri = temp`.此时引用只能改变`temp`的值,而改变不了`i`的值.
* 所以 **引用类型必须与引用对象的类型一致**
### **常量指针**和**指向常量的指针**
1. 指向常量的指针
* 想要存放**常量**的地址.只能使用**指向常量的指针**
```
  >    const double pi = 3.14; // double型常量  
  >    double \*ptr = π //普通指针无法存常量地址  
  >    const double \*cptr = π //合法
  >
  > \*cptr = 42; //只能初始化,不能赋值
  >
  > ```asciidoc
* 可以给该指针赋值一个**非常量**,**和上面的引用绑定非常量对象一样**
```
  >
  > double dval = 3.14;  
  > cptr = &dval //赋值
  >
  > ```markdown
2. 常量指针
* 指针本身定义为常量,**必须初始化**(常量必须初始化),
* 指针本身是常量意味着**存放的地址不能够被改变**,而不是指向对象不能被改变
```
  >
  > int errNumb = 0;  
  > int\* const curErr = &errNumb //初始化  
  > const double pi = 3.14;  
  > const double\* const pip = pi; // pip是指向常量的常量指针

  ```markdown
* 指向常量的常量指针意味着**不仅指针存放的地址不能够被改变,而且指向的对象是常量,也不能够被改变**
* 如果分不清符号声明,**从右往左读,const离curErr近说明curErr本身是个常量对象**
#### 顶层const
1. 顶层`const`:指针本身是一个常量.
2. 底层`const`:指针所指向的对象是一个常量
```
  int i=0;  
  int *const p1 = &i //顶层const  
  const int ci = 42; //顶层const  
  const int* p2 = &ci //底层const  
  const int\* const p3 = p2; //  
  const int &r = ci; //底层const
  ```asciidoc
* 执行拷贝操作2个对象都必须具有相同**底层`const`** 资格
```
  int \*p = p3; //常量不能转化成非常量  
  p2 = p3; //都有底层const  
  p2 = &i // 非常量可以辅助给常量  
  const int &r2 = i; //非常量转化成常量
