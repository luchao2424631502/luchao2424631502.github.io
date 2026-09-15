---
title: 使用boost/program_options遇到的一点小问题
date: '2022-01-14 07:32:00'
permalink: 2022/01/14/遇到boostprogram-options遇到的一点小问题/
categories:
- C++
tags:
- Boost
---

### 使用boost/program\_options遇到的一点小问题

#### 1.boost/program\_options::options\_description类

[使用例子](https://www.boost.org/doc/libs/1_78_0/doc/html/program_options/tutorial.html)

```cpp
po::options_description desc("Allowed options");
desc.add_options()
    ("help", "produce help message")
    ("compression", po::value<int>(), "set compression level")
;
po::variables_map vm;
po::store(po::parse_command_line(ac, av, desc), vm);
po::notify(vm);    

if (vm.count("help")) {
    cout << desc << "\n";
    return 1;
}

if (vm.count("compression")) {
    cout << "Compression level was set to " 
 << vm["compression"].as<int>() << ".\n";
} else {
    cout << "Compression level was not set.\n";
}
```

这个po::add\_options方法第一眼看有点奇怪,正好也遇到了[Line 164](https://github.com/luchao2424631502/emerald/blob/master/src/pmd/pmdOptions.cpp),于是看了看解释和实现

1. 手册解释: The add\_options method of that class returns a special proxy object that defines operator(). Calls to that operator actually declare options,这个类的add\_options方法返回了一个特殊的代理对象,这个对象重载了`operator()`
2. 查看[options\_description类定义](https://www.boost.org/doc/libs/1_78_0/doc/html/boost/program_options/options_description.html)

   ```cpp
// In header: <boost/program_options/options_description.hpp>


class options_description {
public:
  // construct/copy/destruct
  options_description(unsigned = m_default_line_length, 
                      unsigned = m_default_line_length/2);
  options_description(const std::string &, unsigned = m_default_line_length, 
                      unsigned = m_default_line_length/2);

  // public member functions
  void add(shared_ptr< option_description >);
  options_description & add(const options_description &);
  unsigned get_option_column_width() const;
  options_description_easy_init add_options();
  const option_description & 
  find(const std::string &, bool, bool = false, bool = false) const;
  const option_description * 
  find_nothrow(const std::string &, bool, bool = false, bool = false) const;
  const std::vector< shared_ptr< option_description > > & options() const;
  void print(std::ostream &, unsigned = 0) const;

  // friend functions
  friend BOOST_PROGRAM_OPTIONS_DECL std::ostream & 
  operator<<(std::ostream &, const options_description &);

  // public data members
  static const unsigned m_default_line_length;
};
```

   看到返回的代理类是`options_deescription_easy_init`,于是看看其实现:

   ```cpp
options_description_easy_init
options_description::add_options()
{
	return options_dscription_easy_init(this);
}
```

在来看看[这个类的定义](https://www.boost.org/doc/libs/1_78_0/doc/html/boost/program_options/options_d_1_3_32_9_7_1_1_4.html)，

```cpp
   // In header: <boost/program_options/options_description.hpp>
   
   
   class options_description_easy_init {
public:
     // construct/copy/destruct
     options_description_easy_init(options_description *);
    // public member functions
     options_description_easy_init & operator()(const char *, const char *);
    options_description_easy_init & 
     operator()(const char *, const value_semantic *);
     options_description_easy_init & 
     operator()(const char *, const value_semantic *, const char *);
   };
```

果然重载了`operator()`,并且支持3种插入配置参数的规则: The parameters are option name, information about value, and option description.

然后到boost源码里面看看具体的实现`boost/libs/program_options/src/options_description.cpp`

摘出了一段:

```
   options_description_easy_init&
   options_description_easy_init::
   operator()(const char* name,
              const char* description)
   {
       // Create untypes semantic which accepts zero tokens: i.e. 
       // no value can be specified on command line.
       // FIXME: does not look exception-safe
       shared_ptr<option_description> d(
           new option_description(name, new untyped_value(true), description));

       owner->add(d);
       return *this;
   }

   options_description_easy_init&
   options_description_easy_init::
   operator()(const char* name,
              const value_semantic* s)
   {
       shared_ptr<option_description> d(new option_description(name, s));
       owner->add(d);
       return *this;
   }

   options_description_easy_init&
   options_description_easy_init::
   operator()(const char* name,
              const value_semantic* s,
              const char* description)
   {
       shared_ptr<option_description> d(new option_description(name, s, description));

       owner->add(d);
       return *this;
   }
```

`owner`是指向被代理类的指针`options_description *owner;`

这个代理类构造一条`option_description`利用`owner`指针调用`options_description::add()`添加一条配置记录.

#### 2. 小结

> 这应该是一个设计模式,但是我还不知道叫什么….

自己实现一下其中关系:

```arduino
c++
#include <iostream>
#include <map>
#include <string>

class Base;

//就是一个代理类
class Base_init
{
  private:
    Base *m_owner;
  public:
    Base_init(Base *owner):m_owner(owner) {}
    ~Base_init() {}
  public:
    Base_init &operator()(const char *a,const char *b);
    /*
    Base_init &operator()(const char *a,const value_semantic *s) {}
    Base_init &operator()(const char *a,const value_semantic *s,const char *description) {}
    */
};

//被代理的类
class Base
{
  private:
    std::map<std::string,std::string> _map;
  public:
    Base() {}
    ~Base() {}
  public:
    Base_init add_desc();

    void add(const char *a,const char *b);
    
    void print();
};

Base_init 
Base::add_desc()
{
  return Base_init(this);
}

void 
Base::add(const char *a,const char *b)
{
  _map.insert(std::make_pair<std::string,std::string>(a,b));
}

void 
Base::print()
{
  std::map<std::string,std::string>::iterator it = _map.begin();
  while (it != _map.end())
  {
    std::cout << it->first << " " << it->second << std::endl;
    it++;
  }
}

Base_init&
Base_init::operator()(const char *a,const char *b)
{
  m_owner->add(a,b);
  return *this;
}

int main()
{
  Base b;
  b.add_desc()
    ("key1","llc1")
    ("key2","llc2")
    ("key3","llc3")
    ("key4","llc4");
  b.print();
  return 0;
}
```
