---
title: StrBlob类的实现(shared_ptr与weak_ptr的混用)
date: '2019-08-31 20:57:00'
permalink: 2019/08/31/csdn/StrBlob类的实现(shared_ptr与weak_ptr的混用)/
categories:
- 编程语言
- C与C++
tags:
- 智能指针
---

`my_StrBlob.h`

- 实现了2个类`StrBlob StrBlobPtr`
- `StrBlob`成员包含`shared_ptr<>`,`StrBlobPtr`这个伴随类有`weak_ptr<>`和`shared_ptr`共享一块内存,在2个类之间建立一些接口
- 作为参数的`initializer_list<>`的用法,**实参数量未知但是实参类型相同**,用法和`vector`类似,但`initializer_list<>`的元素是常量

  ```arduino
#ifndef MY_STRBLOB_H
#define MY_STRBLOB_H

#include <vector>
#include <string>
#include <memory>
#include <initializer_list>
using namespace std;

class StrBlobPtr;
class StrBlob {
	friend class StrBlobPtr;
	public:
		typedef vector<string>::size_type size_type;
		StrBlob() :data(make_shared<vector<string>>()) {}
		StrBlob(initializer_list<string> i1) :data(make_shared<vector<string>>(i1)) {}
		size_type size() const { return data->size(); }
		bool empty() const { return data->empty(); }
		int get_use_count() const { return data.use_count(); }

		void push_back(const string& t) { data->push_back(t); }
		void pop_back();

		string& front();
		const string& front() const;
		string& back();
		const string& back() const;

		//  将自己作为StrBlobPtr的构造函数参数来构造StrBlobPtr对象
		StrBlobPtr begin();
		StrBlobPtr end();

		// 接收 const StrBlob & 对象来构造StrBlobPtr对象
		StrBlobPtr begin() const;
		StrBlobPtr end()   const;
	private:
		shared_ptr<vector<string>> data;
		void check(size_type,const string&) const;
};
inline void StrBlob::check(size_type i, const string& msg) const {
	if (i >= data->size())
		throw out_of_range(msg);
}
inline string& StrBlob::front() {
	check(0,"front");
	return data->front();
}
inline const string& StrBlob::front() const {
	check(0,"const front");
	return data->front();
}
inline string& StrBlob::back() {
	check(0,"back");
	return data->back();
}
inline const string& StrBlob::back() const{
	check(0,"const back");
	return data->back();
}
inline void StrBlob::pop_back() {
	check(0,"pop_back");
	data->pop_back();
}

class StrBlobPtr {
	friend bool eq(const StrBlobPtr&, const StrBlobPtr&);
	public:
		StrBlobPtr():curr(0) {}
		StrBlobPtr(StrBlob& a, size_t sz = 0) :wptr(a.data), curr(sz) {}
		//接收const StrBlob & 对象的构造函数
		StrBlobPtr(const StrBlob& a, size_t sz = 0) :wptr(a.data), curr(sz) {}

		string& deref() const; //返回下标出的值
		StrBlobPtr& incr(); //curr后移
		StrBlobPtr& decr(); //curr前移
	private:
		size_t curr; //下标
		weak_ptr<vector<string>> wptr; //此类的精华,weak_ptr<> 弱shared_ptr指针
		shared_ptr<vector<string>> check(size_t,const string&) const;
};
inline shared_ptr<vector<string>> StrBlobPtr::check(size_t i, const string& msg) const {
	auto ret = wptr.lock();
	if (!ret)
		throw runtime_error("empty");
	if (i >= ret->size())
		throw out_of_range(msg);
	return ret;
}
inline string& StrBlobPtr::deref() const {
	auto p = check(curr,"dereference past end");
	return (*p)[curr];
}
inline StrBlobPtr& StrBlobPtr::incr() {
	check(curr,"incement past end of StrBlobPtr");
	++curr;
	return *this;
}
inline StrBlobPtr& StrBlobPtr::decr() {
	curr--;
	// 直接减,然后检查不是-1就行了
	check(-1,"decrment past end of StrBlobPtr");
	return *this;
}// 实现了StrBlobPtr,开始实现与StrBlob之间的接口
inline StrBlobPtr StrBlob::begin() {
	return StrBlobPtr(*this);
	//返回指向首元素的StrBlobPtr
}
// 接收 const 对象
inline StrBlobPtr StrBlob::begin() const {
	return StrBlobPtr(*this);
}
//返回指向最后一个元素的
inline StrBlobPtr StrBlob::end() {
	auto ret = StrBlobPtr(*this,data->size());
	return ret;
}
inline StrBlobPtr StrBlob::end() const {
	return StrBlobPtr(*this, data->size());
}
inline bool eq(const StrBlobPtr& lhs, const StrBlobPtr& rhs) {
	auto l = lhs.wptr.lock(); // 智能指针本着是一个对象, .来访问自己的成员
	auto r = rhs.wptr.lock();
	if (l == r) // 都为空,或者指向的对象一样
		//空 或者 指向相同的元素
		return (!r || lhs.curr == rhs.curr);
	else
		return false;
}
inline bool neq(const StrBlobPtr& lhs, const StrBlobPtr& rhs) {
	return !eq(lhs,rhs);
}
#endif
```
- 通过`StrBlobPtr`类来打印每个`string`元素

  ```arduino
#include <iostream>
#include <fstream>
#include "Sales_data.h"
using namespace std;
int main() {
	fstream in("1.in");
	if (!in) {
		cout << "faile to open 1.in" << endl;
		return -1;
	}
	StrBlob b;
	string s;
	while (getline(in, s))
		b.push_back(s);
	// StrBlob.begin() 生成了StrBlobPtr对象,通过StrBlobPtr来访问每个元素的内容
	for (auto it = b.begin(); neq(it, b.end()); it.incr())
		cout << it.deref() << endl;
	return 0;
}
```
