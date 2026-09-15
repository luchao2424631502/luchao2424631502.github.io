---
title: prim和kruskal模板
date: '2019-07-15 15:13:00'
permalink: 2019/07/15/csdn/prim和kruskal模板/
categories:
- 算法
tags:
- 模板
---

- 两种都是基于贪心思想的算法

1. prim
   ```cpp
#include <bits/stdc++.h>
#define INF 0x3f3f3f3f
using namespace std;
const int maxn = 1e3;

int a[maxn][maxn];
int vis[maxn];
int dist[maxn];
int n,m;
void prim() {
	memset(vis, 0 ,sizeof vis);
	vis[1] = 1; //随便找一个点加入最小生成树中
	for (int i=1; i<=n; i++) dist[i] = a[1][i]; // 更新每个点到树的距离

	long sum = 0;//最短的路径长度
	for (int i=1; i<n; i++) { // 开始找n-1条边
		long minn = INF; // 距离树最短的边
		int point = INF; // 距离树最近的点
		for (int i=1; i<=n; i++) {
			if (!vis[i] && dist[i]<minn ) {
				point = i;
				minn = dist[i];
			}
		}
		vis[point] = true; // 该点访问过（在树中）
		sum += dist[point];
//		dist[point] = INF;  将该点到树的距离改成最大值

		//通过刚刚入树的点   更新所有没有访问过的点到新的最小生成树的距离
		for (int i=1; i<=n; i++) {
			if ( !vis[i] && a[point][i]<dist[i] )
				dist[i] = a[point][i];
		}
	}
	printf("%d",sum);
}
int main() {
	freopen("a.txt","r",stdin);
	memset(a,0x3f,sizeof a);
	cin >> n >> m;
	for (int i=1; i<=m; i++) {
		int u,v,w;
		cin >> u >> v >> w;
		a[u][v] = w;
		a[v][u] = w;
	}
	prim();
	return 0;
}
```
2. kruskal  
   解决图的最小生成树（n个点，n-1条边）路径最短的问题. 求的就是最短路径和
3. 将所有边从小到大排序 没有形成回路就加入到树中
4. 记录权值  
   输入格式：  
   n个点,m条边，接下来的m行 输入每一条边的 顶点 终点 权值

```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn=1e3;
struct node{
    int u;
    int v;
    int div;
    bool operator<(const node& t)const {
        return div<t.div;
    }
}e[maxn];
int pre[maxn];
 
int find(int x){
    int r=x;
    while( r!=pre[r] ) r=pre[r];
    int k=x;
    while( pre[k]!=r){
        int temp=pre[k];
        pre[k]=r;
        k=temp;
    }
    return r;
}
int main(){
//	freopen("a.txt","r",stdin);
    int n,m;
    cin>>n>>m;
    //并查集一定要初始化每个点的根节点
    for(int i=1;i<=n;i++)  pre[i]=i;
    
    for(int i=0;i<m;i++)  cin>>e[i].u>>e[i].v>>e[i].div;
    int ans=0;
    //按照边的权值排序
    sort(e,e+m);
    for(int i=0;i<m;i++){
        int a=e[i].u;
        int b=e[i].v;
        if( find(a) != find(b) ){ //根节点不同说明没有环
            ans+=e[i].div;
            pre[find(a)]=find(b);
        }
    }
    cout<<ans;
    return 0;
}
```
