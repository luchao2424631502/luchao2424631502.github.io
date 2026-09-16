---
title: POJ_2349_建图+kruskal
date: '2019-07-16 10:45:00'
permalink: 2019/07/16/csdn/POJ_2349_建图+kruskal/
categories:
- 算法与数据结构
- 图论
tags:
- kruskal
---

[POJ 2349](http://poj.org/problem?id=2349)

- 题意:一个卫星频道等同于2个点之间可以任意通信,
- 处理点之后,建图,跑`kruskal`,然后将最短路的最大边都用卫星频道替代,
- 所以最大的`D`是最小生成树里面除掉卫星通信边之后的最大边
  ```cpp
#include <iostream>
#include <string.h>
#include <math.h>
#include <algorithm>

using namespace std;
const int maxn=1e6;
int s,n;
struct point {
    int x,y;
    point(){}
    point(int a,int b) {
        x = a; y = b;
    }
} points[maxn];
struct node{
    int u,v;
    double div; 
    node(){}
    node(int a,int b,double c) {
        u = a; v = b; div = c;
    }
    bool operator<(const node& t)const {
        return div<t.div;
    }
} e[maxn];

int pre[maxn];
 
int find(int x){
    if (x == pre[x]) return x;
    else return  pre[x] = find(pre[x]);
}
double Distance(point& a,point& b) {
    double dx = (a.x - b.x)*(a.x - b.x);
    double dy = (a.y - b.y)*(a.y - b.y);
    return sqrt(dx + dy);
}

double edge[maxn];

int main(){
//	freopen("a.txt","r",stdin);
    int times; cin >> times;
    while (times--) {
        cin >> s >> n;
        for (int i=1;i<=n;i++)  pre[i]=i;

        for (int i=1; i<=n; i++) {
            int a,b; cin >> a >> b;
            points[i] = point(a,b);
        }
        int cnt = 0;
        for (int i=1; i<=n; i++) 
            for (int j=i; j<=n; j++) {
            	double div = Distance(points[i],points[j]);
                e[cnt++] = node (i,j,div);
                e[cnt++] = node (j,i,div );
            }
        int m=0;
        //按照边的权值排序
        
        sort(e,e+cnt);
        for(int i=0;i<cnt;i++){
            int a=e[i].u;
            int b=e[i].v;
            if( find(a) != find(b) ){ //根节点不同说明没有环
                // ans+=e[i].div;
                edge[m++] = e[i].div;
//                printf("%lf \n",e[i].div);
                pre[find(a)]=find(b);
            }
        }
        printf("%.2lf\n",edge[m-s]);
    }
    return 0;
}
```
