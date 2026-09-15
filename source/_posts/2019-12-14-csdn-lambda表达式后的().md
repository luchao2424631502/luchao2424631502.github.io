---
title: lambda表达式后的()
date: '2019-12-14 19:02:00'
permalink: 2019/12/14/csdn/lambda表达式后的()/
categories:
- C++primer读书笔记
tags:
- lambda
---

- 一直对lambda后面的`()`这种离奇的语法感到奇怪,今天看到如下代码:

```c
auto optimize_cpp_stdio = []() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);
    std::setvbuf(stdout, nullptr, _IOFBF, BUFSIZ);
    return 0;
}();
```

---

- 沙雕的以为是声明函数对象?
- 但是`optimize_cpp_stdio`接收的是函数调用后的返回值而已

---

#### 没有()是定义函数对象

> ```c
// 定义了一个函数对象
auto func = [](){ std::cout << "test" << std::endl; };
func(); //然后调用该函数对象
```

### c++11 中

> C++11允许lambda函数根据return语句的表达式类型推断返回类型。C++14为一般的函数也提供了这个能力。

- 返回类型若缺失，则由函数的 return 语句所蕴含（**或当函数不返回任何值时为 void**）

#### lambda后有() 等价于 直接调用函数对象并且返回值,

- 如果`lambda`函数没有`return` 这个表达式,那么不能用变量接收函数返回结果

1. 返回`void`直接调用`lambda`

   ```c
[](){
        std::cout << "test" << std::endl;
    }();
```

   **函数不返回任何值时为 void**，当然不能用`auto`变量去推导返回类型

   错误写法:

   ```c
auto ans = [](){
 	std::cout << "test" << std::endl;
}();
```
2. **离奇写法(正确)**,声明`lambda`且调用,

   ```c
auto optimize_cpp_stdio = []() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);
    std::setvbuf(stdout, nullptr, _IOFBF, BUFSIZ);
    return 0;
}();
```
3. 一般用法

   ```c
auto func = [](){
        std::cout << "test" << std::endl;
    };
func();
```

---

#### 这种写法`[](){}();`确实让人挺窒息的,但是要清楚`()`无非就是 函数调用 而已,
