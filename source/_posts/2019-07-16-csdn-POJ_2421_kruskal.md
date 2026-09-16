---
title: POJ_2421_kruskal
date: '2019-07-16 00:52:00'
permalink: 2019/07/16/csdn/POJ_2421_kruskal/
categories:
- 算法与数据结构
- 图论
---

[POJ 2421](http://poj.org/problem?id=2421)

- 思路:最小生成树中有的边已经被选取,那么先标记加入到并查集中就行了,
- 然后继续求最小生成树
  ```cpp
#include <iostream>
#include <algorithm>
using namespace std;
const int maxn=1e5;
struct node{
    int from,to,div;
    node(){}
    node(int u,int v,int w) {
    	from = u; to = v; div = w;
    }
    bool operator<(const node& t)const {
        return div<t.div;
    }
}e[maxn];
int pre[maxn];
 
int find(int x){
    if (x == pre[x]) return x;
    else return pre[x] = find(pre[x]);
}
int main(){
//	freopen("a.txt","r",stdin);
    int n;
    cin >> n;
    for(int i=1;i<=n;i++)  pre[i]=i;
    int cnt = 0;
    for(int i=1;i<=n;i++) {
    	int div;
    	for (int j=1; j<=n; j++) {
    		cin >> div;
    		e[cnt++] = node(i,j,div);
    	}
    }
    int times;
    cin >> times;

    for (int i=1; i<=times; i++) {
    	int a,b;
    	cin >> a >> b;
    	pre[find(a)] = find(b);
    }
    int ans=0;
    sort(e,e+cnt);
    
    for(int i=0;i<cnt;i++){
        int a=e[i].from;
        int b=e[i].to;
        if( find(a) != find(b) ){ //根节点不同说明没有环
            ans+=e[i].div;
            pre[find(a)]=find(b);
        }
    }
    cout<<ans;
    return 0;
}
```
