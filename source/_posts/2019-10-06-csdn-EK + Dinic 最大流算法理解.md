---
title: EK + Dinic 最大流算法理解
date: '2019-10-06 00:09:00'
permalink: 2019/10/06/csdn/EK + Dinic 最大流算法理解/
categories:
- 算法与数据结构
- 图论
tags:
- Edmonds-Karp算法 Dinic算法
---

## 网络流常见问题 最大流:

#### 我对残留网的理解：

- 原本**网络**中不存在流,为了求出最大流.**人为的给出一条任意大小流**从 **源点出发**经过一些边**到达汇点**.**且流的大小最后被限制成 经过的边中 容量最小的边**,但是**流具有守恒性,不可能凭空产生？？？**,所以又要从**汇点流回去,所以形成了残留网**

[最大流算法的图解.以及残留网的图,](https://blog.csdn.net/tengweitw/article/details/17766133#commentBox)

### Ford-Fulkerson (方法)

- 是一类计算[网络流](https://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E6%B5%81)的[最大流](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E6%B5%81%E9%97%AE%E9%A2%98)的[贪心算法](https://zh.wikipedia.org/wiki/%E8%B4%AA%E5%BF%83%E7%AE%97%E6%B3%95)。 之所以称之为“方法”而不是“算法”，是因为它寻找增广路径的方式并不是完全确定的，而是有几种不同[时间复杂度](https://zh.wikipedia.org/wiki/%E6%97%B6%E9%97%B4%E5%A4%8D%E6%9D%82%E5%BA%A6)的实现方式

### Edmond-Karp （EK）算法理解

1. 邻接表存储的小技巧: **2点之间的 来回边的下标** `(x->y)`为`i`,那么`(x<-y)`为`i^1`（成对变换）
2. 流程:

- 首先通过`bfs`从**源点**出发 **找到任意一条** **边的容量限制下**可以到达**汇点的路径 (称为增广路)**,且`pre[]`记录一下.
- 通过`pre[]`找到**此次增广路径上 流的大小,**,也就是**路径上的容量最小的边**,累加每次增广路径上的流的大小
- 然后**根据流守恒**把 把图(网络) 更新为 新的图 (残留图).这样流才能守恒
- 直到`bfs`找不到**增广路**了就说明找到了**最大流**

```c
#include <iostream> 
#include <cstring>
#include <algorithm>
#include <queue>

using namespace std;
const int maxn = 505;
const int inf = 0x3f3f3f3f;
const int maxm = 4e4+10;

struct node { int u,v,c,next;} edge[maxm];
int head[maxn],pre[maxn];
int cnt,n,m,source,sink;
bool vis[maxn];

void add(int u,int v,int c) {
    edge[cnt].u = u; edge[cnt].v = v; edge[cnt].c = c;
    edge[cnt].next = head[u]; head[u] = cnt++;

    edge[cnt].u = v; edge[cnt].v = u; edge[cnt].c = 0;
    edge[cnt].next = head[v]; head[v] = cnt++;
}

bool bfs() {
    queue<int> que;
    memset(pre,-1,sizeof pre);
    memset(vis, 0,sizeof vis);
    pre[source]=-1;
    vis[source]=1;
    que.push(source);
    while (!que.empty()) { //通过bfs找到f()>0的增广路
        int cur = que.front(); que.pop();
        for (int i=head[cur]; i!=-1; i=edge[i].next) {
            int to = edge[i].v;
            if (edge[i].c>0 && !vis[to]) {
                pre[to]=i; //记录进入该点的边
                vis[to] = 1;
                if (to==sink) return 1;
                que.push(to);
            }
        }
    }
    return false;
}


int Edmond_Karp() {
    int maxflow = 0;
    int delta;
    while (bfs()) {
        delta=inf;
        int i = pre[sink]; //i点sink点的入边
        while (i!=-1) {// 找到流中的最小边(流量)
            delta = min(delta,edge[i].c);
            i = pre[edge[i].u];
        }
        i = pre[sink]; //重新扫描一些
        while (i!=-1) {
            edge[i].c -= delta;
            edge[i^1].c += delta;
            i = pre[edge[i].u];
        }
        maxflow += delta;
    }
    return maxflow;
}


int main() {
    freopen("1.in","r",stdin);
    while (scanf("%d%d",&n,&m) != EOF) {
        int u,v,w;
        memset(head,-1,sizeof head);
        for (int i=0; i<m; ++i) {
            scanf("%d%d%d",&u,&v,&w);
            add(u,v,w);
        }
        source=1;
        sink=n;
        printf("%d\n",Edmond_Karp());
    }
    return 0;
}
```

#### Dinic算法由来: `bfs`每次只能找到一条增广路效率太低

### Dinic算法

> 背景:在一次增广的过程中想要找到 多条增广路
>
> - 仍用邻接表存储
> - Dinic算法 将 EK算法中的 `bfs`找增广路 **分为** 2步.由`bfs`分层.(源点到它最少要经过的边数).`dfs`从源点开始由**前一层**向**后一层**反复寻找增广路.

- 流程:

  1. `bfs`通过图中的边 将 网络的图 **分层**
  2. 在这次**分层之后**.重复调用`dfs`来找**增广路**.
     - `dfs(int i,int delta)` .`i`表示当前点,**`delta`表示流入该点的流量**
     - `int flow`:表示从**该点已经流出的流量**.
     - `min(delta - flow,edge[i].c)`:**巧妙的解决了: 出边的容量 与 剩下可以流出的流量**来满足增广路的需要.
     - `dfs`回溯时 维护 残留网
     - `dfs`中 `!flow`:**流出的流量=0**. 即 增广路找不到了.`dep[u]==-1`.将该点从该层移出去(`dfs`下次访问不到)
  3. `dfs`找不到**增广路**后.通过`bfs`重新分层. 直到不能**分层为止**

  ### 总结: Dinic就是从每次找一条增广路 变为 在分层基础上由dfs去找多条增广路

```cpp
#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>

using namespace std;
const int maxn = 505;
const int inf = 0x3f3f3f3f;
const int maxm = 4e4+10;

struct node { int u,v,c,next; } edge[maxm];
int n,m,cnt,source,sink;
int head[maxn],dep[maxn];

void add(int u,int v,int c) {
    edge[cnt].u = u; edge[cnt].v = v; edge[cnt].c = c;
    edge[cnt].next = head[u]; head[u] = cnt++;

    edge[cnt].u = v; edge[cnt].v = u; edge[cnt].c = 0;
    edge[cnt].next = head[v]; head[v] = cnt++;
}

int bfs() {
    queue<int> que;
    //while (!que.empty()) que.pop();
    memset(dep,-1,sizeof dep);
    dep[source]=0;
    que.push(source);
    while (!que.empty()) {
        int cur = que.front(); que.pop();
        for (int i=head[cur]; i!=-1; i=edge[i].next) {
            int to = edge[i].v;
            if (edge[i].c>0 && dep[to] == -1) {
                dep[to] = dep[cur] + 1;
                que.push(to);
            }
        }
    }
    return dep[sink] != -1; // 不等于-1说明分层成功
}

int dfs(int u,int delta) {
    if (u == sink)
        return delta;
    int flow=0;
    for (int i=head[u]; i!=-1; i=edge[i].next) {
        int to = edge[i].v;
        if (edge[i].c>0 && dep[to]==dep[u]+1) {
            int temp = dfs(to,min(delta-flow,edge[i].c));
            edge[i].c -= temp;
            edge[i^1].c += temp;
            flow += temp;
        }
    }
    if (!flow) dep[u]=-1;
    return flow;
}

int dinic() {
    int ans=0,temp;
    while (bfs()) { // 分层后通过dfs一次找到多条增广路
        while (1) {
            temp = dfs(1,inf);
            if (!temp) break;
            ans += temp;
        }
    }
    return ans;
}

int main() {
    freopen("1.in","r",stdin);
    while (scanf("%d%d",&m,&n) != EOF) {
        cnt = 0;
        memset(head,-1,sizeof head);
        int u,v,c;
        while (m--) {
            scanf("%d%d%d",&u,&v,&c);
            add(u,v,c);
        }
        source=1;sink=n;
        printf("%d\n",dinic());
    }
    return 0;
}
```

- [最大流例题 POJ 1273](http://poj.org/problem?id=1273)
- `SAP`算法理解 先占坑待解决
- 参考**北京大学暑期课讲义-网络流**
