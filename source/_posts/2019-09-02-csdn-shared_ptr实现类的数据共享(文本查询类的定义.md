---
title: shared_ptr实现类的数据共享(文本查询类的定义
date: '2019-09-02 19:58:00'
permalink: 2019/09/02/csdn/shared_ptr实现类的数据共享(文本查询类的定义/
categories:
- C++primer读书笔记
---

### 面对过程

- `vector<>`来存输入文件的每一行
- `map<string,set<int>>`,每一个单词映射一个集合,集合包含其出现的行数
- `istringstream`:将每一行`string`放到字符串流里面,通过流来分割出单词,
  ```arduino
 1 #include <iostream>
 2 #include <sstream>
 3 #include <fstream>
 4 #include <vector>
 5 #include <set>
 6 #include <map>
 7 #include <string>
 8 
 9 #include <cstdlib>
10 using namespace std;
11 using line_no = vector<string>::size_type;
12 vector<string> file;
13 map<string,set<line_no>> wm;
14 
15 string cleanup_str(const string& word) {
16     string ret;
17     for (auto it = word.begin(); it!=word.end(); it++) {
18         if (!ispunct(*it))
19             ret += tolower(*it);
20     }
21     return ret;
22 }
23 
24 ostream& query_and_print(const string& sought,ostream& os) {
25     auto loc = wm.find(sought);
26     if (loc == wm.end()) {
27         os << sought << " have seen zero times " << endl;
28     } else {
29         // loc is a iterator , and pair<> is being pointed
30         auto lines = loc->second;
31         os << sought << "have seen " << lines.size() << " times " << endl;
32         for (auto num : lines)                                                   
33             os << "\t (The " << num+1 << " line) " << *(file.begin() + num) << e#
34     }
35     return os;
36 }
37 
38 void input_txt(ifstream& is) {
39     string text;
40     while (getline(is,text)) {
41         file.push_back(text);
42         int n = file.size() - 1;
43         istringstream line(text);
44         string word;                                                             
45         while (line >> word)
46             wm[cleanup_str(word)].insert(n);
47         }
48 }
49 void runQueries(ifstream& infile) {
50     input_txt(infile);
51     while (true) {
52         cout << "Enter word to look for, or q to quit: ";
53         string s;
54         if (!(cin >> s) || s == "q") break;
55         query_and_print(s,cout);
56     }
57 }
58 int main() {
59     ifstream infile("1.in");
60     if (!infile) {
61         cout << " fail to open infile ";
62         return -1;
63     }
64     runQueries(infile);
65     infile.close();
66     return 0;
67 }
```

### 关于&是否会增加shared\_ptr<>的引用计数问题

- **变量的引用只是变量的别名,并不会增加智能指针的引用计数**
  ```cpp
 1 #include <iostream>
 2 #include <memory>
 3 using namespace std;
 4 
 5 int main() {
 6     shared_ptr<int> p (new int(24));
 7     cout << p.use_count() << endl;
 8 
 9     auto& q = p;                                                                 
10     cout << " q.use_count()= " << q.use_count() << " *q= " << *q << endl;
11     cout << " p.use_coutn()= " << p.use_count() << " *p= " << *p << endl;
12     return 0;
13 }
```
- 创建了一个新的`shared_ptr<>`对象并且指向同一块内存,自然就会增加`shared_ptr`的引用计数
  ```cpp
 1 #include <iostream>
 2 #include <memory>
 3 using namespace std;
 4 
 5 int main() {
 6     shared_ptr<int> p (new int(24));
 7     cout << p.use_count() << endl;
 8 
 9     auto q = p;                                                                  
10     cout << " q.use_count()= " << q.use_count() << " *q= " << *q << endl;
11     cout << " p.use_coutn()= " << p.use_count() << " *p= " << *p << endl;
12     return 0;
13 }
```

  ### 面对对象

  ```arduino
// 注意使用指针和对象之间的区别
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <memory>
using namespace std;
//QueryResult 保存查询结果的类,要想共享类之间的数据且不通过拷贝,shared_ptr<>来解决
class QueryResult;
class TextQuery {
public:
	using line_no = vector<string>::size_type; //类型成员
	TextQuery(ifstream&); //接收 文件流来读取文本
	QueryResult query(const string&) const; // 
private:
	shared_ptr<vector<string>> file;
	map<string, shared_ptr<set<line_no>>> wm; //string 关联一个 动态分配的set<>集合
};
TextQuery::TextQuery(ifstream& in):file(new vector<string>){
	string text;
	while (getline(in,text)) {
		(*file).push_back(text);
		int n = (*file).size() - 1;
		istringstream line(text);
		string word;
		while (line >> word) {
			// wm[word] 是一个shared_ptr<set<line_no>>指针,但是我们不确定他是否分配了内存
			auto& lines = wm[word]; //& 不增加 引用计数
			if (!lines) //如果 智能指针为空,.reset(新动态内存对象)
				lines.reset(new set<line_no>);
			(*lines).insert(n);
		}
	}
}
class QueryResult {
	friend ostream& print(ostream&,const QueryResult&); //友元
public:
	using line_no = vector<string>::size_type;
	QueryResult(string s, shared_ptr<set<line_no>> p, shared_ptr<vector<string>> f) :sought(s), lines(p), file(f) {}
private:
	// 查询结果3内容
	string sought;
	shared_ptr<set<line_no>> lines;
	shared_ptr<vector<string>> file;
};
QueryResult TextQuery::query(const string& sought) const{
	//如果 没有找到该单词所属的行,返回一个指向空set的shared_ptr,static(全局静态)保证了函数结束前内存不会被释放
	static shared_ptr<set<line_no>> nodata(new set<line_no>);
	auto loc = wm.find(sought);
	if (loc == wm.end())
		//将TextQuery的内存也让QueryResult的shared_ptr指向,这样就能共享内存，
		return QueryResult(sought, nodata, file);
	else
		return QueryResult(sought,loc->second,file);
}
ostream& print(ostream& os, const QueryResult& qr) { //接收一个查询结果类
	os << qr.sought << " occurs " << qr.lines->size() << " times " << endl;
	for (auto num : *qr.lines)
		os << "\t(line " << num + 1 << ")  " << *(qr.file->begin() + num) << endl;
	return os;
}
int main() {
	ifstream in("a.txt");
	if (!in) { //文件打开失败,return 
		cout << "fail to open file " << endl;
		return -1;
	}
	TextQuery solution(in); //传入输入流对象初始化
	while (1) {
		cout << " Enter word to look for, or q to quit: ";
		string s;
		if (!(cin >> s) || s == "q") break;
		print(cout,solution.query(s)); //querys返回一个QueryResult对象
	}
	return 0;
}
```
