---
title: const int* 和 const int * const 和 int const * 的区别
date: '2019-12-18 19:31:00'
permalink: 2019/12/18/csdn/const int! 和 const int ! const 和 int const ! 的区别/
categories:
- C++primer读书笔记
tags:
- const pointer
---

# `const int*`和`const int * const`和 `int const *`的区别

[原文地址](https://www.geeksforgeeks.org/difference-between-const-int-const-int-const-and-int-const/)

---

### `int const *`是一个指向常量整数的指针

- **指向了一个不能被修改的值但是指针指向的地址可以改变**
- `const` 在数据类型的一侧,所以可以放在`int`的前面`const int *`,(从`c++ prime`了解到)

```c
#include <stdio.h>

int main() {
    const int q = 5;
    int const *p = &q;
    // 等价于
    const int *p1 = &q;
    
    const int q2 = 7;
    p = &q2;
    return 0;
}
```

### `int * const`是一个指向整数的常量指针

- **指针指向的地址不能被改变,但是地址中的值可以被改变**

```c
#include <stdio.h>

int main() {
    const int q = 5;
    int q1 = 5;
    // 错误写法 指向int 而非const int 整形常量
    /*int *const p = &q;*/
    int *const p = &q1;
    *p = 11;

    int q2 = 1;
    // 只读变量p ,p指向的地址不能改变
    //p = &q2;
    return 0;
}
```

### `const int * const`是一个指向常量整数的常量指针

- 第一个`const`可以位于数据类型的任意一侧,所以等效写法`int const * const`
- **此指针既不能指向新地址,也不能修改指向的值**

```c
#include <stdio.h>

int main() {
    const int q = 5;
    int const * const p = &q;
    // assignment of read-only location ‘*p’
    *p = 10;
    const int q2 = 10;
    // assignment of read-only variable ‘p’
    p = &q2;
    return 0;
}
```
> 这2句报错也能很好的告诉我们
>
> 只读变量
>
> 只读位置

---

### 螺旋规则解释语法

- 从变量名开始，然后顺时针移动到下一个指针或类型。重复直到表达式结束 (原文中的图)

`int const * const var`: 变量是-> const -> 是指针 (`const pointer`)->指向`const`->int (`const int` 指向常量值)

- 可看做从右到左

### 因此

- `int const *` 指针指向常量`int`
- `int * const`常量指针指向`int`
- `int const * const`常量指针指向常量`int`

---

- `int ** const`**常量指针**指向**一个指针**且该指针指向一个`int`
- `int * const *`**指针** 指向 一个**常量指针**且该指针指向`int`
- `int const **`:**指针** 指向一个**指针**且该指针指向常量`int`, 看做`const int **`更好理解
- `int * const * const`**常量指针**指向**一个常量指针**且该指针指向`int`

---

> 暂时忽略`c++`中的顶层`const`和底层`const`
>
> 没有记错的话: `c`标准中`const`是从`c++`标准中引入的…….

---

### 由于`c++`引用原因,`int &a = b;`,导致我经常`int* p;`这样声明指针

- 这种声明很容易导致混淆 `int* p,q;`:

> 长时间写`c++`，会习惯性理解成声明了2个指针
>
> 但实际上是
>
> - `p`是指针
> - `q`是`int`
>
> 尽管这种写法是正确的,
>
> 一般都这样写`int *p,q;`,不容易导致混淆

- 上面的写法属于习惯问题,编译器并不会报错

---

[关于int \*p 和 int\* p的讨论](https://stackoverflow.com/questions/5590150/difference-between-int-p-and-int-p-declaration)
