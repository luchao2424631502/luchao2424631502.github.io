---
title: POJ_1511_(dij/bellmanford)
date: '2019-07-09 10:37:00'
permalink: 2019/07/09/csdn/POJ_1511_(dij!bellmanford)/
categories:
- 算法
---

[POJ 1511](http://poj.org/problem?id=1511)

- 题意：求每个点去1点的时间和回来时间的最小值,回来的最短时间就是**点1到每一个点的最短路径**,那么每个点去点1的时间呢？单独求每个点到点1时间肯定超时
- 将所有有向边都反向,在求点1到每个点的最短路径就相当于去点1的时间
- 主要是数据量太大,只能用邻接表存图,关键在于邻接表的构建

1. bellmanford
   ```cpp
 #include <iostream>
#include <vector>
#include <string.h>
#include <queue>

using namespace std;
const int maxn = 1e6+3;

struct node {
	int to,div;
	node () {};
	node (int v,int w) {
		to = v; div = w;
	}
};
int n,m;
bool vis[maxn];
int dist[2][maxn];
vector<node> e[2][maxn];

void bellmanford(int x) {
	queue<int> que;
	memset(vis,0,sizeof vis);
	for (int i=2; i<=n; i++) dist[x][i] = 0x3f3f3f3f; //初始化dist数组
	dist[x][1] = 0; vis[1] = 1;
	que.push(1);
	while (!que.empty()) {
		int cur = que.front(); que.pop();
		vis[cur] = 0;
		for (int i=0; i<e[x][cur].size(); i++) {
			int to = e[x][cur][i].to;
			int div = e[x][cur][i].div;
			if (dist[x][to] > dist[x][cur] + div) {
				dist[x][to] = dist[x][cur] + div;
				if (!vis[to]) {
					vis[to] = 1;
					que.push(to);
				}
			}
		}
	}
	return ;
}

int main() {
//	freopen("a.txt","r",stdin);
	int times;
	scanf("%d",&times);
	while (times--) {
		scanf("%d%d",&n,&m);
		int u,v,w;
		for (int i=1; i<=m; i++) {
			scanf("%d%d%d",&u,&v,&w);
			e[0][u].push_back( node(v,w) );
			e[1][v].push_back( node(u,w) );
		}
		bellmanford(1);
		bellmanford(0);
		long long  ans = 0;
		for (int i=2; i<=n; i++) 
			ans += (dist[0][i]+dist[1][i]);
		cout << ans << endl;
		// 清空第一组的数据
		memset(e,0,sizeof e);
	}
	return 0;
}
```
2. dij
   ```cpp
 #include <iostream>
#include <vector>
#include <string.h>
#include <queue>

using namespace std;
const int maxn = 1e6+3;

struct node {
	int to,div;
	node () {};
	node (int v,int w) {
		to = v; div = w;
	}
};
int n,m;
bool vis[maxn];
int dist[2][maxn];
vector<node> e[2][maxn];

void dij(int x) {
	priority_queue<pair<int,int> > que;
	for (int i=2; i<=n; i++) dist[x][i] = 0x3f3f3f3f;
	memset(vis,0,sizeof vis);
	dist[x][1] = 0;
	que.push( make_pair(-dist[x][1],1) );
	while (!que.empty()) {
		int cur = que.top().second; que.pop();
		if (vis[cur]) continue;
		vis[cur] = 1;
		for (int i=0; i<e[x][cur].size(); i++) {
			int to = e[x][cur][i].to;
			int div = e[x][cur][i].div;
			if (dist[x][to] > dist[x][cur] + div) {
				dist[x][to] = dist[x][cur] + div;
				que.push( make_pair(-dist[x][to],to) );
			}
		}
	}
	return ;
}

int main() {
//	freopen("a.txt","r",stdin);
	int times;
	scanf("%d",&times);
	while (times--) {
		scanf("%d%d",&n,&m);
		int u,v,w;
		for (int i=1; i<=m; i++) {
			scanf("%d%d%d",&u,&v,&w);
			e[0][u].push_back( node(v,w) );
			e[1][v].push_back( node(u,w) );
		}
		dij(1);
		dij(0);
		long long  ans = 0;
		for (int i=2; i<=n; i++) 
			ans += (dist[0][i]+dist[1][i]);
		cout << ans << endl;
		// 清空第一组的数据
		memset(e,0,sizeof e);
	}
	return 0;
}
```
