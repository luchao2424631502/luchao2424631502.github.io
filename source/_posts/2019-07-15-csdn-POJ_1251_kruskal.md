---
title: POJ_1251_kruskal
date: '2019-07-15 15:11:00'
permalink: 2019/07/15/csdn/POJ_1251_kruskal/
categories:
- 算法
tags:
- kruskal
---

[POJ 1251](http://poj.org/problem?id=1251)

- 处理输入输出格式+kruskal
  ```cpp
#include <iostream>
#include <algorithm>

using namespace std;
const int maxn = 100;

int n;
struct node {
	int from,to,div;
	node () {}
	node (int u,int v,int w) {
		from = u; to = v; w = div;
	}
	bool operator<(const node& temp) const{
		return this->div < temp.div;
	}
}e[maxn];
int pre[maxn];

int find(int x) {
	if (x == pre[x]) return x;
	else return pre[x] = find(pre[x]);
}

int main() {
//	freopen("a.txt","r",stdin);
	while (scanf("%d",&n) && n) {
		int cnt = 0;
		for (int i=1; i<=n; i++) pre[i] = i;
		for (int i=1; i<=n-1; i++) {
			char ch; int k;
			scanf("\n%c %d",&ch,&k);
			int cur = ch - 'A' + 1;
			for (int j=1; j<=k; j++) {
				int to,div;
				scanf(" %c %d",&ch,&div);
				to = ch - 'A' + 1;
				e[cnt].from = cur; e[cnt].to = to; e[cnt].div = div;
				cnt++;
			}
		}
		sort(e,e+cnt);
		int ans = 0;
		for (int i=0; i<cnt; i++) {
			int from = e[i].from;
			int to = e[i].to;
			if ( find(from) != find(to) ) {
				ans += e[i].div;
				pre[find(from)] = find(to);
			}
		}
		cout << ans << endl;
	}
	return 0;
}
```
