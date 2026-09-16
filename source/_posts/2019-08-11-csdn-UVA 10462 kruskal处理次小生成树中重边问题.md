---
title: UVA 10462 kruskal处理次小生成树中重边问题
date: '2019-08-11 09:32:00'
permalink: 2019/08/11/csdn/UVA 10462 kruskal处理次小生成树中重边问题/
categories:
- 算法与数据结构
- 图论
tags:
- 次小生成树重边问题
---

[UVA 10462](https://cn.vjudge.net/problem/UVA-10462)

- ~~prim实在是好难理解如何处理重边,看了6小时的blog没看明白~~
- `kruskal`原理就是将所有的边排序,然后从小到大处理,正好也将重边给排序了,所有适合处理这个问题
- 每条边存`uesd,del`变量,`used`代表第一次跑出生成树的结果,`del`代表这条边是否删去
- 第一次跑完kruskal后,枚举每一条在生成树的边,删除,然后标记(使得下次跑kruskal不在加入到生成树中).在跑一次kruskal,更新次小生成树的值,直到第一次跑出来的生成树的所有边都被枚举到.

```arduino
#include <iostream>
#include <algorithm>
#include <string.h>
using namespace std;
const int inf = 0x3f3f3f3f;
const int maxn = 205;
struct node {
	int u, v, w;
	bool del, used;
	bool operator<(const node& temp)const {
		return w < temp.w;
	}
}e[maxn];

int n, m, cnt;
bool flag;
int pre[105];

void init() {
	for (int i = 1; i <= n; i++) pre[i] = i;
}
int find(int p) {
	if (p == pre[p]) return p;
	else return pre[p] = find(pre[p]);
}

int kruskal() {
	int sum = 0, num = 0;
	init();
	for (int i = 0; i < m; i++) {
		if (e[i].del) continue;
		int p = find(e[i].u);
		int q = find(e[i].v);
		if (p != q) {
			sum += e[i].w;
			pre[p] = q;
			if (!flag) e[i].used = 1;
			num++;
		}
		if (num >= n - 1) break;
	}
	if (num >= n - 1) return sum;
	else return inf;
}
int main() {
//	freopen("a.txt","r",stdin);
	int times; cin >> times; int k = 1;
	while (times--) {
		scanf("%d%d",&n,&m);
		for (int i = 0; i < m; i++) {
			scanf("%d%d%d",&e[i].u,&e[i].v,&e[i].w);
			e[i].del = e[i].used = false;
		}
		sort(e,e+m);
		flag = false;
		int mst = kruskal();
		flag = 1;
		int minn = inf;
		for (int i = 0; i < m; i++) {
			if (e[i].used) {
				e[i].del = 1;
				minn = min(minn,kruskal());
				e[i].del = 0;
			}
		}
		printf("Case #%d : ",k++);
		if (mst == inf) printf("No way\n");
		else if (minn == inf) printf("No second way\n");
		else printf("%d\n",minn);
	}
	return 0;
}
```

### 这是一份处理重边的Prim算法,没看懂如何求次小生成时处理重边的方法

```arduino
#include <iostream>
#include <algorithm>
#include <string.h>
#include <vector>

using namespace std;
const int maxn = 1e3+5;
const int inf = 0x3f3f3f3f;

int dist[maxn], e[maxn][maxn],pre[maxn],maxdist[maxn][maxn],use[maxn][maxn];
bool vis[maxn];
vector<pair<int, int>> edge[maxn];
int n, m;

int prim() {
	memset(dist, inf, sizeof dist); memset(vis,0,sizeof vis);
	dist[1] = 0; int ans = 0;
	for (int i = 1; i <= n; i++) { 
		int minn = inf, point = -1;
		for (int j = 1; j <= n; j++) 
			if (!vis[j] && minn > dist[j]) { minn = dist[j]; point = j; }
		if (point == -1) return -1; //判断是否存在最小生成树
		vis[point] = 1; ans += dist[point];
		for (int j = 1; j <= n; j++)
			if (vis[j])
				maxdist[point][j] = maxdist[j][point] = j == point ? 0 : max(maxdist[pre[point]][j], dist[point]);
			else if (dist[j] > e[point][j]) //更新不在书上的点,到树的距离
				dist[j] = e[point][j], pre[j] = point;
	}
	return ans;
}
int check(int sum) {
	int ans = inf;
	for (int u=1; u<=n; u++) 
		for (int i = 0; i < edge[u].size(); i++) {
			int v = edge[u][i].first, w = edge[u][i].second;
			// pre[v] != u && pre[u] != v 说明这2个点是树上(间隔超过1条边)的点,且之间还存在边
			// e[u][v]!= w 树中的一条边的重边,
			// use[][]说明2个点在树上,且用的还最小边,用来更新最小值
			if ((pre[v] != u && pre[u] != v) || e[u][v] != w || use[u][v])
				ans = min(ans,sum - maxdist[u][v] + w);
			if ((pre[v] == u || pre[u] == v) && e[u][v] == w) //标记在生成树中的点
				use[u][v] = use[v][u] = 1;
		}
	return ans;
}
int main() {
	//freopen("a.txt","r",stdin);
	int times; cin >> times;
	for (int casei = 1; casei <= times; casei++) {
		memset(e, inf, sizeof e); memset(use,0,sizeof use);
		scanf("%d%d",&n,&m);
		for (int i = 1; i <= m; i++) {
			int u, v, w; scanf("%d%d%d",&u,&v,&w);
			e[u][v] = e[v][u] = min(e[u][v],w);
			if (u > v) swap(u,v);
			edge[u].push_back(make_pair(v,w));
		}
		printf("Case #%d : ",casei);
		int ans = prim();
		if (ans == -1) printf("No way\n");
		else {
			ans = check(ans);
			ans == inf ? printf("No second way\n") : printf("%d\n",ans);
		}
		for (int i = 1; i <= n; i++) 
			edge[i].clear();
	}
	return 0;
}
```
