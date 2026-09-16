---
title: Dijkstra_最短路模板
date: '2019-06-01 15:38:00'
permalink: 2019/06/01/csdn/Dijkstra_最短路模板/
categories:
- 算法与数据结构
- 图论
tags:
- dij
---

#### dij 原理, ~~总是容易和最小生成树搞混~~

- dij求的是 ***源点到每个点的最短距离***
- 所以会更新一个`dist[]`的距离表,代表选定源点到每一个点的最短距离
- 每次通过选出来的**点的出边**来**松弛** **出边指向的点**到**源点**的距离,同时将**松弛后的边**加入到优先队列中 来找到 **出边指向的点中**距离源点最近的点
- 不断重复上一步,直到所有点都标记了
- **松弛**意思就是更新**出边指向的点**到源点的距离,(因为**此轮选的点到源点的距离**已经是最短的,)
  `````prolog
if (div + dist[cur] < dist[to]) 
	dist[to] = div + dist[cur];
````

1. [POJ 2387](http://poj.org/problem?id=2387)邻接矩阵存图
* 数据会出现 **重边**,选取最小的距离
`````
  #include   
  #include <string.h>  
  #include   
  #include   
  using namespace std;  
  const int maxn = 1001;

// vector<pair<int,int>> e[maxn];  
int e[maxn][maxn];  
int dist[maxn];  
bool vis[maxn];  
int t,n;

void dij() {  
 memset(dist,0x3f,sizeof dist);  
 dist[1] = 0;  
 priority\_queue<pair<int,int>> que;  
 que.push(make\_pair( -dist[1],1) );  
 while ( !que.empty() ) {  
 int cur = que.top().second;  
 que.pop();  
 if (vis[cur]) continue;  
 vis[cur] = 1;  
 for (int i=1; i<=n; i++) {  
 int to = i;  
 int div = e[cur][i];  
 if (div + dist[cur] < dist[to]) {  
 dist[to] = div + dist[cur];  
 que.push(make\_pair(-dist[to],to));  
 }  
 }  
 }  
 cout << dist[n];  
}  
void read() {  
// freopen(“a.txt”,”r”,stdin);  
 cin >> t >> n;  
 memset(e,0x3f,sizeof e);  
 for (int i=1; i<=t; i++) {  
 int a,b,c;  
 cin >> a >> b >> c;  
 // e[a].push\_back( make\_pair(b,c) );  
 if (c < e[a][b] || c < e[b][a])  
 e[a][b] = e[b][a] = c;  
 }  
}  
int main() {  
 read();  
 dij();  
 return 0;  
}

```markdown
2. 邻接表存图
```

#include   
#include <string.h>  
#include   
#include   
using namespace std;  
const int maxn = 1001;

vector<pair<int,int>> e[maxn];  
int dist[maxn];  
bool vis[maxn];  
int t,n;

void dij() {  
 memset(dist,0x3f,sizeof dist);  
 dist[1] = 0;  
 priority\_queue<pair<int,int>> que;  
 que.push(make\_pair( -dist[1],1) );  
 while ( !que.empty() ) {  
 int cur = que.top().second;  
 que.pop();  
 if (vis[cur]) continue;  
 vis[cur] = 1; // 取出 一个最短的点 标记 或者 判断  
 for (int i=0; i<e[cur].size(); i++) {  
 int to = e[cur][i].first;  
 int div = e[cur][i].second;  
 if (div + dist[cur] < dist[to]) {  
 dist[to] = div + dist[cur];  
 que.push(make\_pair(-dist[to],to)); // 松弛此轮点周围的点  
 }  
 }  
 }  
 return ;  
}  
void read() {  
 // freopen(“a.txt”,”r”,stdin);  
 cin >> t >> n; // t 边数, n 点的编号数  
 for (int i=1; i<=t; i++) {  
 int a,b,c;  
 cin >> a >> b >> c;  
 e[a].push\_back( make\_pair(b,c) ); // 有向图  
 }  
}

int main() {  
 read();  
 dij();  
 return 0;  
}

```

```
