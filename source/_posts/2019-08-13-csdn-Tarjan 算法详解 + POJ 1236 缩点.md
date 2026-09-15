---
title: Tarjan 算法详解 + POJ 1236 缩点
date: '2019-08-13 20:45:00'
permalink: 2019/08/13/csdn/Tarjan 算法详解 + POJ 1236 缩点/
categories:
- 算法
tags:
- Tarjan
---

### 有向图(`directed graph`)

- 强连通(`strongly connected`):有向图中的**任意2个顶点**`v1 v2`.存在`v1->v2`的路径和`v2->v1`的路径,比如环.
- 强连通图:有向图中**任意2个顶点**都存在强连通.强连通图1强连通分量(自身)
- 强连通分量:有向图中的**极大强连通子图**.**将所有强连通分量缩成点,则原图变成有向无环图(`directed acyclic(非周期性) graph`)**

### Tarjan算法

- 有向图中查找强连通分量
- 整个算法基于`dfs`

---

#### 算法流程

1. 任选节点开始dfs(有向图中可能有`dfs`仍未访问到的节点,通过标记将所有点都`dfs`到)  
    搜索到的点标记后,回溯时不再取消标记(每个点访问一次)
2. 节点按照访问顺序存入栈中.`dfs`返回每个节点时检查该点是否是强连通分量的根节点.如果是那么**在栈中在该点出栈前的点就构成了该节点所在的强连通分量**.
3. `dfn[]`:表示每个节点是`dfs`第几个被访问到的.用来找到判断是否有强连通分量.  
   `low[]`:表示从该节点(包括该点)出发的可到达的点的最小`dfn[]`值

```arduino
vector<int> e[maxn];
stack<int> st;
int dfn[maxn],low[maxn];
bool vis[maxn],instack[maxn];
int cnt;
void tarjan(int u) {
	dfn[u] = low[u] =  ++cnt;
	vis[u] = 1; //访问过
	instack[u] = 1;  //标记在栈中
	st.push(u); // 加入栈中

	for (int i=0; i<e[u].size(); i++) {
		int to = e[u][i];
		if (!vis[to]) { //没有被访问过
			tarjan(to);
			low[u] = min(low[u],low[to]); //回溯时 更新每个点的low[u]
		} else if (instack[to]) // 如果to在栈中说明下一个点访问过,更新
			low[u] = min(low[u],dfn[to]); 
	}
	// 回溯时判断每个点 是否是 强联通 的 根节点, 
	// 这里将有向图中 没有出边的点也记成了一个强联通分量.因为每个点默认 dfn[] = low[]
	// int num = 0;// 看需求是否要记录强联通分量点的个数
	if (dfn[u] == low[u]) {
		// 将根节点出栈
		int cur;
		do {
			cur = st.top(); st.pop();
			instack[cur] = 0;
			// num++;
		} while(cur != u); //一直删除到根节点
	}
}
```

[POJ 1236](http://poj.org/problem?id=1236)

- 给出一个有向图.

1. 求走完整个图至少要从几个点出发
2. 添加多少条边,是的从任意点出发都能达到所有点(强连通图)

   ### 思路:
3. `tarjan`求出强连通的数量,每个点标记其所属的强连通分量,
4. 然后扫描每个点及其所有出边指向的点.由所属的强连通分量判断这2个点是否属于一个强连通分量.
5. 缩点:**将强联通分量看成点**  
   **如果这2个有向图的点属于同一个强连通分量,那么该强连分量缩成的点的入边和出边不变**  
   **如果这2个点属于不同的强连通分量,那么增加这2点所属的强联通分量所代表点的入边和出边个数**
6. 缩点后:**入边`=0`的点的个数**就是至少要从几个点出发才能满足走完整个图.  
     
   **添加多少条边**`=max(入边=0的点个数,出边=0的点的个数)`

   #### 缩点后变成有向无环图

   ### 随便画个有向无环图,模拟题目的图.使得添加最少边能变成强联通图

- 找个边界起点画一个环,所添加的边恰好是`max()`的值
  ```arduino
#include <iostream>
#include <stack>
#include <string.h>
#include <vector>
#include <algorithm>
using namespace std;
const int maxn = 105;

stack<int> st;
vector<int> e[maxn];
int cnt, index;
int dfn[maxn], low[maxn],in[maxn],out[maxn],belong[maxn];
bool vis[maxn];

void tarjin(int u) {
	dfn[u] = low[u] = ++index;
	st.push(u);
	vis[u] = 1;
	for (int i = 0; i < e[u].size(); i++) {
		int to = e[u][i];
		if (!dfn[to]) { //dfn[] == 0 时间戳=0说明没有被访问过
			tarjin(to);
			low[u] = min(low[to], low[u]); //回溯时更新low[]数组
		}
		else if (vis[to] && dfn[to] < low[u]) // (to点在栈中)存在环,更新low[u]
			low[u] = dfn[to];
	}

	if (dfn[u] == low[u]) { //存在环
		cnt++; int m;
		do {
			m = st.top(); st.pop();
			vis[m] = 0;
			belong[m] = cnt;
		} while (m!=u);
	}
}
void suodian(int n) {
	for (int i = 1; i <= n; i++) {
		int pre = belong[i]; //同一强连通分量(环)上点的出入边都=1,缩成一点.也可理解为抵消了
		for (int j = 0; j < e[i].size(); j++) {
			int topre = belong[e[i][j]]; //topre是点e[i][j]代表的强连通的编号
			if (pre != topre) {
				in[topre]++;//i->j的边 且 i点和j点不在一个强连通分量上
				out[pre]++;
			}
		}
	}
}
int main() {
//	freopen("a.txt","r",stdin);
	int n; scanf("%d",&n);
	for (int i=1; i<=n; i++)
		while (1) {
			int temp; scanf("%d",&temp);
			if (!temp) break;
			e[i].push_back(temp);
		}
	for (int i = 1; i <= n; i++)
		if (!dfn[i]) tarjin(i);
	suodian(n);
	int ans1 = 0, ans2 = 0;
	for (int i = 1; i <= cnt; i++) { //强连通缩成点后,点的总数就是强联通分量的个数
		if (!in[i]) ans1++; //起点入边=0,ans1统计起点的数量
		if (!out[i]) ans2++; //终点出边=0,ans2统计终点的数量
	}
	if (ans1 > ans2) ans2 = ans1;
	if (cnt == 1) printf("1\n0\n");
	else printf("%d\n%d\n",ans1,ans2);
	return 0;
}
```
