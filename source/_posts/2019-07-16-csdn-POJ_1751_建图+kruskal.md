---
title: POJ_1751_建图+kruskal
date: '2019-07-16 13:47:00'
permalink: 2019/07/16/csdn/POJ_1751_建图+kruskal/
categories:
- 算法
tags:
- kruskal
---

[POJ 1751](http://poj.org/problem?id=1751)

- 已经建好的边先用并查集指向在一起,然后`kruskal`
- 由于是特判,边的输出顺序无关
  ```cpp
#include <iostream>
#include <string.h>
#include <algorithm>
#include <math.h>

using namespace std;
const int maxn = 1e6; 

struct point{
    int x,y;
    point(){}
    point(int a,int b){
        x = a; y = b;
    }
}points[maxn];
struct node {
    int from,to;
    double div;
    node() {}
    node(int a,int b,double c) {
        from = a; to = b; div = c;
    }
    bool operator<(const node& tmp)const {
        return div < tmp.div;
    }
} e[maxn];
int n,m;
int pre[maxn];
int find(int x) {
    if (x == pre[x]) return x;
    else return pre[x] = find(pre[x]);
}
double Distance(point& a,point& b) {
    double dx = (a.x - b.x)*(a.x - b.x);
    double dy = (a.y - b.y)*(a.y - b.y);
    return sqrt(dx + dy);
}

int main() {
//	freopen("a.txt","r",stdin);
    scanf("%d",&n);
    for (int i=1; i<=n; i++) pre[i] = i;

    for (int i=1; i<=n; i++) {
        int x,y; scanf("%d%d",&x,&y);
        points[i] = point(x,y);
    }
    int cnt = 0;
    for (int i=1; i<=n; i++) {
        for (int j=i+1; j<=n; j++) {
            double div = Distance(points[i],points[j]);
            e[cnt++] = node(i,j,div);
//            e[cnt++] = node(j,i,div); 
        }
    }
    scanf("%d",&m);
    for (int i=1; i<=m; i++) {
    	int a,b; scanf("%d%d",&a,&b);
    	pre[find(a)] = find(b);
    }
    sort(e,e+cnt);
    for (int i=0; i<cnt; i++) {
        int from = e[i].from; int to = e[i].to;
        int roota = find(from),rootb = find(to);
        if ( roota != rootb ) {
        	printf("%d %d\n",from,to);
			pre[roota] = rootb;
        }
    }
    return 0;
}
```
