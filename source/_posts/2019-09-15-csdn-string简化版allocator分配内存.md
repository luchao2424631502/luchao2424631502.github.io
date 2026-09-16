---
title: string简化版allocator分配内存
date: '2019-09-15 13:55:00'
permalink: 2019/09/15/csdn/string简化版allocator分配内存/
categories:
- 编程语言
- C与C++
---

## 通过allocator类来分配内存实现简化版string

### 功能:

- `String(const char*)`和`String(const std::string)`接受隐式类型转换
- 重载`string`的多种运算符:`[]`,`+`,`+=`,`<<`,`>>`
- 实现`string`多个成员函数`size()`,等
- 构造函数和析构函数对原始内存的分配和释放,

### 内存分配问题

1. `allocator<>`类分配的是原始内存,结合`construct()`来构造对象(此处是`char`内置类型)
2. `for_each()`+`lambda`实现对象的`destroy`

   ### 拷贝控制操作
3. `String(const String&)` 拷贝构造函数
4. `String& operator=(const String&)`拷贝复制运算符vim
5. `reallocate()`中通过`std::move()`返回右值引用.

### 细节

1. 通过下标`[]`访问返回`char&`,赋值给`char*`或者`char&`都能修改`String`的单个字符(未定义成`const`)

- 在`.h`文件中声明了`char _temp_arr[size]`全局变量,即使重载`+`返回`char*`(使得不必声明`const char*`变量来接收),但它隐式的为`const char*`,原因如下:

  ### 关于c++ 字符串常量
- 字符串常量`c++`标准看做为一个`const char*`的地址,存储在静态内存区(但它并不是静态变量,只是行为上相似,字符串常量很少需要被修改,放在静态内存区提高效率),它是常量.

1. `char* p = "example"`

- `g++编译时的警告`:  
  `warning: ISO C++ forbids converting a string constant to ‘char*’ [-Wwrite-strings] char* p = "test" ;`
- `c`程序可以这样声明
- 字符串常量**是无法被修改的**.

`String.h`

```cpp
#ifndef STRING_H
#define STRING_H

#include <memory>
#include <string>
#include <cstring>
#include <algorithm>
#include <iostream>
const int size = 1000;
char _temp_arr[size];

class String {
    friend std::ostream& operator << (std::ostream&,const String&);
    friend std::istream& operator >> (std::istream&,String&);

    friend String& operator += (String& lhs,const String& rhs);
    friend char* operator + (String& lhs,String& rhs);

public:
    String():_begin(nullptr),_first_free(nullptr),_end(nullptr) {}
    String(const char*);
    String(const std::string&);
    String& operator= (const String&);
    ~String();

    char& operator[](const size_t&); //返回的char& 在内存未被回收的情况下可以通过[]改变
    const char* c_str() const { return _begin; }
    size_t size() const { return _first_free-_begin; }
    bool empty() const { return _first_free-_begin?0:1; }
    char* begin() const { return _begin; }
    char* end() const { return _end; }
    size_t capacity() const { return _end-_begin; }
    size_t remain() const { return _end-_first_free; }

private:
    static std::allocator<char> alloc;
    void free();
    void reallocate();
    std::pair<char*,char*>
        alloc_n_copy(const char*,const char*);

    char* _begin;
    char* _first_free;
    char* _end;
};
std::ostream& operator<<(std::ostream& out,const String& rhs) {
    out << rhs._begin;
    return out;
}
std::istream& operator>>(std::istream& in,String& rhs) {
    char p[size];
    in >> p;
    rhs = p;
    return in;
}

String& operator+=(String& lhs,const String& rhs) {
    if (lhs.remain() > rhs.size()) {
        auto dest = rhs._begin;
        for (size_t i=0; i<rhs.size(); ++i)
            lhs.alloc.construct(lhs._first_free++,*dest++);
    } else {
        lhs.reallocate();
        auto dest = rhs._begin;
        for (size_t i=0; i<rhs.size(); ++i)
            lhs.alloc.construct(lhs._first_free++,*dest++);
    }
    return lhs;
}

char* operator+(String& lhs,String& rhs) {
    strcpy(_temp_arr,lhs._begin);
    auto temp_ptr = _temp_arr + strlen(_temp_arr);
    strcpy(temp_ptr,rhs._begin);
    return _temp_arr;
}

char& String::operator[](const size_t& index) {
    if (index < size())
        return *(_begin + index);
}

std::pair<char*,char*>
String::alloc_n_copy(const char* b,const char* c) {
    auto newdata = alloc.allocate(c-b);
    return {newdata,std::uninitialized_copy(b,c,newdata)};
}
String::String(const char* p) {
    int len = strlen(p);
    auto newdata = alloc_n_copy(p,p+len);
    _begin = newdata.first;
    _end = _first_free = newdata.second;
}
String::String(const std::string& s) {
    int len = s.size();
    auto newdata = alloc_n_copy(&s[0],&s[len]);
    _begin = newdata.first;
    _end = _first_free = newdata.second;
}
void String::free() {
    std::for_each(_begin,_end,
            [](char& p){ alloc.destroy(&p); });
    alloc.deallocate(_begin,_end-_begin);
}
String::~String() { free(); }

String& String::operator= (const String& rhs) {
    auto newdata = alloc_n_copy(rhs.begin(),rhs.end());
    free();
    _begin = newdata.first;
    _end = _first_free = newdata.second;
    return *this;
}
void String::reallocate() {
    auto newcapacity = size() ? 2*size() : 1;
    auto newdata = alloc.allocate(newcapacity);

    auto dest = newdata;
    auto elem = _begin;
    for (size_t i=0; i<size(); ++i)
        alloc.construct(dest++,std::move(*elem++));
    free();
    _begin = newdata;
    _first_free = dest;
    _end = _begin + newcapacity;
}
#endif
```

`test.cpp`

```cpp
#include <iostream>
#include "String.h"
std::allocator<char> String::alloc;
int main() {
    String temp1("emerald |");
    String temp2 = "is a boy";
    String temp3 = temp2 + temp1;

    std::cout << "temp3=" << temp3 << std::endl;
    temp3 = " new string X";
    std::cout << "temp3=" << temp3 << std::endl;

    char* p = temp2 + temp1;
    std::cout << "p=" << p << std::endl;

    std::cout << "[]=" << temp2[2] << "|" << std::endl;
    char* pp = &temp2[3];
    *pp = 'X';
    std::cout << "*pp=" << *pp << std::endl;
    std::cout << "temp2=" << temp2 << std::endl;
    return 0;
}
```
