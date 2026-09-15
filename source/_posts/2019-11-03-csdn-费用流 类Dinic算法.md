---
title: 费用流 类Dinic算法
date: '2019-11-03 15:53:00'
permalink: 2019/11/03/csdn/费用流 类Dinic算法/
categories:
- 算法
tags:
- 费用流
---

### 费用流类Dinic算法

- 因为**费用**有**负边权**所以用`spfa`，求**单位费用之和最小的路径**
- 将`bfs`分层标记`dep`数组 **换成** `spfa`分层标记`dist[](最小费用和)`
- `dfs`寻找多条增广路时, 开`vis`标记筛掉**返回的边** ,且**增广路顺着`spfa`标记的最小费用和路径走**,
- `dfs`维护**流和费用**

---

[Luogu P4016](https://www.luogu.org/problem/P4016)

##### 注意:

1. 环形,
2. 最终`n`个仓库存货量相同,
3. 只能在相邻的仓库之间搬运

##### 建图

- 将**流量**看做**在仓库之前转移货物数量的个数**,
- 建立**超级源点和超级汇点**
- `x = 每个仓库当前存货量 - 最后平均的存货量`

  1. `x>0` 说明当前仓库存货 比最后 **多** 一部分储存货物, **转化成网络中源点到该点的边的流量,且单位货物的费用=0**
  2. `x<0`说明当前仓库存货 比最后 **少**一部分存储货物 ,**该点到汇点的边的流量所缺的货物,且单位货物的费用=0**
  3. 相邻`2`个点之间 **建 流量为inf 且 单位费用为1**的边,

  ---

  - **流量为inf**是因为,**源点的出边和汇点的入边**的流量已经**限制了整个网络中的流量**
  - **单位货物费用为1**是将**搬运量转化为费用**
- 注意一下环

```c
#include <bits/stdc++.h>
using namespace std;
const int maxn = 105;
const int maxm = 1e5;
const int inf = 0x3f3f3f3f;

struct Edge {
    int v,c,next,cost;
} edge[maxm];
int n,tot,sink,source,mincost;
int num[maxn],x[maxn];
int head[maxn],dep[maxn];

void add(int u,int v,int c,int cost) {
    edge[tot].v=v; edge[tot].c=c;
    edge[tot].cost=cost; edge[tot].next=head[u]; head[u]=tot++;
}
void addedge(int u,int v,int c,int cost) {
    add(u,v,c,cost);
    add(v,u,0,-cost);
}

int dist[maxn],pre[maxn];
bool vis[maxn];

bool spfa() {
    queue<int> que;
    memset(dist,inf,sizeof dist);
    memset(vis,0,sizeof vis);
    dist[source] = 0;
    que.push(source);
    while (!que.empty()) {
        int cur = que.front(); que.pop();
        vis[cur] = 0;
        for (int i=head[cur];i!=-1;i=edge[i].next) {
            int to = edge[i].v;
            if (edge[i].c>0 && dist[to]>dist[cur]+edge[i].cost) {
                dist[to] = dist[cur] + edge[i].cost;
                if (!vis[to]) {
                    vis[to] = 1;
                    que.push(to);
                }
            }
        }
    }
    return dist[sink]!=inf;
}

int dfs(int u,int delta) {
    if (u == sink)
        return delta;
    vis[u] = 1;
    int flow = 0;
    for (int i=head[u];i!=-1;i=edge[i].next) {
        int to = edge[i].v;
        if (!vis[to] && edge[i].c>0 && dist[to]==dist[u]+edge[i].cost) {
            int temp = dfs(to,min(delta-flow,edge[i].c));
            if (temp) { // 还有流可以走
                mincost += (edge[i].cost * temp);
                edge[i].c -= temp;
                edge[i^1].c += temp;
                flow += temp;
            }
        }
    }
    vis[u] = 0; //回溯取消标记,想要一次寻找多条增广路
    return flow;
}


int Dinic() {
    int maxflow=0;
    while (spfa()) {
        while (1) {
            int temp = dfs(source,inf);
            if (!temp) break;
            maxflow += temp;
        }
    }
    return maxflow;
}

int main() {
    memset(head,-1,sizeof head);
    cin >> n;
    int avg = 0;
    for (int i=1; i<=n; ++i) {
        cin >> num[i];
        avg += num[i];
    }
    avg = avg / n;
    source = 0; sink = n+1;
    for (int i=1; i<=n; ++i) x[i] = num[i] - avg;
    for (int i=1; i<=n; ++i) {
        if (x[i] > 0)
            addedge(source,i,x[i],0);
        if (x[i] < 0)
            addedge(i,sink,-x[i],0);
    }
    for (int i=1; i<=n; ++i) {
        if (i!=1)
            addedge(i,i-1,inf,1);
        if (i!=n)
            addedge(i,i+1,inf,1);
    }
    addedge(1,n,inf,1);
    addedge(n,1,inf,1);
    int maxflow = Dinic();
    //cout << maxflow << endl;
    cout << mincost << endl;
    return 0;
}
```
