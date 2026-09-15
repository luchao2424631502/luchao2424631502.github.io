---
title: template和namespace简单使用
date: '2021-01-06 17:18:00'
permalink: 2021/01/06/template和namespace简单使用/
categories:
- C++primer读书笔记
tags:
- c++
---

### template

> <>中 既可以传递类型,也可以传递值

1. 模板函数

   1)推断类型

   ```cpp
template<typename T>
void Print(const T& value)
{
	std::cout << value << std::endl;
}

int main()
{		
	Print<std::string>("abc");
	Print(1.1f);
	Print(23);
	

	//std::cin.get();
}
```

   2)推断值

   ```cpp
template<int N>
unsigned int func()
{
	return N;
}

int main()
{
    std::cout << func<10>() << std::endl;
    std::cin.get();
}
```

2. 模板类

   1)推断类型

   ```cpp
template<typename T>
class Temp
{
private:
	T m_Value;
public:
	Temp() = default;
};
```

   2)推断值

   ```cpp
template<int N>
class Temp
{
private:
	int m_Value[N];
public:
	Temp() = default;

	unsigned int GetSize() const { return N; }
};

int main()
{
	Temp<10> temp;
	std::cout << temp.GetSize() << std::endl;;
	std::cin.get();
}
```

   3)既推断类型又推断值,像`std::array`一样

   ```cpp
template<typename T,int N>
class Array
{
private:
	T value[N];
public:
	Array() = default;
	unsigned int GetSize()const { return N; }
};

int main()
{
    Array<double, 20>* ptr = new Array<double, 20>;
	std::cout << ptr->GetSize() << std::endl;
    delete ptr;
    std::cin.get();
}
```

---

### namespace

> 尽量不要再大的作用域范围内使用`using namespace xxx;`,避免函数调用不清晰,最多在函数内使用.
>
> 最好这样`std::cout << " " << std::endl;`

1. 命名空间 名字 代替

   ```cpp
namespace T = std;
```
2. 命名空间嵌套

   ```cpp
namespace A
{
	namespace B
	{
		namespace C
		{
			void Fabc()
			{
				using namespace std;
				cout << "abc" << endl;
			}
		}
	}
}

int main()
{
    A::B::C::Fabc();
	std::cin.get();
}
```
3. 多个编译单元中使用

   > 如何使用其他编译单元中的命名空间,
   >
   > 在头文件中使用**相同的命名空间来声明**

   –main.cpp

   –local.h

   –local.cpp

   ```cpp
//main.cpp
#include "../src/include/local.h"

void f1(int)
{
}

int main()
{
	namespace F = T;
	F::apple::orange::print("abc");
	using Func = T::apple::Func;
	Func ptr = f1;
	using T::apple::print;
	print("abc");
	T::apple::print("Hello");
	T::apple::orange::print("Hello");
	std::cin.get();
}
```

   ---

   ```cpp
//local.h
#include <iostream>
#include <string>
#include <array>
#include <stdlib.h>
#include <memory>
#include <vector>
//#include "GLFW/glfw3.h"
//#include "GLFW/glfw3native.h"
//#include <utility>
#include <functional>
#include <unordered_map>
#define ps(str) std::cout << str<<std::endl

namespace T
{
	namespace STD = std;
	void func();
	namespace apple 
	{
		typedef void(*Func)(int);
		void print(const char*);
		namespace orange 
		{
			void print(const char*);
		}
	}
}
```

   ---

   ```cpp
//local.cpp
#include <iostream>

namespace T
{
	namespace apple
	{
		namespace orange
		{
			void print(const char* text)
			{
				std::string temp = text;
				std::reverse(temp.begin(), temp.end());
				std::cout << temp << std::endl;
			}
		}
		void print(const char* text)
		{
			std::cout << text << std::endl;
		}
	}
	void func()
	{
		std::cout << "func" << std::endl;
	}
}
```

> 和不同的声明方法一样,只是注意加上命名空间的作用于就行了
