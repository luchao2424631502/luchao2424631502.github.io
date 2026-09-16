---
title: POJ_3026_BFS+prim+建图
date: '2019-07-16 18:06:00'
permalink: 2019/07/16/csdn/POJ_3026_BFS+prim+建图/
categories:
- 算法与数据结构
- 图论
tags:
- BFS+prim
---

[POJ 3026](http://poj.org/problem?id=3026)

- 题意:求出图中连接`S`和`A`在图中的最短距离。
- 样例的意思是`S`出发步数为0.
- 难点：

1. 在读入时用`map<pair<int,int>,int>`将坐标上的每一个点按顺序从1离散出来.
2. 通过`bfs`建图.~~一开始我以为单点`bfs`,后来才用多点`bfs`建图~~.能使所有点之间边都存在
3. `prim`求最短路.
4. 题目数据读入有空格,也要读(首先就写读入数据)
   ```cpp
#include <iostream>
#include <queue>
#include <string.h>
#include <map>
using namespace std;
// 思路:通过bfs建边,然后prim
const int maxn = 1e3;
const int INF = 0x3f3f3f3f;

char ch[maxn][maxn];
int m,n;
bool book[maxn][maxn];
int next1[4][2] = {0,1,1,0,0,-1,-1,0};
int e[200][200];
map<pair<int,int>,int> id;
bool vis[maxn];
int dist[maxn];
int cnt;

struct point{
    int x,y,step;
    point(){}
    point(int a,int b) {
        x=a;y=b;
    }
    point(int a,int b,int c) {
        x=a;y=b;step=c;
    }
}points[maxn];

void bfs(int x,int y) {
    memset(book,0,sizeof book);
    queue<point> que;
    book[x][y] = 1; que.push( point(x,y,0) );
    while (!que.empty()) {
        point cur = que.front(); que.pop();
        for (int i=0; i<4; i++) {
            int tx = cur.x + next1[i][0];
            int ty = cur.y + next1[i][1];
            if (tx>=1 && ty>=1 && tx<=n && ty<=m && !book[tx][ty] && ch[tx][ty]!='#') {
                book[tx][ty] = 1;
                if (ch[tx][ty] == 'A' || ch[tx][ty] == 'S') {
                    e[ id[make_pair(x,y)] ][ id[make_pair(tx,ty)] ] = cur.step+1;
                    e[ id[make_pair(tx,ty)] ][ id[make_pair(x,y) ] ] = cur.step+1;
//                    printf("e[%d][%d] = %d\n",cur.step+1);
                }
                que.push( point(tx,ty,cur.step+1) );
            }
        }
    }
} 
void prim(int start,int end) {
	memset(vis, 0 ,sizeof vis);
	int ss = id[ make_pair(start,end) ];
	vis[ss] = 1; //随便找一个点加入最小生成树中
	for (int i=1; i<=cnt; i++) dist[i] = e[ss][i]; // 更新每个点到树的距离

	long sum = 0;//最短的路径长度
	for (int i=1; i<cnt; i++) { // 开始找n-1条边
		long minn = INF; // 距离树最短的边
		int point = INF; // 距离树最近的点
		for (int i=1; i<=cnt; i++) {
			if (!vis[i] && dist[i]<minn ) {
				point = i;
				minn = dist[i];
			}
		}
		vis[point] = true; // 该点访问过（在树中）
		sum += dist[point];
		for (int i=1; i<=cnt; i++) {
			if ( !vis[i] && e[point][i]<dist[i] )
				dist[i] = e[point][i];
		}
	}
	printf("%d\n",sum);
}
int main() {
//    freopen("a.txt","r",stdin);
    int times; cin >> times;
    while (times--) {
		int start,end;
    	cnt = 0;
        scanf(" %d %d \n",&m,&n);
        for (int i=1; i<=n; i++) {
            for (int j=1; j<=m; j++) {
                scanf("%c",&ch[i][j]);
                if (ch[i][j] == 'S' || ch[i][j] == 'A') {
                    points[++cnt] = point(i,j);
                    id[make_pair(i,j)] = cnt;
                    start=i; end=j;
                }
            }
            getchar();
        }
        // 每个点bfs建图
        for (int i=1; i<=cnt; i++) 
            bfs(points[i].x,points[i].y);
        prim(start,end);
//        for (int i=1; i<=cnt; i++) {
//            for (int j=1; j<=cnt; j++) {
//                printf("%d ",e[i][j]);
//            }
//            cout << endl;
//        }
//        for (int i=1; i<=n; i++) {
//            for (int j=1; j<=m; j++) {
//                printf("%c",ch[i][j]);
//            }
//            printf("\n");
//        }
    }
    return 0;
}
```
