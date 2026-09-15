---
title: Tarjan求割边 + UVA 796
date: '2019-08-14 15:48:00'
permalink: 2019/08/14/csdn/Tarjan求割边 + UVA 796/
categories:
- 算法
---

- 割点去除后生成`>=2`的子图
- `dfs`遍历的无向图每个点一次所组成的树就是搜索树

  ### 割边

  从无向图删除边`e`之后,`G`分裂成2个不相连的子图.称`e`是图`G`的**桥**或者**割边**
- 割去除后生成`2`个子图

  ### 割边判定法则

1. 当且仅当搜索树存在`x`的一个子节点`y`,**满足`dfn[x] < low[y]`**
   > `low[y] > dfn[x]`说明:`y`点及其子树的所有点 **能访问到的搜索树中最早的点比`x`点还晚**,那么就是**不能通过`(x,y)`这条边**,如果**删除(x,y)这条边**,`y`点这部分必然是一个独立的子图或者(`y`一个点也算图)
2. 由于无向图是`2`条有向边.在`Tarjan()`更新`low[]与dfn[]`关系时,要去掉**父节点**

   #### 但是可能2点之间存在重边,它们中只有一条在搜索树上.这些不在搜索树上的`2`点间的重边,仍可以用来更新`low[]与dfn[]`的关系

- 需要用一个方法既能**解决重边,也能标记父亲节点**

  ### 记录递归进入每个节点的边的编号.编号处理成邻接表的下标
- 运用**成对变换**的技巧.即双向边按照下标`2`和`3`. `4`和`5`存入邻接表
- 通过异或直接找到反向边:`2^1=3` 并且 `3^1=2`.这样就能除去与父节点连接的边而不影响与父节点之间的重边

例题:[UVA 796](https://cn.vjudge.net/problem/UVA-796)

```arduino
#include <iostream>
#include <string.h>
#include <algorithm>
using namespace std;
	
const int maxn = 1e5 + 10;
int head[maxn], next1[maxn << 1], ver[maxn << 1];
int dfn[maxn], low[maxn];
int n,tot,num;
bool bridge[maxn << 1];

void edgeadd(int x,int y) {
	ver[++tot] = y; next1[tot] = head[x]; head[x] = tot;
}
void tarjan(int x,int in_edge) {
	dfn[x] = low[x] = ++num;
	for (int i = head[x]; i; i = next1[i]) {
		int y = ver[i];
		if (!dfn[y]) {
			tarjan(y, i);
			low[x] = min(low[x], low[y]);

			if (low[y] > dfn[x]) {
				bridge[i] = bridge[i ^ 1] = 1;
			}
		}
		else if (i != (in_edge ^ 1))
			low[x] = min(dfn[y],low[x]);
	}
}
void init() {
	tot = 1; num = 0;

	memset(low,0,sizeof low);
	memset(dfn,0,sizeof dfn);

	memset(head, 0, sizeof head); 
	memset(next1, 0, sizeof next1);
	memset(ver,0,sizeof ver);

	memset(bridge,0,sizeof bridge);
}
int main() {
//	freopen("a.txt","r",stdin);
	while (~scanf("%d",&n)) {
		init();
		if (n == 0) {
			printf("0 critical links\n\n");
			continue;
		} 
		for (int i = 1; i <= n; i++) {
			int cur, cnt;
			scanf("%d (%d)",&cur,&cnt); 
			cur++;
			for (int j = 1; j <= cnt; j++) {
				int to; scanf("%d", &to); 
				to++;
				if (to <= cur) continue;
				edgeadd(cur, to); 
				edgeadd(to,cur);
			}
		}
		for (int i = 1; i <= n; i++)
			if (!dfn[i]) tarjan(i,0);
		int ans = 0;
		for (int i = 2; i < tot; i+=2) //邻接表存边从2开始
			if (bridge[i]) ans++;
	
		printf("%d critical links\n",ans);
		for (int i = 2; i < tot; i += 2) 
			if (bridge[i]) printf("%d - %d\n",ver[i^1] - 1,ver[i] - 1);
		printf("\n");
	}
	return 0;
}
```
