---
title: Sales_data类实现 及 类特性
date: '2019-08-24 22:16:00'
permalink: 2019/08/24/csdn/Sales_data类实现 及 类特性/
categories:
- 编程语言
- C与C++
tags:
- 类
---

实现`Sales_data`类

```cpp
#include <iostream>
#include <string>
class Sales_data {
	friend std::istream& operator >> (std::istream&, Sales_data&);
	friend std::ostream& operator << (std::ostream&,const Sales_data&);
	friend bool operator == (const Sales_data&, const Sales_data&);
	public: //重载类的+=运算符
		Sales_data& operator += (const Sales_data&);
		std::string isbn() const { return bookNo; }
	public:
		Sales_data() = default; //显式声明默认构造函数
		Sales_data(const std::string& book) :bookNo(book){}
		Sales_data(std::istream& is) { is >> *this; }
	private:
		std::string bookNo;
		unsigned units_sold = 0;
		double sellingprice = 0.0;
		double saleprice = 0.0;
		double discount = 0.0;
};
//好习惯: 现将友元函数声明
std::istream& operator >> (std::istream&, Sales_data&);
std::ostream& operator << (std::ostream&, const Sales_data&);
bool operator == (const Sales_data&, const Sales_data&);
//全局函数.
inline bool compareIsbn(const Sales_data& lhs, const Sales_data& rhs) {
	return lhs.isbn() == rhs.isbn();
}
inline bool operator == (const Sales_data& lhs, const Sales_data& rhs) {
	return lhs.units_sold == rhs.units_sold &&
		lhs.sellingprice == rhs.sellingprice &&
		lhs.saleprice == rhs.saleprice &&
		lhs.isbn() == rhs.isbn();
}
inline bool operator != (const Sales_data& lhs, const Sales_data& rhs) {
	return !(lhs == rhs);
}
Sales_data& Sales_data::operator += (const Sales_data& rhs) {
	units_sold += rhs.units_sold;
	saleprice = (rhs.saleprice * rhs.units_sold + saleprice * units_sold) / (rhs.units_sold + units_sold);
	if (sellingprice != 0)
		discount = saleprice / sellingprice;
	return *this;
}
Sales_data operator + (const Sales_data& lhs, const Sales_data& rhs) {
	Sales_data ret(lhs);
	ret += rhs;
	return ret; //如果返回引用,临时对象内存被销毁,引用没意义,只能返回临时对象的拷贝
}
std::istream& operator >> (std::istream& in, Sales_data& s) {
	in >> s.bookNo >> s.units_sold >> s.sellingprice >> s.saleprice;
	if (in && s.sellingprice != 0)
		s.discount = s.saleprice / s.sellingprice;
	else
		s = Sales_data();//默认构造
	return in;
}
std::ostream& operator << (std::ostream& out,const Sales_data& s) {
	out << s.isbn() << " " << s.units_sold << " " << s.sellingprice << " " << s.saleprice << " " << s.discount;
	return out;
}
int main() {
	Sales_data trans1, trans2;
	std::cout << "输入2条相同的ISBN销售记录: " << std::endl;
	std::cin >> trans1 >> trans2;
	if (compareIsbn(trans1, trans2))
		std::cout << "汇总信息: ISBN,售出本数,原始价格,实际价格,折扣:" << trans1 + trans2 << std::endl;
	else std::cout << "2条销售记录ISBN不相同 " << std::endl;
	Sales_data total, trans;
	std::cout << " 请输入几条ISBN相同的销售记录: " << std::endl;
	if (std::cin >> total) {
		while (std::cin >> trans) {
			if (compareIsbn(total, trans))
				total += trans;
			else {
				std::cout << " 当前书的ISBN不同 " << std::endl;
				break;
			}
		}
		std::cout << "有效汇总信息: ISBN,售出书本,原始价格,实际价格,折扣:" << total << std::endl;
	}
	else {
		std::cout << " 没有数据 " << std::endl;
		return -1;
	}
	return 0;
}
```

## 构造函数初始值列表

- 为数据成员赋初值,赋值的顺序根据数据成员定义的顺序

  ## `=default`要求编译器生成默认构造函数

  `Sales_data() = default;`

  ## `this`的引入
- `obj.isbn() //成员函数的调用`,**成员函数通过名为`this`的额外隐式参数来访问调用它的对象,调用一个成员函数时,用请求该函数的对象地址初始化`this`**
- 从编译器角度等价于`Sales_data::isbn(&obj);`.
- 我们能在**成员函数内部直接调用该函数对象的成员就是通过`this`实现的,被看做是`this`的隐式引用,**

  ### `this`本身是一个常量指针 (不要和指向常量的指针混淆).
- **常量指针**即:指针存的地址是不变的,
- **指向常量的指针**即:指向的对象是不变的
- 所以不能改变`this`保存的地址

  ## `const`成员函数

  `std::string isbn() const { return bookNo; }`
- 相当于隐式修改`this`的类型,本来是常量指针`Sales_data * const`
- 现在是`const Sales_data * const`,**指向常量的常量指针,意味着指向的对象是常量,如果该函数不需要修改对象的数据成员,那么`const`成员函数很有必要**,

  ## 类的作用域`Sales_data::`, 全局作用域`::`
- 如果`isbn()`定义在类的外部.`std::string Sales_data::isbn() const { return bookNo; }`
- 那么在`Sales_data::`之后都属于类的作用域内,如果`isbn()`要返回**类中定义的变量类型**,那么返回值要声明作用域

## 定义返回`this`对象的函数

`````autohotkey
Sales_data& operator += (const Sales_data&);
//用一个函数代替重载+=的效果
Sales_data& Sales_data::combine(const Sales_data &rhs) {
    units_sold += rhs.units_sold;
    return *this; //解引用返回this绑定对象本身
}
//使用combine时,total绑定到this上,trans 绑定到 rhs上,
total.combine(trans);

````
* 结果都加到`total`中,因为定义的函数类似`+=`运算符,**左边的运算对象作为左值返回**,**必须与左值返回保持一致**,所以**要返回total对象本身**
* 如果返回类型是`Sales_data`,**相当于通过拷贝创建了一个临时对象然后返回**.

## 访问控制符 `access specifiers`
* `class`与`struct`的区别在于 **第一个访问控制符出现之前**  `class`的默认权限是`private`,而`struct`的权限是`public`
* `private`的数据成员**只能被类的成员函数访问**,而使用该类的代码不能访问,需要在`public`中提供**接口**,`private`相当于封装了类的实现细节

## 友元
* 其他类或者函数访问它的**非公有成员**,方法是声明**其他类或函数**成为**该类的友元(`friend`)**
* 友元函数的声明,仅仅是声明了友元的关系,并不是函数声明.
## 类成员
1. 定义类型成员,别名(`alias`)作用范围从定义开始
`````

class Screen {  
 public:  
 typedef std::string::size\_type pos;  
 // using pos=std::string::size\_type;  
};

```clean
* 在类外使用类的类型成员要说明作用域
## inline是否展开取决于编译器

## 构造函数的默认实参
```

Sales\_data(std::string s = “”):bookNo(s) {}

```markdown
* 使用实参来初始化`bookNo`,不接受参数就默认`string`初始化

## 委托构造函数
* 委托构造函数使用所属类的其他构造函数来执行自己的初始化过程,
* 先执行所委托给的构造函数,然后再来执行自己函数体的内容
```

Sales\_data(std::string s,unsigned cnt,double sellp,double salep) : bookNo(s),units\_sold(cnt),sellingprice(sellp),saleprice(salep){}  
Sales\_data() : Sales\_data(“”, 0, 0.0, 0.0) {}  
Sales\_data(std::istream& is) :Sales\_data() { is >> \*this; }

```clean
* 委托构造函数能够多层委托,可以委托给一个已经是委托构造函数的函数,从受委托的构造函数开始依次执行代码.最后才返回到委托者自身函数体

## 使用默认构造函数
```

Sales\_data obj(); //错误,声明了一个返回值是Sales\_data的函数  
Sales\_data obj; //调用默认构造

```clean

## 隐式类型转换规则 (关键字:`explicit`)
* 只存在于 **接收一个实参的构造函数,默认就定义了为此类类型的隐式转换机制**
#### 在需要使用`Sales_data`的地方,**使用接收一个参数的构造函数的参数类型作为替代,能隐式转化成Sales_data类型**
```

//如果:  
Class Sales\_data {  
 public:  
 Sales\_data& combine(Sales\_data&);  
};

string ss = “aaa”;  
total.combine(ss); //combine另一个Sales\_data的对象,这里用string对象替代  
//编译器用string对象创建了一个Sales\_data对象,这个生成的Sales\_data临时对象作为参数传给combine

```asciidoc
* 只能从**一个参数的构造函数的参数类型转换到Sales_data**
```

total.combine(“dads”); //“dads”是c风格的字符串 char[],不是string对象  
total.combine(string(“abc”)); //转化成string  
total.combine(Sales\_data(“abc”)); //直接转化成Sales\_data对象

```clean
### 抑制构造函数定义的隐式类型转换 explicit :明白的
* 只在接收一个参数的构造函数中定义了隐式类型转换,即使对于多个参数构造函数声明了也没意义
```

class Sales\_data {  
 public:  
 Sales\_data() = default;  
 Sales\_data(const std::string &s,unsigned n,double p1,double p2):  
 bookNo(s),units\_sold(n),sellingprice(p1),saleprice(p2) {}  
 explicit Sales\_data(const std::string &s) : bookNo(s) {}  
 explicit Sales\_data(std::istream&);  
};

```markdown
* 函数在类外部定义时不需要再次声明explicit
* 拷贝初始化
```

std::string temp = “acx”;  
Sales\_data item(temp);  
Sales\_data item = temp; //拷贝形式,隐式转换成Sales\_data

```asciidoc
* 强制类型转换
```

item.combine(Sales\_data(temp));  
item.combine(static\_cast(cin));  
item.combine(static\_cast(temp));

```clean

## 友元部分的理解,(最好在友元函数实现前,声明一次,有点编译器需要声明)
```

friend std::istream& operator >> (std::istream&, Sales\_data&);  
friend std::ostream& operator << (std::ostream&,const Sales\_data&);  
friend bool operator == (const Sales\_data&, const Sales\_data&);

```autohotkey
* 在全局作用域内重载`>>` 和 `<<`运算符,友元的目的是访问到Sales_data对象的private成员
## `istream` `ostream`输入输出流的使用
* `cin`和`cout`分别是`iostream`类和`ostream`的对象
* 接收流的引用,**特别要注意返回流的引用**
```

std::istream& operator >> (std::istream& in, Sales\_data& s) {  
 in >> s.bookNo >> s.units\_sold >> s.sellingprice >> s.saleprice;  
 if (in && s.sellingprice != 0)  
 s.discount = s.saleprice / s.sellingprice;  
 else  
 s = Sales\_data();//默认构造  
 return in;  
}  
std::ostream& operator << (std::ostream& out,const Sales\_data& s) {  
 out << s.isbn() << “ “ << s.units\_sold << “ “ << s.sellingprice << “ “ << s.saleprice << “ “ << s.discount;  
 return out;  
}

```
* 构造函数接收的输入流对象参数,那么想要通过流来初始化对象一定要重载`>>`  
`Sales_data(std::istream& is) { is >> *this; }`
```
