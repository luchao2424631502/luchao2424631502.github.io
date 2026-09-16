---
title: BZOJ 1123 无向图割点_Tarjan
date: '2019-08-14 17:58:00'
permalink: 2019/08/14/csdn/BZOJ 1123 无向图割点_Tarjan/
categories:
- 算法与数据结构
- 图论
tags:
- 割点
---

[BZOJ 1123](https://www.lydsy.com/JudgeOnline/problem.php?id=1123)

### 题意

给出一个无向图,`n`个点`m`条边,输出`n`个整数.第`i`个整数表示把节点`i`关联的所有边去掉后**无向图中有多少个有序对`(x,y)`,满足x和y不联通**

### 思路

1. 去掉**非割点,那么整个图分为成了1个点和(n-1)个点组成的连通图**,**有序对指的是双向:**`(x,y),(y,x)`.此时答案`=2*(n-1)`
2. 去掉**割点**.那么至少会被分成`3`块连通图,

- 割点自身
- 割点的子节点`s1,s2,...`可能有多个点满足`low[y]>=dfn[x]`.那么子节点集合可能被分成多个联通块.
- 割点上方的联通块

3. 由于要统计有序对个数.在`tarjan()`遍历时就要**统计每个子树的节点个数`Size[]`**

   ### 统计有序对个数

- 有序对是有方向的.

  #### **统计每个联通块出发到其余点的单向的对数**

1. 割点的子节点的联通块点集  
   `$Size[s_1]*(n-Size[s_1])+Size[s_2]*(n-Size[s_2]+.....)$`
2. 割点自身  
   `$1*(n-1)$`
3. 割点上方的联通块点集.(总数-割点-割点子节点数量)  
   `$(n - 1 - \Sigma_{k=1}^{t}Size[s_k])*(1+\Sigma_{k=1}^{t}Size[s_k])$`

- 这样就组成了**一个割点的所有有序对**.

```gml
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <algorithm>
#define ll long long 
using namespace std;
const int maxn = 1e5 + 10;
const int maxm = 5e5 + 10;

int head[maxn], ver[maxm << 1], next1[maxm << 1];
int dfn[maxn], low[maxn], Size[maxn];
ll ans[maxn];
bool cut[maxn];
int n, m, tot, num;

void add(int x,int y) {
	ver[++tot] = y; next1[tot] = head[x]; head[x] = tot;
}

void tarjan(int x) {
	dfn[x] = low[x] = ++num; Size[x] = 1;
	int flag = 0, sum = 0;
	for (int i = head[x]; i; i = next1[i]) {
		int y = ver[i];
		if (!dfn[y]) {
			tarjan(y);
			low[x] = min(low[x],low[y]);
			Size[x] += Size[y];
			if (low[y] >= dfn[x]) {
				flag++;
				ans[x] += (ll)Size[y] * (n - Size[y]); //子树的联通块出发的有序对个数
				sum += Size[y]; //sum用来统计该节点子树的联通块大小
				if (x != 1 || flag > 1) cut[x] = 1;//标记割点
			}
		}
		else
			low[x] = min(low[x],dfn[y]);
	}
	if (cut[x]) //求出从 根节点上面的联通块出发的有序对 和 根节点出发的有序对
		ans[x] += (ll)(n - 1 - sum) * (sum + 1) + (n - 1);
	else ans[x] = 2 * (n - 1); //不是割点,该点和另一个联通块相互出发,
}

int main() {
//	freopen("a.txt","r",stdin);
	cin >> n >> m; tot = 1;
	for (int i = 1; i <= m; i++) {
		int x, y; scanf("%d%d",&x,&y);
		if (x == y) continue;
		add(x, y); add(y,x);
	}
	tarjan(1);
	for (int i = 1; i <= n; i++)
		printf("%lld\n",ans[i]);
	return 0;
}
```
