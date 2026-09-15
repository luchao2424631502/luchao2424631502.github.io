---
title: tuple_variant_any_string_view_Singleton使用
date: '2021-01-11 11:48:00'
permalink: 2021/01/11/tuple-variant-any-string-view-Singleton使用/
categories:
- C++primer读书笔记
tags:
- c++17
---

### Virutal 析构函数

99%的类的析构函数都要声明成virtual,因为要继承给子类,然后子类能正确释放自己的资源

```cpp
class Base
{
public:
	Base() {
	
		std::cout << "Base ConStructor\n";
	}
	 ~Base()
	{
		std::cout << "Base Destructor\n";
	}
};

class Derived :public Base
{
public:
	Derived() :m_Array(new int[5]{1,2,3,4,5}) { std::cout << "Derived Constructor\n"; }
	~Derived()  { delete[] m_Array; std::cout << "Derived Destructor\n"; }
	int* GetPtr()  { return m_Array; }
private:
	int *m_Array;
};

int main()
{
	Base* base = new Base();
	delete base;
	std::cout << "---------------" << std::endl;
	Derived* derived = new Derived();
	delete derived;
	std::cout << "---------------" << std::endl;
	Base* ploy = new Derived();/*多态,基类指针指向的元素没有子类的析构函数,
							   有构造函数出现是因为调用new.*/
	int* ptr =((Derived*)ploy)->GetPtr();
	delete ploy;

	std::cin.get();
}
```

### 结构化绑定,接收std::tuple<>的语法糖

> c++17

```cpp
std::tuple<std::string,int> CreatePerson()
{
	return {"abc",10};
}

struct res
{
	std::string name;
	int age;
};

int main()
{
	auto person = CreatePerson(); //返回的临时的tuple构造了auto,而上面的参数是临时变量,右值,
	const std::string& name = std::get<0>(person);
	int age = std::get < 1>(person);

	/*例子*/
	auto [name,age] = CreatePerson();
	std::cout << name << " " << age << std::endl;

	std::cin.get();
}
```

### std::optional<>,对返回空值进行包装

根据函数返回值进行判断是否执行成功,使用`std::optional<>`来包装

```cpp
#include "../src/include/local.h"

std::optional<std::string> ReadFileAsString(const std::string& filepath)
{
	std::ifstream stream(filepath);
	if (stream)
	{
		std::string result;
		stream.close();
		return result;
	}

	return {};
}

int main()
{
	std::optional<std::string> data = ReadFileAsString("data.txt");
	if (data.has_value())
	{
		std::cout << "File read successfully!\n";
	}
	else 
	{
		std::string& string = *data;
		std::cout << "File couldn't open";
	}

	std::optional<int> count;
	int c = count.value_or(100);
	int c1 = *count;
	std::cout << c << "\n" << c1;

	std::cin.get();
}
```

### std::variant<>多类型的数据存放在单一变量

但是同时只能存储一个类型的变量,注意和`std::tuple<>`的区别,

大小等于所有类型之和,可使用在函数返回

```cpp
enum class ErrorCode
{
	None = 0,
	NotFound = 1,
	NotAccess = 2
};

std::variant<std::string, ErrorCode> ReadFileAsString(std::string pathfile)
{
	return ErrorCode::NotAccess;
}

int main()
{
	std::variant<std::string, ErrorCode> res = ReadFileAsString("data.txt");
	int index = res.index();
	if (index == 0)
		std::cout << std::get<0>(res);
	else
		std::cout << (int)std::get<1>(res);

	std::cout << (int)std::get<ErrorCode>(res);
	std::cin.get();
}
```

### std::any 单个变量存储任意类型数据

**注意是非模板类**,可以存储任意类型的变量

```cpp
#include "../src/include/local.h"
#define ps(str) std::cout << str << std::endl

std::any Func()
{
	return 1;
}

enum class ErrorCode
{
	None = 1,
	Access = 2,
	NotFound = 3
};

int main()
{
	std::any data;
	data = 2;
	data = std::string("Abc"); //std::string
	data = "das"; //const char*;
	data = ErrorCode::Access;
	data = 1.0f;

	std::string& string = std::any_cast<std::string&>(data);

	auto res = Func();
	if (res.type() == typeid(std::string))
	{
		std::cout << "std::string";
	}
	else
	{
		std::cout << "no";
	}
	std::cout << std::any_cast<int>(res);
	std::cin.get();
}
```

### std::string\_view fast

因为std::string构造和类的函数操作都会在堆上分配内存,而减少在堆上分配内存的次数能够run fast.

std::string\_view构造函数接收`const char *`和长度,通过指针来操作原`std::string`而不是在堆上分配内存

```cpp
#include "../src/include/local.h"
#define ps(str) std::cout << str << std::endl

uint32_t s_AllocCount = 0;

void* operator new(size_t size)
{
	s_AllocCount++;
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
}

#define STRING_VIEW 1

#if STRING_VIEW
void PrintName( std::string_view name)
{
	std::cout << name << std::endl;
}
#else
void PrintName(const std::string& name)
{
	std::cout << name << std::endl;
}
#endif

int main()
{
	std::string name = "Yan Chernikov";

#if STRING_VIEW 
	std::string_view firstName(name.c_str(), 3);
	std::string_view lastName(name.c_str() + 4, 9);
#else 	
	std::string firstName = name.substr(0,3);
	std::string lastName = name.substr(4, 9);
#endif

	PrintName("Cherno");
	PrintName(firstName);
	PrintName(lastName);

	std::cout << s_AllocCount << " allocations" << std::endl;
	std::cin.get();
}
```

### 使用chrome::tracing查看json格式的benchmark数据

生成json格式的benchmark数据,

用chrome::tracing打开

```cpp
#include "../src/include/local.h"
#define  _CRT_SECURE_NO_WARNINGS
#define ps(str) std::cout << str << std::endl

struct ProfileResult
{
	std::string Name;
	long long Start, End;
};

struct InstrumentationSession
{
	//InstrumentationSession(const std::string& name)
	//	:Name(name)
	//{}
	std::string Name;
};

class Instrumentor
{
private:
	InstrumentationSession* m_CurrentSession;
	int m_ProfileCount;

	//生成文件
	std::ofstream m_OutputStream;
public:
	Instrumentor()
		:m_CurrentSession(nullptr),m_ProfileCount(0)
	{
	}
	
	void BeginSession(const std::string &name,const std::string &filepath = "results.json")
	{
		m_OutputStream.open(filepath);
		WriteHeader();
		m_CurrentSession = new InstrumentationSession{name};
	}

	void EndSession()
	{
		WriteFooter();
		m_OutputStream.close();
		delete m_CurrentSession;
		m_CurrentSession = nullptr;
		m_ProfileCount = 0;
	}

	void WriteProfile(const ProfileResult& result)
	{
		if (m_ProfileCount++ > 0)
			m_OutputStream << ",";
		std::string name = result.Name;
		std::replace(name.begin(),name.end(),'"','\'');
		
		m_OutputStream << "{";
		m_OutputStream << "\"cat\":\"function\",";
		m_OutputStream << "\"dur\":" << (result.End - result.Start) << ",";
		m_OutputStream << "\"name\":\"" << name << "\",";
		m_OutputStream << "\"ph\":\"X\",";
		m_OutputStream << "\"pid\":0,";
		m_OutputStream << "\"tid\":0,";
		m_OutputStream << "\"ts\":" << result.Start;
		m_OutputStream << "}";

		m_OutputStream.flush();
	}

	void WriteHeader()
	{
		m_OutputStream << "{\"otherData\": {},\"traceEvents\":[";
		m_OutputStream.flush();
	}

	void WriteFooter()
	{
		m_OutputStream << "]}";
		m_OutputStream.flush();
	}

	static Instrumentor& Get()
	{
		static Instrumentor* instance = new Instrumentor();
		return *instance;
	}
};

class InstrumentationTimer
{
public:
	InstrumentationTimer(const char* name)
		:m_Name(name),m_Stopped(false)
	{
		m_StartTimepoint = std::chrono::high_resolution_clock::now();
	}
	~InstrumentationTimer()
	{
		if (!m_Stopped)
		{
			Stop();
		}
	}
	void Stop()
	{
		auto endTimePoint = std::chrono::high_resolution_clock::now();

		long long start = std::chrono::time_point_cast<std::chrono::microseconds>(m_StartTimepoint).time_since_epoch().count();
		long long end = std::chrono::time_point_cast<std::chrono::microseconds>(endTimePoint).time_since_epoch().count();

		//std::cout << m_Name << ": " << (end - start) << "ms";
		//按照json格式写入文件
		Instrumentor::Get().WriteProfile({ m_Name,start,end });

		m_Stopped = true;
	}
private:
	const char* m_Name;
	std::chrono::time_point<std::chrono::steady_clock> m_StartTimepoint;
	bool m_Stopped;

};


void Function1()
{
	InstrumentationTimer timer("Function1");

	for (int i = 0; i < 1000; i++)
	{
		std::cout << "Hello World #" << i << std::endl;
	}
}

void Function2()
{
	InstrumentationTimer timer("Function2");
	for (int i=0; i<1000; i++)
	{
		std::cout << "Hello World #" << sqrt(i) << std::endl;
	}
}

void RunBenchmarks()
{
	InstrumentationTimer timer("RunBenchmarks");
	Function1();
	Function2();
}

int main()
{
	Instrumentor::Get().BeginSession("Profile");
	RunBenchmarks();
	Instrumentor::Get().EndSession();
	std::cin.get();
}
```

### Singleton(单例模式)或使用namespace来代替

> 单例模式就不解释了,添加一个cpp file,和一个头文件,实现单例模式效果

```cpp
#include "../src/include/local.h"
#define ps(str) std::cout << str << std::endl

class Random
{
private:
	Random() {}
	float m_RandomGenerator = 0.5f;

	float IFloat() { return m_RandomGenerator; }
public:
	/*拷贝构造函数*/
	Random(const Random&) = delete;

	static float Float() 
	{
		return Random::Get().IFloat();
	}

	static Random& Get()
	{
		static Random* s_Instance = new Random();
		return *s_Instance;
	}
};

namespace RandomClass
{
	static float IFloat();
	static float s_RandomGenerator = 0.5f;
	float Float() { return IFloat(); }
}

int main()
{
	float ans = Random::Float();
	std::cout << ans << std::endl;

	float ans1 = RandomClass::Float();
	std::cout << ans1 << std::endl;
	std::cin.get();
}

namespace RandomClass
{
	static float IFloat() { return s_RandomGenerator; }
}
```
