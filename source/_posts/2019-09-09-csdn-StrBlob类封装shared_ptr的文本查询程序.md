---
title: StrBlob类封装shared_ptr的文本查询程序
date: '2019-09-09 16:28:00'
permalink: 2019/09/09/csdn/StrBlob类封装shared_ptr的文本查询程序/
categories:
- 编程语言
- C与C++
---

## 核心: 类之间通过智能指针来共享数据

### 接口和实现分离,并且将`shared_ptr<vector<string>>`封装成`StrBlob`类

#### 并且通过`StrBlobPtr`来作为`StrBlob`的接口

##### `StrBlob`以及`StrBlobPtr`实现

```arduino
#ifndef MY_STRBLOB_H
#define MY_STRBLOB_H

#include <vector>
#include <string>
#include <initializer_list>
#include <memory>
#include <stdexcept>

using namespace std;

class StrBlobPtr;

class StrBlob {
    friend class StrBlobPtr;
    public:
    typedef vector<string>::size_type size_type;
    StrBlob();
    StrBlob(initializer_list<string> i1);
    StrBlob(vector<string> *p);
    size_type size() const { return data->size(); }
    bool empty() const { return data->empty(); }

    void push_back(const string& t) { data->push_back(t); }
    void pop_back();

    string& front();
    const string& front() const;
    string& back();
    const string& back() const;

    StrBlobPtr begin();
    StrBlobPtr end();

    StrBlobPtr begin() const;
    StrBlobPtr end() const;

    private:
    shared_ptr<vector<string>> data;
    void check(size_type i,const string& msg) const;
};

inline StrBlob::StrBlob():data(make_shared<vector<string>>()) {}
inline StrBlob::StrBlob(initializer_list<string> i1):data(make_shared<vector<string>> (i1)) {}
inline StrBlob::StrBlob(vector<string>* p):data(p) {}

inline void StrBlob::check(size_type i,const string& msg) const {
    if (i >= data->size())
        throw out_of_range(msg);
}

inline string& StrBlob::front() {
    check(0,"front on empty StrBlob");
    return data->front();
}
inline const string& StrBlob::front() const {
    check(0,"const front on empty StrBlob");
    return data->front();
}
inline string& StrBlob::back() {
    check(0,"back on empty StrBlob");
    return data->back();
}
inline const string& StrBlob::back() const {
    check(0,"const back on empty StrBlob");
    return data->back();
}
inline void StrBlob::pop_back() {
    check(0,"pop_back on empty StrBlob");
    data->pop_back();
}

class StrBlobPtr {
    friend bool eq(const StrBlobPtr&,const StrBlobPtr&);

    public:
    StrBlobPtr():curr(0) {}
    StrBlobPtr(StrBlob& a,size_t sz=0):wptr(a.data),curr(sz) {}
    StrBlobPtr(const StrBlob& a,size_t sz=0):wptr(a.data),curr(sz) {}

    string& deref() const;
    string& deref(int off) const;

    StrBlobPtr& incr();
    StrBlobPtr& decr();

    private:
    shared_ptr<vector<string>> check(size_t,const string&) const;
    weak_ptr<vector<string>> wptr;
    size_t curr;
};

inline shared_ptr<vector<string>>
StrBlobPtr::check(size_t i,const string& msg) const {
    auto ret = wptr.lock();
    if (!ret)
        throw runtime_error("unbound StrBlobPtr");
    if (i >= ret->size())
        throw out_of_range(msg);
    return ret;
}

inline string& StrBlobPtr::deref() const {
    auto p = check(curr,"dereference past end");
    return (*p)[curr];
}
inline string& StrBlobPtr::deref(int off) const {
    auto p = check(curr + off,"dereference past end");
    return (*p)[curr + off];
}
inline StrBlobPtr& StrBlobPtr::incr() {
    check(curr,"increment past end of StrBlobPtr");
    ++curr;
    return *this;
}
inline StrBlobPtr& StrBlobPtr::decr() {
    --curr;
    check(-1,"decrement past end of StrBlobPtr");
    return *this;
}
inline StrBlobPtr StrBlob::begin() {
    return StrBlobPtr(*this);
}
inline StrBlobPtr StrBlob::end() {
    auto ret = StrBlobPtr(*this,data->size());
    return ret;
}
inline StrBlobPtr StrBlob::begin() const {
    return StrBlobPtr(*this);
}
inline StrBlobPtr StrBlob::end() const {
    auto ret = StrBlobPtr(*this,data->size());
    return ret;
}
inline bool eq (const StrBlobPtr &lhs,const StrBlobPtr &rhs) {
    auto l = lhs.wptr.lock();
    auto r = rhs.wptr.lock();
    if (l == r)
        return (!r || lhs.curr == rhs.curr);
    else
        return false;
}
inline bool neq(const StrBlobPtr &lhs,const StrBlobPtr &rhs) {
    return !eq(lhs,rhs);
}

#endif
```

### 将`TextQuery`和`QueryResult`从`main.cpp`中分离出来

- `my_TextQuery.h`和`my_QueryResult.h`分别作为 类的声明.
- 它们的定义一起实现在`my_TextQuery.cpp`

1. `my_QueryResult.h`
   ```arduino
#ifndef MY_QUERYRESULT_H
#define MY_QUERYRESULT_H

#include <memory>
#include <string>
#include <vector>
#include <set>
#include <iostream>
#include "my_StrBlob.h"

class QueryResult {
    friend std::ostream& print(std::ostream&,const QueryResult&);
public:
    using line_no = std::vector<std::string>::size_type;
    using line_it = std::set<line_no>::const_iterator;
    QueryResult(std::string s,
                std::shared_ptr<std::set<line_no>> p,
                StrBlob f):
            sought(s),lines(p),file(f) {}
    std::set<line_no>::size_type size() const { return lines->size(); }
    line_it begin() const { return lines->cbegin(); }
    line_it end() const { return lines->cend(); }
    StrBlob get_file() { return file; }
private:
    std::string sought;
    std::shared_ptr<std::set<line_no>> lines;
    StrBlob file;
};

std::ostream& print(std::ostream&,const QueryResult&);

#endif
```
2. `my_TextQuery.h`
   ```cpp
#ifndef MY_TEXTQUERY_H
#define MY_TEXTQUERY_H

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <fstream>

#include "my_QueryResult.h"

class QueryResult;
class TextQuery {

public:
    using line_no = std::vector<std::string>::size_type;
    TextQuery(std::ifstream&);
    QueryResult query(const std::string&) const;
    void display_map();
private:
    StrBlob file;
    std::map<std::string,std::shared_ptr<std::set<line_no>>> wm;

    static std::string cleanup_str(const std::string&);
};

#endif
```
3. `my_TextQuery.cpp`
   ```arduino
#include "my_TextQuery.h"

#include <cstddef>
#include <memory>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <fstream>
#include <cctype>
#include <cstring>
#include <utility>

using std::size_t;
using std::shared_ptr;
using std::istringstream;
using std::string;
using std::getline;
using std::vector;
using std::set;
using std::map;
using std::cerr;
using std::cout;
using std::cin;
using std::ostream;
using std::endl;
using std::ifstream;
using std::ispunct;
using std::tolower;
using std::strlen;
using std::pair;

TextQuery::TextQuery(ifstream& is):file(new vector<string>) {
    string text;
    while (getline(is,text)) {
        file.push_back(text);
        int n = file.size() - 1;
        istringstream line(text);
        string word;
        while (line >> word) {
            word = cleanup_str(word);
            auto& lines = wm[word];
            if (!lines)
                lines.reset(new set<line_no>);
            lines->insert(n);
        }
    }
}
string TextQuery::cleanup_str(const string& word) {
    string ret;
    for (auto it = word.begin(); it!=word.end(); ++it)
        if (!ispunct(*it))
            ret += tolower(*it);
    return ret;
}

QueryResult TextQuery::query(const string& sought) const {
    static shared_ptr<set<line_no>> nodata(new set<line_no>);
    auto loc = wm.find(cleanup_str(sought));
    if (loc == wm.end())
        return QueryResult(sought,nodata,file);
    else
        return QueryResult(sought,loc->second,file);
}

ostream& print(ostream& os,const QueryResult& res) {
    os << res.sought << " occurs " << res.lines->size() << " \n";
    for (auto i : *res.lines)
        os << " line " << i+1 << ": " << res.file.begin().deref(i) << " \n";
    return os;
}

void TextQuery::display_map() {
    auto iter = wm.cbegin();
    auto iter_end = wm.cend();
    for (; iter!=iter_end; ++iter) {
        cout << " word: " << iter->first << " {";

        auto& text_locs = iter->second;
        auto loc_iter = text_locs->cbegin();
        auto loc_iter_end = text_locs->cend();

        while (loc_iter != loc_iter_end) {
            cout << *loc_iter;

            if (++loc_iter != loc_iter_end)
                cout << ", ";
        }
        cout << "}\n";
    }
    cout << endl;
}
```

4. `main.cpp`
   ```arduino
#include <iostream>
using std::cin;
using std::cout;
using std::cerr;
using std::endl;

#include <string>
using std::string;

#include <fstream>
using std::ifstream;

#include <cstdlib>
#include "my_TextQuery.h"

void runQueries(ifstream& infile) {
    TextQuery temp(infile);
    while (1) {
        std::string s;
        cout << "enter word to look for, or q to quit: ";
        if(!(cin >> s) || s == "q") break;
        print(cout,temp.query(s));
    }
}
int main() {
    ifstream infile("../other_code/1.in");
    if (!infile)
        std::cout << "fail to open the file\n";

    runQueries(infile);

    infile.close();
    return 0;
}
```

   ### 分析书中代码的设计思路:

   #### `TextQuery`类
5. 处理文本数据 ,将`StrBlob`类作为`private`成员来存储数据.
6. `query()`成员函数返回处理的结果,将处理结果抽象成一个类`QueryResult`
7. `print()`接受 **输出流** 和`QueryResult`**数据结果**结合 输出

   #### `QueryResult`类

- 保存处理结果

  #### `StrBlob`类

1. 为`shared_ptr<vector<string>>`封装了一系列`vector<string>`的操作.
2. 以及`StrBlobPtr`作为`StrBlob`整个类的接口,通过`StrBlobPtr StrBlob::begin()`和`StrBlobPtr StrBlobPtr::end()`实现.

   #### `StrBlobPtr`类
3. `weak_ptr<>`不增加`shared_ptr<>`的引用计数,因此在此类的`weak_ptr`上定义了`vector<string>`的**下标操作**.

### 理解智能指针是一个类,实例化出来的对象有自己的成员函数.例如`.use_count()` `.reset()` `.release()`等,但是可以指针一样使用, 理解`->`与`.`的区别
