---
title: dfs bfs拓扑序列+判断
date: '2019-05-05 15:39:00'
permalink: 2019/05/05/csdn/dfs bfs拓扑序列+判断/
categories:
- 算法
tags:
- 拓扑序列
---

- 想要得到拓扑序的图一定是有向图.
- 拓扑序列虽然不止`1`个,但都满足,每个点的前驱后继点的顺序，**某点的后继点在拓扑序中不可能出现在该点的前面**,

#### 基本思想：

1. 拓扑序列满足，入度为0的点进入序列，且该点的出边点的入度`-1`,
2. 如果该点出边的入度为`0`,则**重复第1步**

###### 邻接表+bfs

1. 开一个数组记录所有点的入度,将入度为`0`的点加入到队列
2. 取出队头,加入到拓扑序.
3. 更新出边的点的入度,判断是否为`0`，为`0`加入队列
4. 重复`2 3`知道队列为空

```arduino
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e6;
int head[maxn];
int next1[maxn];
int ver[maxn];
int tot = 0;
int deg[maxn];
void add(int u,int v) {
	ver[++tot] = v;
	next1[tot] = head[u];
	head[u] = tot;
	//预处理每个点的入度
	deg[v]++;
}
vector<int> ans;
void topsort() {
	queue<int> que;
	for (int i=1; i<=n; i++) //将入度为0的点加入到队列中,
		if (!deg[i]) que.push(i);
	while (!que.empty()) {
		//队列中的点一定是入度=0的点，那么先加入到top序列中,
		int cur = que.top();
		que.pop();
		ans.push_back(cur);
		for (int i=head[cur]; i ; i=next1[i]) {
			deg[i]--;
			if (!deg[i]) que.push(i);
		}
	}
}
int main() {
	freopen("a.txt","r",stdin);
	int n,m;
	cin >> n >> m;
	for (int i=1; i<=m; i++) {
		int u,v;
		cin >> u >> v;
		add(u,v);
	}
	topsort();
	for (int i=0; i<ans.size(); i++) cout << ans[i] << " ";
	return 0;
}
```

##### 邻接表+dfs

- 在dfs回溯时将该点加入栈中,全部点dfs后,出栈的序列为拓扑序

1. dfs回溯时肯定下面的点都走过或者该点为叶子节点(出度一定为`0`，且入度不为`0`),
2. 出边的终点没有走过,往下面走,能想象到每次入栈的一定是从下到上的点，
3. 正好符合前驱后继的关系
4. 每个点都dfs一次,标记的点不dfs,
5. 那么把所有点分成两个集合，一个是待处理的点集D，一个是已拓扑排序后的点集A，当且仅当D中某个点没有后继结点（或该后继结点已经加入了点集A中）时，此时将点从D转移到A，回溯恰好满足这个操作

```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5;
int head[maxn];
//int val[maxn];
int next1[maxn];
int ver[maxn];
int tot = 0;
stack<int> ans;
void add(int u,int v) {
	ver[++tot] = v;
	next1[tot] = head[u];
	head[u] = tot;
}
bool vis[maxn];
int dfs(int x) {
	vis[x] = 1;
	for (int i=head[x]; i ; i=next1[i]) {
		if (!vis[ver[i]]) dfs(ver[i]);
	}
	ans.push(x);
}
int main() {
	freopen("a.txt","r",stdin);
	int n,m;
	cin >> n >> m;
	for (int i=1; i<=m; i++) {
		int u,v;
		cin >> u >> v;
		add(u,v);
	}
	for (int i=1; i<=n; i++) {
		if (!vis[i]) dfs(i); // vis是全局变量，可能先遍历的最低处的点，push进入stack 
	}
	// stack最后push进去的一定是没有出度的点,或者后续节点已经入栈，间接的想到最后push进去的点一定是 入度等于0的点 
	while (!ans.empty()) {
		cout << ans.top() << endl;
		ans.pop();
	}
	return 0;
}
```

##### 判断是否存在拓扑序列（既不存在入度为0的点）

- 恰好成环也有拓扑序，存在入度`=0`的点
- 成环的意思是总有一点的入度不为0，没有拓扑序列
- `vis[i]`代表3中状态,`1`此轮dfs访问过,`-1`别的dfs访问过，`0`没有被访问过，
- 此轮dfs访问到`vis[i]=1`说明能够返回该点,则存在不存在入度`=0`的点
  ```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5;
int tot = 0;
int head[maxn];
int next1[maxn];
int ver[maxn];
int vis[maxn];
int n,m;
stack<int> ans;
void add(int u,int v) {
	ver[++tot] = v;
	next1[tot] = head[u];
	head[u] = tot;
}
bool dfs(int x) {
	vis[x] = 1;
	for (int i=head[x]; i ; i=next1[i]) {
		int v = ver[i];
		if ( vis[v] == 1 ) return false;
		if ( vis[v] == 0 && !dfs(v) ) return false;
	}
	vis[x] = -1;
	ans.push(x);
	return true;
}
int main() {
	freopen("a.txt","r",stdin);
	cin >> n >> m;
	for (int i=1; i<=m; i++) {
		int u,v;
		cin >> u >> v;
		add(u,v);
	}
	bool flag = true;
	for (int i=1; i<=n; i++) {
		if ( vis[i] == 0 ) 
			if ( !dfs(i) ) {
				cout << i << endl;
				flag = false;
				cout << "无法生成拓扑序列" << endl;
				break;
			} 
	}
	while ( flag && !ans.empty() ) {
		cout << ans.top() << endl;
		ans.pop();
	} 
	return 0;
}
```
