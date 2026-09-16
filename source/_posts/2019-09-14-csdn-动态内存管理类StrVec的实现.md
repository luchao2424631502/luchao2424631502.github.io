---
title: 动态内存管理类StrVec的实现
date: '2019-09-14 18:32:00'
permalink: 2019/09/14/csdn/动态内存管理类StrVec的实现/
categories:
- 编程语言
- C与C++
---

### 实现一个动态内存管理类

1. `StrBlob`中`vector<string>`可以管理元素的内存.
2. 实现一个`vector<string>`

#### `allocator<>`类是分配的原始内存,当调用`alloc.destroy(first_free)`,

- 按道理来说`destroy`执行对象的析构函数,`string`的**析构函数执行完后会回收内存**,再访问该`string`就访问越界了
- **但是如果在`destroy()`后访问`string`指针的内容,仍可以读取到,我觉得原因在于内存是由`allocator`类申请来的的,由`alloc`对象管理,即使`string`对象执行完析构函数.内存也不会回收**

### `alloc_n_copy`非常巧妙

- 在原`alloc`对象申请原始内存,通过`uninitialized_copy()`来初始化
- 支持`vector<>`的部分初始化

---

`StrVec.h`

```typescript
#ifndef STRVEC_H
#define STRVEC_H

#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <initializer_list>
#include <algorithm>


class StrVec {
public:
    StrVec():elements(nullptr),first_free(nullptr),cap(nullptr) {}
    StrVec(std::initializer_list<std::string> i1);
    StrVec(const StrVec&);
    StrVec& operator=(const StrVec&);
    ~StrVec();
    StrVec(size_t);
    StrVec(size_t,const std::string&);

    void resize(size_t,const std::string&);
    void resize(size_t);
    void reserve(size_t);
    void push_back(std::string&);
    void push_back(std::string);
    std::string pop_back();
    size_t size() const { return first_free - elements; }
    size_t capacity() const { return cap - elements; }
    std::string* begin() const { return elements; }
    std::string* end() const { return first_free; }

private:
    static std::allocator<std::string> alloc;

    void chk_n_alloc();
    void free();
    void reallocate();
    void reallocate(size_t);
    std::pair<std::string*,std::string*>
        alloc_n_copy(const std::string*,const std::string*);

    void alloc_n_copy(size_t,const std::string&);

    std::string* elements;
    std::string* first_free;
    std::string* cap;
};
void StrVec::free() {
   /* if (elements)*/
        //for (auto it = first_free; it != elements;)
            /*alloc.destroy(--it);*/
    if (elements)
        std::for_each(elements,first_free,
            [](std::string& s){ alloc.destroy(&s);});
    alloc.deallocate(elements,cap - elements);
    std::cout << " ~StrVec() " << std::endl;
}
void StrVec::reallocate() {
    auto newcapacity = size() ? 2*size() : 1;
    auto newdata = alloc.allocate(newcapacity);

    auto dest = newdata;
    auto elem = elements;
    for (size_t i=0; i!=size(); ++i)
        alloc.construct(dest++,std::move(*elem++));
    free();

    elements = newdata;
    first_free = dest;
    cap = elements + newcapacity;
}

void StrVec::reallocate(size_t newcapacity) {
    auto newdata = alloc.allocate(newcapacity);

    auto dest = newdata;
    auto elem = elements;
    for (size_t i=0; i!=size(); ++i)
        alloc.construct(dest++,std::move(*elem++));
    free();

    elements = newdata;
    first_free = dest;
    cap = elements + newcapacity;
}

void StrVec::reserve(size_t n) {
    if (n > capacity()) reallocate(n);
}
void StrVec::resize(size_t n) {
    if (n > size()) {
        while (size() < n)
            push_back("");
    } else if (n < size()) {
        while (size() > n)
            alloc.destroy(--first_free);
    }
}
void StrVec::resize(size_t n,const std::string& s) {
    if (n > size()) {
        while (size() < n)
            push_back(s);
    }
}

void StrVec::chk_n_alloc() {
    if (size() == capacity())
        reallocate();
}
void StrVec::push_back(std::string& s) {
    chk_n_alloc();
    alloc.construct(first_free++,s);
}

void StrVec::push_back(std::string s) {
    chk_n_alloc();
    alloc.construct(first_free++,s);
}

std::pair<std::string*,std::string*>
StrVec::alloc_n_copy(const std::string* b,const std::string* c) {
    auto data = alloc.allocate(c-b);
    return {data,uninitialized_copy(b,c,data)};
}

StrVec::StrVec(const StrVec& rhs) {
    auto newdata = alloc_n_copy(rhs.begin(),rhs.end());
    elements = newdata.first;
    cap = first_free = newdata.second;
}

void StrVec::alloc_n_copy(size_t n,const std::string& s) {
    auto newdata = alloc.allocate(n);
    auto dest = newdata;
    for (auto i=0; i<n; ++i)
        alloc.construct(dest++,s);
    elements = newdata;
    first_free = dest;
    cap = elements + n;

}
StrVec::StrVec(size_t n) {
    alloc_n_copy(n,"");
}

StrVec::StrVec(size_t n,const std::string& s) {
    alloc_n_copy(n,s);
}

StrVec::~StrVec() { free(); }

StrVec& StrVec::operator=(const StrVec& rhs) {
    auto data = alloc_n_copy(rhs.begin(),rhs.end());
    free();
    elements = data.first;
    cap = first_free = data.second;
    return *this;
}
StrVec::StrVec(std::initializer_list<std::string> i1) {
    auto newdata = alloc_n_copy(i1.begin(),i1.end());
    elements = newdata.first;
    cap = first_free = newdata.second;
}
std::string StrVec::pop_back() {
    if (size()>=1) {
        std::string temp = *(--first_free);
        alloc.destroy(first_free);
        return temp;
    }
}
#endif
```

### `StrVec`类的使用

`main.cpp`

```cpp
#include <iostream>
#include "StrVec.h"
#include <string>

std::allocator<std::string> StrVec::alloc;

int main() {
    std::string test(" test string ");
    StrVec temp1(10,test);
    StrVec temp2 = {"a","ab","abc","abcd"};
    StrVec temp3(2);
    StrVec temp4 = temp2;
    for (auto i:temp1)
        std::cout << " i " << i << std::endl;
    for (auto i:temp2)
        std::cout << " i " << i << std::endl;
    return 0;
}
```
