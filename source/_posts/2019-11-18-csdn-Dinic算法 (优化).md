---
title: Dinic算法 (优化)
date: '2019-11-18 20:11:00'
permalink: 2019/11/18/csdn/Dinic算法 (优化)/
categories:
- 算法与数据结构
- 图论
tags:
- 最大流 最小割
---

## Dinic 算法(优化)

##### 前言: (个人而言)

1. `dfs_test()`是 **我以前学然后写`Dinic`中的`dfs`用来增广**
2. 新的`dfs()`速度比原来快很多

   1. 判断 **向下增广返回的流是否为0**
   2. **返回的流**不为0代表增广成功 维护边后**直接回溯**
   3. 原来的`dfs_test`**处于一个点时 : 只要所有出边遍历结束才回溯**,

---

### 优化

1. **当前弧优化** :

> 1. 原来的dfs都是**从每个点的第一条边开始遍历**,**导致已经增广过的边会被重复dfs**
> 2. 开一个`cur[]`**记录每一个点当前增广到的边,当其他的dfs增广到的时候,从有效的边开始增广**,
>
> - `bfs`**分层后初始化`cur[]`, 即`head[]`每个点的第一条边**,

2. 分层优化(**说法不一,其他blog学习到的,下同**): `bfs`分层时找到汇点直接退出
3. 剩余量优化: **用不到我新学的`dfs`上, 但是原来的`dfs_test`可以优化**

---

### 需要Dinic优化才能过 且 建图巧妙 [luogu P1361 最小割](https://www.luogu.org/problem/P1361)

- 转化为最小割问题模型 | [建图方法NB](https://www.luogu.org/problemnew/solution/P1361)

1. 源点$s \in S$,源点和每个点连边代表在$S$部分的收益, 同理汇点$t \in T$,每个点和汇点连边代表处于$T$部分的收益
2. **建虚点** 处理**部分点所在的点集处于图的2个部分的额外收益**：

   > 1. 点集看做2个点,在$S$部分时, **源点向虚点 连边且边权代表额外收益,**
   > 2. 如何处理,**点集中任意一个点不在此集合中会额外收益也消失**
   > 3. **虚点连向点集中每个点一条边权为无穷的边**,
   > 4. 当点集中的点被割到另一集合中时,这条`inf`的边使得**源点和虚点的边（额外收益）的边也被割掉**

```java
#include <bits/stdc++.h>
using namespace std;
const int maxn = 3010;
const int maxm = 2e6+5;
const int inf  = 0x3f3f3f3f;
struct Edge {
    int v,c,next;
} edge[maxm];

int n,m,tot,source,sink,cnt;
int head[maxn],dep[maxn],cur[maxn];

void add(int u,int v,int c) {
    edge[tot].v=v; edge[tot].c=c;
    edge[tot].next=head[u]; head[u]=tot++;
}
void addedge(int u,int v,int c) {
    add(u,v,c);
    add(v,u,0);
}

bool bfs() {
    queue<int> que;
    memset(dep,-1,sizeof dep);
    dep[source] = 0;
    que.push(source);
    while (!que.empty()) {
        int u = que.front(); que.pop();
        for (int i=head[u]; i!=-1; i=edge[i].next) {
            int to = edge[i].v;
            if (edge[i].c>0 && dep[to] == -1) {
                dep[to] = dep[u] + 1;
                que.push(to);
                // 找到汇点直接退出 优化2
                if (to == sink) return 1;
            }
        }
    }
    return dep[sink] != -1;
}

int dfs(int u,int dist) {
    if (u == sink)
        return dist;
    for (int &i=cur[u]; i!=-1; i=edge[i].next) { // 通过引用更新cur[]:记录每个点当前增广的边
        int to = edge[i].v;
        if (edge[i].c>0 && dep[to]==dep[u]+1) {
            int temp = dfs(to,min(dist,edge[i].c));
            if (temp > 0) {
                edge[i].c -= temp;
                edge[i^1].c += temp;
                return temp;
            }
        }
    }
    return 0;
}

int dfs_test(int u,int delta) {
    if (u == sink)
        return delta;
    int flow = 0;
    for (int &i=cur[u]; i!=-1; i=edge[i].next) {
        int to = edge[i].v;
        if (edge[i].c>0 && dep[to]==dep[u]+1) {
            int temp = dfs(to,min(delta-flow,edge[i].c));
            edge[i].c   -= temp;
            edge[i^1].c += temp;
            flow += temp;
            // 没有流量就打破循环 优化3
            if (delta-flow <= 0) break;
        }
    }
    if (!flow) dep[u] = -1;
    return flow;
}

int Dinic() {
    int ans = 0;
    while (bfs()) { 
        for (int i=0; i<cnt; ++i) // 分层后每个点当前增广到的边当然是第一条边
            cur[i] = head[i];
        while(1) {
            int temp = dfs(source,inf);
            //int temp = dfs_test(source,inf);
            if (!temp) break;
            ans += temp;
        }
    }
    return ans;
}

int main() {
    memset(head,-1,sizeof head);
    scanf("%d",&n);
    source = 0;
    sink = n+1;
    int tot_val = 0;
    for (int i=1; i<=2*n; ++i) {
        int val; scanf("%d",&val);
        tot_val += val;
        if (i <= n) {
            addedge(source,i,val);
        } else {
            addedge(i-n,sink,val);
        }
    }
    scanf("%d",&m);
    cnt = sink+1;
    for (int i=1; i<=m; ++i) {
        int k,c1,c2,to;
        //cin >> k >> c1 >> c2;
        scanf("%d%d%d",&k,&c1,&c2);
        tot_val += (c1+c2);
        addedge(source,cnt++,c1);
        addedge(cnt++, sink, c2);
        while (k--) {
            //cin >> to;
            scanf("%d",&to);
            addedge(cnt-2,to,inf);
            addedge(to,cnt-1,inf);
        }
    }
    int maxflow = Dinic();
    //cout << tot_val-maxflow << endl;
    printf("%d\n",tot_val - maxflow);
    return 0;
}
```
