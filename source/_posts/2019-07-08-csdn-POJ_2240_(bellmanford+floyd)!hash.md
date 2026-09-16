---
title: POJ_2240_(bellmanford+floyd)/hash
date: '2019-07-08 21:19:00'
permalink: 2019/07/08/csdn/POJ_2240_(bellmanford+floyd)!hash/
categories:
- 算法与数据结构
- 图论
---

[POJ 2240](http://poj.org/problem?id=2240)

- 与  
  [POJ 1860](https://blog.csdn.net/qq_43580151/article/details/95029341) 一样, 判断是否存在 **正权环**
- 将字符串`hash`成`[1,30]`之内的顶点,
- bellmanford通过松弛次数来判断是否存在环,
- floyd通过比较2次货币流通后的任意一点(点就是货币)的值是否增加,增加了就说明存在正环

1. bellmanford
   ```cpp
 #include <iostream>
#include <queue>
#include <string.h>

using namespace std;
const int maxn = 35;
const int MIN = -0x3f3f3f3f;

int n,m;
double e[maxn][maxn];
double dist[maxn];
bool vis[maxn];
int cnt[maxn];
// BKDR Hash Function
unsigned int Hash(char *str)
{
    unsigned int seed = 131; // 31 131 1313 13131 131313 etc..
    unsigned int hash = 0;
 
    while (*str)
    {
        hash = hash * seed + (*str++);
    }
 
    return (hash & 0x7FFFFFFF) % 30 + 1;
}

bool bellmanford(int x) {
	queue<int> que;
	for (int i=1; i<=30; i++) dist[i] = MIN;
	memset(vis,0,sizeof vis);
	memset(cnt,0,sizeof cnt);
	// 源点可能是任意点
	vis[x] = 1; dist[x] = 1; //本金设置为1,
	que.push(x);
	while (!que.empty()) {
		int cur = que.front(); que.pop();
		vis[cur] = 0;
		for (int i=1; i<=30; i++) { // 开始扫描所有的出边
			if (dist[i] < dist[cur]*e[cur][i]) {
				dist[i] = dist[cur]*e[cur][i];
				if (!vis[i]) {
					vis[i] = 1;
					que.push(i);
					if (++cnt[i] > n) return  1;
				}
			}
		}
	}
	return  0;
}

int main() {
//	freopen("a.txt","r",stdin);
	int times=0;
	while (scanf("%d",&n) && n) {
		memset(e,0,sizeof e);
		char ch1[50],ch2[50],ch[1];
		for (int i=1; i<=n; i++) scanf("%s",ch); //读入,和做题无关, 
		
		scanf("%d",&m);
		double profit;
		int tmp=0; // 注意到hash后顶点的值在[1,30]之间,所以保存一个,等一下作为bellmanford的起点 
		for (int i=1; i<=m; i++) { // hash, 
			scanf("%s %lf %s",ch1,&profit,ch2);
			int u = Hash(ch1); int v = Hash(ch2);
			e[u][v] = profit;  
			tmp = u; // u,v都行,取一个出现的点 
		}
		if (bellmanford(tmp)) printf("Case %d: Yes\n",++times);
		else printf("Case %d: No\n",++times);
	}
	return 0;
}
```

- `backup`数组作用是对比,链接博客中有分析
- 跑两次`floyd`进行对比

2. floyd
   ```cpp
 #include <iostream>
#include <queue>
#include <string.h>

using namespace std;
const int maxn = 35;
const int MIN = -0x3f3f3f3f;

int n,m;
double e[maxn][maxn];
double dist[maxn];
bool vis[maxn];
int cnt[maxn];

// BKDR Hash Function
unsigned int Hash(char *str) {
    unsigned int seed = 131; // 31 131 1313 13131 131313 etc..
    unsigned int hash = 0;
    while (*str) {
        hash = hash * seed + (*str++);
    }
    return (hash & 0x7FFFFFFF) % 30 + 1;
}

bool istrue() {
	double backup[maxn];
	for (int i=1; i<=30; i++) backup[i] = dist[i];
	for (int k=1; k<=500; k++) 
		for (int i=1; i<=30; i++)
			for (int j=1; j<=30; j++)
				if (dist[j] < dist[i] * e[i][j]) dist[j] = dist[i] * e[i][j];
	for (int i=1; i<=30; i++)
		if (dist[i] > backup[i]) return 1;
	return 0;
}

int main() {
//	freopen("a.txt","r",stdin);
	int times=0;
	while (scanf("%d",&n) && n) {
		memset(e,0,sizeof e);
		memset(dist,0,sizeof dist);
		char ch1[50],ch2[50],ch[2];
		for (int i=1; i<=n; i++) scanf("%s",ch);
		
		scanf("%d",&m);
		double profit;
		int tmp = 0;
		for (int i=1; i<=m; i++) {
			scanf("%s %lf %s",ch1,&profit,ch2);
			int u = Hash(ch1); int v = Hash(ch2);
			e[u][v] = profit;
			tmp = u;
		}
		dist[tmp] = 1;
		istrue();
		if ( istrue() ) printf("Case %d: Yes\n",++times);
		else printf("Case %d: No\n",++times);
	}
	return 0;
}
```
