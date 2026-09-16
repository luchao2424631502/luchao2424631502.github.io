---
title: VsStudio制作静态库-mutable-explicit等用法
date: '2021-01-06 17:26:00'
permalink: 2021/01/06/VsStudio制作静态库-mutable-explicit等用法/
categories:
- 编程语言
- C与C++
tags:
- mutable,explicit
---

#### mutable关键字

2. **class中的常函数**,当函数中不需要修改类中的变量时将函数声明为 `const` 函数,**配合const&对象使用**,(const的位置和override出现的位置相同,说明这个地方是修改函数属性的),

   **如果要在class的const函数中修改类中变量,则将成员变量声明为mutable**

   ```cpp
#include <iostream>
#include <string>
#include <array>
#include "../src/include/local.h"

#include <stdlib.h>

class Entity
{
private:
	int m_X, m_Y;
	mutable int var; //mutable:可变的,表示即使在常方法中也可以修改此可变的变量,可变:允许在常函数中允许变量被修改
public:
	int GetX() const
	{
		var = 2;
		return m_X;
	}
	int GetX()
	{
		return m_X;
	}

	void SetX(int x)
	{
		m_X = x;
	}
};

void PrintEntity(const Entity& e)
{
	std::cout << e.GetX() << std::endl;
}

int main()
{
	const int MAX_AGE = 80;
	int const*const  a = new int;

	std::cout << *a << std::endl;

	std::cin.get();
}
```
3. 可变lambda函数

   值捕获的变量不能在非可变lambda中修改,**即:只能在可变lambda中修改值捕获的变量**

   ```cpp
int x = 8;
auto f = [=]() 
{
	x++;
	std::cout << x << std::endl;
};
f();
std::cout << x << std::endl;
```

---

#### 类的构造函数中初始化成员变量尽量使用初始化列表,避免在构造函数体内部初始化成员变量

---

### new运算符的不同用法

operator new 和 placement new

### explicit关键字声明类的构造函数，禁止类的隐式类型转化

```
implicit (含蓄的) 隐式类型转换 explicit (明确的) 显式构造函数,**只要有对应的构造函数,默认是implicit的,即可以进行隐式类型转换,除非将构造函数声明为explicit,显式的构造函数**
```

### 重载运算符的写法

> 1. 重载运算符operator的写法**和写class中的成员函数是一样的**,
>
>    注意:
>
> 1. 在类中重载运算符的函数参数只有一个是因为重载的是2元运算符,且第一个参数是this指针
> 2. 如上,当我们重载全局运算符的时候**千万不要向重载class的2元运算符一样只写一个参数**
>
>    如果重载了+ - & /运算符,**最好有对应的名字的成员函数来表达运算符的意思**

### 拷贝构造函数

> 应为类中有指针,重写拷贝构造函数解决浅拷贝和深拷贝问题

```cpp
String abc;
/*调用拷贝构造函数例子*/
String string = abc;
String string1(abc);

/*定义自己的拷贝构造函数*/
class String
{
  public:
    String() = default;
    String(const String& other)
};
```

### std::vector

1. 注意容器大小的变化

   `std::vector<int> vec;`在stack上分配的容器大小是1,当push\_back时,**容器会申请新的内存空间, 并且将原来所有的元素都复制 (模板是类则调用类的拷贝构造函数) 过去**,

   > 在push\_back()前使用`reserve()`函数申请容器的内存空间,**减少扩容时,元素的多次拷贝构造**

   2. 添加元素时调用`emplace_back()`,**此函数直接在容器的内存上使用参数构造元素(类),而`push_back()`则是先构造临时对象,然后在容器内存上调用拷贝构造函数.**```cpp
#include <iostream>
#include <string>
#include <array>
//#include "../src/include/local.h"
#include <stdlib.h>
#include <memory>
#include <vector>

struct Vertex
{
public:
	Vertex() = default;

	Vertex(float x, float y, float z)
		:x(x), y(y), z(z)
	{
		std::cout << "x,y,z构造函数"<< std::endl;
	}
	Vertex(const Vertex& other)
		:x(other.x), y(other.y), z(other.z)
	{
		std::cout << "拷贝构造函数" << std::endl;
	}
	//~Vertex()
	//{
	//	std::cout << "~析构函数" << std::endl;
	//}
public:
	float x, y, z;
};

std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
	stream << vertex.x << ", " << vertex.y << ", " << vertex.z;
	return stream;
}

void Function(const std::vector<Vertex>& v)
{
}

int main()
{	
	std::vector<Vertex> vertices;
	vertices.reserve(3);

	//vertices.push_back({1,2,3});
	//vertices.push_back({4,5,6});
	//vertices.push_back({7,8,9});

	vertices.emplace_back(1,2,3);
	vertices.emplace_back(1,2,3);
	vertices.emplace_back(3,4,5);

	std::cin.get();
}
```

---

### Visual Studio中c++项目添加静态库

> 首先下载需要使用的库,然后配置include目录和静态库or动态库目录,+具体库文件名
>
> 这里以glfw c库[下载](https://www.glfw.org/download.html)来举例
>
> 将下载的文件夹目录下的include/目录和所需要的版本的lib/目录复制到项目所在目录(可自己在项目中添加新的目录)

1. 下载windows预编译二进制文件(库文件)

   > 根据自己项目是win32还是x64对应下载
2. 添加头文件所在目录: 在项目->属性->c/c++->**附加包含目录中**,添加**头文件所在目录**
3. 添加库文件所在目录: 在项目->属性->链接器(`Linker`)->常规,添加**附加库目录(库文件的路径)**
4. 添加依赖的具体库文件: 项目->属性->链接器(`Linker`)->输入->附加依赖项,添加静态库文件`.lib`

---

### 动态库

DLL有2种调用方法

1. 隐式调用
2. 显示调用

---

### 同一解决方案下添加另一个项目(编译成静态库)链接到原项目

1. 新建空c++项目(假设叫做Test),(解决方案和项目不在同一目录中)
2. 在解决方案中添加新项目(空的c++项目),假设叫Static
3. Static编译成lib,修改项目属性->常规属性->配置类型,选择.lib
4. Test要使用Static编译出的.lib,**引用头文件和上面一样**,
5. 引用lib文件可以不需要再次添加lib目录和依赖的lib文件名,**Test项目右键点击添加->引用->同意解决方案下的Static->确定**
6. 编译Test,测试链接成功
