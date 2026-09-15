---
title: POJ_1860_判断正权环(bellmanford和floyd)
date: '2019-07-07 21:01:00'
permalink: 2019/07/07/csdn/POJ_1860_判断正权环(bellmanford和floyd)/
categories:
- 算法
---

### 5

[POJ 1860](http://poj.org/problem?id=1860)  
题意：货币种类是点,货币交换是边,能否在交换回来使得金钱变多,意思就是是否存在正环

- 两层循环 模拟一次流通后 每一个点 的金钱数
- 将第一次多次循环和第二次比较，若有任意一个点钱数变多则说明存在正环
  ```cpp
#include <iostream>
using namespace std;
const int maxn = 105;
int n,m,start;
double money;
double dist[maxn];
double profit[maxn][maxn],cost[maxn][maxn];

bool istrue() {
	double backup[maxn];
	for (int i=1; i<=n; i++) backup[i] = dist[i];
	for (int k=1; k<=n; k++)
		for (int i=1; i<=n; i++)
			for (int j=1; j<=n; j++) 
				if ( (dist[i] - cost[i][j]) * profit[i][j] > dist[j] )
					dist[j] = (dist[i] - cost[i][j]) * profit[i][j];
	for (int i=1; i<=n; i++) 
		if (dist[i] > backup[i]) return 1;
	return 0;
}
int main() {
//	freopen("a.txt","r",stdin);
	cin >> n >> m >> start >> money;
	for (int i=1; i<=m; i++) {
		int u,v;
		double profit1,cost1,profit2,cost2;
		cin >> u >> v >> profit1 >> cost1 >> profit2 >> cost2;
		profit[u][v] = profit1; cost[u][v] = cost1;
		profit[v][u] = profit2; cost[v][u] = cost2;
	}
	dist[start] = money;
	istrue(); 
	if (istrue()) cout << "YES\n";
	else cout << "NO\n";
	return 0;
}
```

bellman\_ford 求最大回路是否存在正环

- 修改松弛条件,`dist[i]`表示换成货币`i`的钱,
- `dist[]`初始化为负的最小值,源点为起始金钱,向外松弛,记录每个点的松弛次数,
- 只要存在正环,那么某个点肯定会一直松弛下去,通过这个判断
  ```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <string.h>

using namespace std;
const int maxn = 105;
const int MIN = -0x3f3f3f3f;

struct node {
	int from,to;
	double profit,cost;
	node (){};
	node (int a,int b,double c,double d) {
		from = a; to = b; profit = c; cost = d;
	}
};
vector<node> edges;
vector<int> e[maxn];
int n,m,start;
double money;
double dist[maxn];
bool vis[maxn];
int cnt[maxn];

void addedge(int u,int v,double profit1,double cost1,double profit2,double cost2) {
	edges.push_back( node(u,v,profit1,cost1) );
	edges.push_back( node(v,u,profit2,cost2) );
	int id = edges.size();
	e[u].push_back(id-2);
	e[v].push_back(id-1);
}
bool bellmanford() {
	queue<int> que;
	for (int i=1; i<=n; i++) dist[i] = MIN;
	memset(vis,0,sizeof vis);
	vis[start] = 1; dist[start] = money;
	que.push(start);
	while (!que.empty()) {
		int cur = que.front(); que.pop();
		vis[cur] = 0;
		for (int i=0; i<e[cur].size(); i++) {
			int id = e[cur][i];
			node& tmp = edges[id];
			if (dist[tmp.to] < (dist[cur] - tmp.cost)*tmp.profit) {
				dist[tmp.to] = (dist[cur] - tmp.cost) * tmp.profit;
				if (!vis[tmp.to]) {
					que.push(tmp.to);
					vis[tmp.to] = 1;
					if (++cnt[tmp.to] > n) return  1;
				}
			}
		}
	}
	return 0;
}
int main() {
//	freopen("a.txt","r",stdin);
	cin >> n >> m >> start >> money;
	for (int i=1; i<=m; i++) {
		int u,v;
		double profit1,cost1,profit2,cost2;
		cin >> u >> v >> profit1 >> cost1 >> profit2 >> cost2;
		addedge(u,v,profit1,cost1,profit2,cost2);
	}
	if (bellmanford()) cout << "YES\n";
	else cout << "NO\n";
	return 0;
}
```
