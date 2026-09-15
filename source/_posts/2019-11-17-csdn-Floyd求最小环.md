---
title: Floyd求最小环
date: '2019-11-17 17:36:00'
permalink: 2019/11/17/csdn/Floyd求最小环/
categories:
- 算法
tags:
- 最小环
---

### Floyd求最小环

#### 原理:

1. 当第三层循环到点`k`时, **所有点之间的最短路只通过`[1,k)`更新**, 记$dis\_{u,v}$是从`u`到`v`且**仅经过**编号在区间$[1,k)$中的点的最短路。
2. **最小环至少要有3个顶点**, 最小环通过**一条最短路**和**枚举一个点的2条边来更新** $ans=min(ans,dis\_{u,v}+g[u][k]+g[k][v])$

#### 算法的疑问?

1. 如果`g[u][k]+g[k][v]`改为`dis[u][k]+dis[k][v]`错误: **因为`u`到`v`的最短路可能会重复，不成环,只能用边来枚举**
2. 至少有三个点,所以三层循环`i!=j`

[POJ 1734](http://poj.org/problem?id=1734)

- `path`记录路径
- `pre[i][j]`记录：**最短路径中`j`点的上一个点是谁**

```c
#include <cstring>
#include <stdio.h>
#include <iostream>
#include <algorithm>
using namespace std;
const int maxn = 110;
const int inf  = 9999999;
int n,m,tot;
int g[maxn][maxn],dis[maxn][maxn];
int pre[maxn][maxn],path[maxn];

int main() {
    cin >> n >> m;
    for (int i=1; i<=n; ++i)
        for (int j=1; j<=n; ++j) {
            g[i][j] = dis[i][j] = inf;
            pre[i][j] = i;
        }
    for (int i=1; i<=m; ++i) {
        int u,v,w;
        cin >> u >> v >> w;
        g[u][v] = g[v][u]= dis[u][v] = dis[v][u] = min(g[u][v],w);
    }
    int ans = inf;
    for (int k=1; k<=n; ++k) {
        for (int i=1; i<k; ++i)
            for (int j=i+1;j<k; ++j) {
                int temp = dis[i][j] + g[i][k] + g[k][j];
                if (temp < ans) {
                    ans = temp;
                    tot = 0;
                    int p = j;
                    while (p != i) {
                        path[tot++] = p;
                        p = pre[i][p];
                    }
                    path[tot++] = i;
                    path[tot++] = k;
                }
            }

        for (int i=1; i<=n; ++i)
            for (int j=1; j<=n; ++j)
                if (dis[i][j] > dis[i][k] + dis[k][j]) {
                    dis[i][j] = dis[i][k] + dis[k][j];
                    pre[i][j] = pre[k][j];
                }
    }
    if(ans==inf)
        cout << "No solution." << endl;
    else {
        for (int i=0; i<tot; ++i)
            cout << path[i] << " ";
        cout << endl;
    }
    return 0;
}
```
