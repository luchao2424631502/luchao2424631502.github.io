---
title: Tarjan求割点原理 + UVA 315
date: '2019-08-14 13:29:00'
permalink: 2019/08/14/csdn/Tarjan求割点原理 + UVA 315/
categories:
- 算法
tags:
- 割点板子
---

### 割点

无向图中.**删去节点`x`,及其所有与`x`关联的边后.分成2个及以上的不相连的子图.则称`x`是图的割点**

- 搜索树:`dfs`遍历无向图的访问的顺序.每个点只遍历了一次,生成的树

  ### 割点判定法则

1. **x不是搜索树的根节点,且存在`y`是`x`的子节点**.

- 满足`low[y]>=dfn[x]`

> 说明从`y`或`y`子树出发的点能访问到的最早的点只能达到`x点(low[y]==dfn[x])`,不能到达`dfs`访问更早的点.这说明`x->y`这部分存在一条边或者一个环.

- 因为此时`x`不是根节点.在搜索树中`x`还有入边,还有比`x`被访问到的更早的点(说明`x`入边这里存在一个点或者一个联通分量).
- 所以此时只要有一条满足`low[y]>=dfn[x]`,`x`就是割点,必然能割出2个子图来

2. **`x`是根节点.`x`点在搜索树中不存在入边,那么肯定要有`2`个满足`low[y]>=dfn[x]`的子节点`y`才能割出2个及以上的子图**

---

例题[UVA 315](https://cn.vjudge.net/problem/UVA-315#author=dream2017)

```arduino
#include <iostream>
#include <string.h>
#include <algorithm>
using namespace std;
const int maxn = 1e5 + 10;

int head[maxn], ver[maxn << 1], next1[maxn << 1];
int dfn[maxn], low[maxn];
int n, m, tot, num, root;
bool cut[maxn];

void init() {
	tot = 0; num = 0; 
	memset(cut,0,sizeof cut);
	
	memset(head,0,sizeof head);
	memset(ver,0,sizeof ver);
	memset(next1,0,sizeof next1);
	
	memset(low,0,sizeof low);
	memset(dfn,0,sizeof dfn);
	
}
void edgeadd(int x,int y) { // <= tot
	ver[++tot] = y; next1[tot] = head[x]; head[x] = tot;
}
void tarjan(int x) {
	dfn[x] = low[x] = ++num;
	int out = 0;
	for (int i = head[x]; i; i = next1[i]) {
		int to = ver[i];
		if (!dfn[to]) { //to没有被访问
			tarjan(to);
			low[x] = min(low[x],low[to]); //回溯时更新由子节点更新low
			//割点存在条件: low[to]>=dfn[x] 说明:to(x的子节点)最多只能访问到x节点.
			if (low[to] >= dfn[x]) {
				out++;
				//如果是x是根节点,要有2个to(子节点)能访问到自身或者x,才能算割点
				//如果只有一个,那么根节点没有入边,删除根节点和指向to的边,仍然只有1个连通分量
				if (x != root || out > 1) { //x不是根节.那么x还有入边,入边那边还有点(连通分量).只有有一个就能构成割点.因为x
					cut[x] = 1;
				}
			}	
		}
		else //说明下个节点已经被访问.这条边构成了环
				low[x] = min(low[x],dfn[to]);
	}
}
int main() {
	int n;
//	freopen("a.txt", "r", stdin);
	while (scanf("%d", &n) && n) {
		int cur, to; 
		init();
		while (scanf("%d", &cur) && cur) {
			while (getchar() != '\n') { 
				scanf("%d", &to);
				if (cur == to) continue;
				edgeadd(cur,to); edgeadd(to,cur);
			}
		}
		for (int i = 1; i <= n; i++)
			if (!dfn[i]) root = i, tarjan(i);
		int ans = 0;
		for (int i = 1; i <= n; i++)
			if (cut[i]) ans++;
		printf("%d\n",ans);
	}
	return 0;
}
```
