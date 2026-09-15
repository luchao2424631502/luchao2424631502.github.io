---
title: allocator 类的使用方法
date: '2019-09-01 20:42:00'
permalink: 2019/09/01/csdn/allocator 类的使用方法/
categories:
- C++primer读书笔记
tags:
- allocator
---

`new`分配内存并且构造对象  
`delete`释放内存并且析构对象

### 注意`delete`删除指向动态数组的指针

```arduino
 1 #include <iostream>
 2 #include <cstring>
 3 
 4 using namespace std;
 5 
 6 int main() {
 7     char *r = new char[20];                                                      
 8     int cnt = 0; char temp;
 9     while (cin.get(temp)) {
10         if (isspace(temp))
11             break;
12         r[cnt++] = temp;
13         if (cnt == 19)
14             break; 
15     }   
16     r[cnt] = 0;
17     cout << r << endl;
18     delete [] r; 
19     return 0; 
20 }
```

### allocator类将内存分配和对象构造分开了

- 一定记住分配内存和构造对象是分开的

1. `<>`指明分配对象的类型   
    定义一个`allocator`对象`allocator<string> alloc`

- 根据对象类型来确定内存大小和对齐位置

#### 成员函数

1. `auto p = alloc.allocate(n)`:分配一段未构造的内存来保存n个`string`对象
2. `alloc.deallocate(p,n)`,释放内存,且要指出**创建时要求的大小**,**并且释放之前一定要析构对象**
3. `alloc.construct(p,"nihao")`:用`"nihao"`构造`p`指向的内存的对象
4. `alloc.destroy(p)`:析构`p`指向的对象

```arduino
 1 #include <iostream>
 2 #include <memory>
 3 #include <vector>
 4 #include <string>
 5 
 6 #include <string.h>
 7 #include <fstream>
 8 
 9 using namespace std;
10 int main() {
11     ifstream in("1.out");
12     if (!in) cout << " wrong to open file \n";
13     allocator<string> alloc;
14     auto const p = alloc.allocate(100);
15     string s;
16     string *q = p;
17 
18     while (in >> s && q != p+100)
19         alloc.construct(q++,s);
20     const size_t size = q-p;
21     for (size_t i=0; i<size; i++) {
22         cout << p[i] << " " << endl;
23     }
24 
25     while (q != p)
26         alloc.destroy(--q);
27     // free memory
28     alloc.deallocate(p,100);
29     in.close();
30     return 0;
31 }
```

### 拷贝和填充未初始化内存的算法

- `allocator`类的伴随算法,定义在`memory`库中

1. `uninitialized_copy(b,e,p)`,将迭代器b到e之间的元素拷贝到p指定的未构造的原始内存中
2. `uninitialized_copy_n(b,n,p)`,从迭代器b开始,拷贝n个元素到p指定的未构造的原始内存中
3. `uninitialized_fill(b,e,t)`,在迭代器b到e之间创建对象,t的拷贝
4. `uninitialized_fill_n(b,n,t)`,从迭代器b开始创建n个对象,每个对象都是t的拷贝

```arduino
 1 #include <iostream>
 2 #include <memory>
 3 #include <vector>
 4 
 6 using namespace std;
 7 
 8 int main() {
 9     vector<int> v(10,1);
10     allocator<int> alloc;
11     auto p = alloc.allocate(v.size() * 2);
12     auto q = uninitialized_copy(v.begin(),v.end(),p);
13 
14     uninitialized_fill_n(q,v.size(),9999);
15 
16     q = q + 10;
17     int cnt = 0;
18     while (p != q) {
19         cnt++;
20         alloc.destroy(--q);
21         cout << *q << endl;
22     }                                                                            
23     cout << cnt << endl;
24     return 0;
25 }
```
