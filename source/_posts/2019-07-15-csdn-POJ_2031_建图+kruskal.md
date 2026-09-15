---
title: POJ_2031_建图+kruskal
date: '2019-07-15 17:04:00'
permalink: 2019/07/15/csdn/POJ_2031_建图+kruskal/
categories:
- 算法
tags:
- kruskal
---

[POJ 2031](http://poj.org/problem?id=2031)

- 思路:先将每个点位置都存起来,然后给每个点建边,**2个球的半径超过圆心之间的距离就边为0**,否则边就是**圆表面之间的距离**
- kruskal

```cpp
#include <iostream>
#include <algorithm>
#include <math.h>
using namespace std;
const int maxn = 1e4;

int n,m;
struct edge {
	double x,y,z,r;
	edge(){}
	edge(double a,double b,double c,double d) {
		x = a; y = b; z = c; r = d;
	}
} edges[maxn];
struct node {
	int from,to;
	double div;
	node () {}
	node (int u,int v,double w) {
		from = u; to = v; div = w;
	}
	bool operator<(const node& temp)const {
		return this->div < temp.div;
	}
}e[maxn];
int pre[maxn];

int find(int x) {
	if (x == pre[x]) return x;
	else return pre[x] = find(pre[x]);
}
double Distance(edge& a,edge& b) {
	double dx = (a.x-b.x)*(a.x-b.x);
	double dy = (a.y-b.y)*(a.y-b.y);
	double dz = (a.z-b.z)*(a.z-b.z);
	return sqrt(dx+dy+dz);
}
int main() {
//	freopen("a.txt","r",stdin);
	while (scanf("%d",&n) && n) {
		double x,y,z,r;
		for (int i=0; i<n; i++) {
			cin >> x >> y >> z >> r;
			edges[i] = edge(x,y,z,r);
		}
		int cnt = 0;
		for (int i=0; i<n; i++) {
			for (int j=0; j<n; j++) {
				double dis = Distance(edges[i],edges[j]);
				if (dis <= edges[i].r + edges[j].r) {
					e[cnt++] = node(i,j,0);		
				} else {
					e[cnt++] = node(i,j,dis - edges[i].r - edges[j].r);
				}
			}
		}
		for (int i=0; i<n; i++)  pre[i] = i;
		sort(e,e+cnt);
		double ans = 0;
		for (int i=0; i<cnt; i++) {
			int a = e[i].from;
			int b = e[i].to;
			if (find(a) != find(b)) {
				ans += e[i].div;
				pre[find(a)] = find(b);
			}
		}
		printf("%.3lf\n",ans);
	}
	return 0;
}
```
