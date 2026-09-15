---
title: Floyd小结
date: '2019-09-08 14:20:00'
permalink: 2019/09/08/csdn/Floyd小结/
categories:
- 算法
---

### `Floyd`:解决多源最短路径,可以判断环

- 只要是求最短路的,不妨先想一想是否能用`floyd`
- `1000`的数据量,且多个源点,恰好适合`floyd`  
  [HDU 2066](https://vjudge.net/contest/283914#problem/C)
  ```cpp
#include <iostream>
#include <cstring>
#include <vector>
#include <algorithm>

using namespace std;
const int maxn =  1005;
const int inf = 0x3f3f3f3f;

int grid[maxn][maxn];
int T,S,D;
int n;
vector<int> cityBegin,cityEnd;

void floyd() {
    for (int k=1; k<=n; ++k)
        for (int i=1; i<=n; ++i)
            if (grid[i][k] != inf)
                for (int j=1; j<=n; ++j)
                    grid[i][j] = min(grid[i][j],grid[i][k]+grid[k][j]);
}
void init() {
    n = 0;
    memset(grid,inf,sizeof grid);
    for (int i=1; i<1005; ++i)
        grid[i][i] = 0;
    while (!cityBegin.empty()) cityBegin.pop_back();
    while (!cityEnd.empty()) cityEnd.pop_back();
}
int main() {
    //freopen("1.in","r",stdin);
    while (scanf("%d%d%d",&T,&S,&D) != EOF) {
        init();
        int a,b,time;
        for (int i=1; i<=T; ++i) {
            scanf("%d%d%d",&a,&b,&time);
            grid[a][b] = min(grid[a][b],time);
            grid[b][a] = min(grid[b][a],time);
            a = max(a,b);    n = max(a,n);
        }
        for (int i=1; i<=S; ++i) {
            int from;
            scanf("%d",&from);
            cityBegin.push_back(from);
        }
        for (int i=1; i<=D; ++i) {
            int to;
            scanf("%d",&to);
            cityEnd.push_back(to);
        }
        floyd();
        int ans = inf;
        for (auto from:cityBegin)
            for (auto to:cityEnd)
                ans = min(ans,grid[from][to]);
        printf("%d\n",ans);
    }
    return 0;
}
```
  [HDU 1217](https://vjudge.net/contest/283914#problem/E)
- 关于汇率问题,有向图判断是否存在环(`spfa`也能,数据小直接`floyd`)
  ```cpp
#include <map>
#include <iostream>
#include <algorithm>
#include <string>
#include <cstring>
using namespace std;
const int maxn = 35;

map<string,int> Hash;
int n,cnt;
double grid[maxn][maxn];
void floyd() {
    for (int k=0; k<cnt; ++k)
        for (int i=0; i<cnt; ++i)
            for (int j=0; j<cnt; ++j)
                grid[i][j] = max(grid[i][j],grid[i][k]*grid[k][j]);
}

int main() {
    freopen("1.in","r",stdin);
    int times = 1;
    while (scanf("%d",&n) && n) {
        cnt = 0;
        Hash.clear();
        memset(grid,0,sizeof grid);
        string temp;
        for (int i=1; i<=n; ++i) {
            cin >> temp;
            Hash.insert({temp,cnt++});
        }
        int m; scanf("%d",&m);
        for (int i=1; i<=m; i++) {
            string to;
            double rate;
            cin >> temp >> rate >> to;
            grid[Hash[temp]][Hash[to]] = rate;
        }
        floyd();
        bool flag = 0;
        for (int i=0; i<cnt; ++i)
            if (grid[i][i] > 1.0) {
                printf("Case %d: Yes\n",times++);
                flag = 1;
                break;
            }
        if (!flag)
            printf("Case %d: No\n",times++);
    }
    return 0;
}
```
  [洛谷 p2009](https://www.luogu.org/problem/P2009)
  ```cpp
#include <iostream>
#include <string.h>
#include <map>

using namespace std;
const int maxn = 30;
const int inf = 0x3f3f3f3f;

int grid[maxn][maxn];
int n,k;

void init() {
    memset(grid,inf,sizeof grid);
    for (int i=1; i<30; i++)
        grid[i][i] = 0;
}
void floyd() {
    for (int k=1; k<=n; ++k)
        for (int i=1; i<=n; ++i)
            for (int j=1; j<=n; ++j)
                grid[i][j] = min(grid[i][j],grid[i][k]+grid[k][j]);
}
int main() {
    //freopen("1.in","r",stdin);
    init();
    cin >> n >> k;
    for (int i=1; i<=n; i++) {
        int temp; cin >> temp;
        if (i != n)
            grid[i][i+1] = grid[i+1][i] = temp;
        else grid[i][1] = grid[1][i] = temp;
    }
    char a,b;
    for (int i=1; i<=k; ++i) {
        char a,b; int from,to,time;
        scanf("\n%c %c %d",&a,&b,&time);
        from = a - 'A' + 1; to = b - 'A' + 1;
        //cout << "from= " << from << "  to=" << to << endl;
        if (grid[from][to] == inf)
            grid[from][to] = grid[to][from] = 0;
        grid[from][to] = grid[to][from] = max(time,grid[from][to]);
    }
    floyd();
    scanf("\n%c %c",&a,&b);
    printf("%d\n",grid[a-'A'+1][b-'A'+1]);
    return 0;
}
```

  ### floyd+dp

  [HDU 2833](http://acm.hdu.edu.cn/showproblem.php?pid=2833)
- 给出一对起点和终点,求出它们最短路上的最多的公共点个数?
- 开一个`dp[][]`表示2点之间点的个数.在`floyd`通过第三个点更行路径时也更新`dp[][]`两点间的点的个数
- **最多公共点肯定在连续的一段**,**枚举2个点代表这一段**看是否在最短路上然后来更新公共点个数
  ```cpp
#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;
const int maxn = 305;
const int inf = 0x3f3f3f3f;

int n,m;
int grid[maxn][maxn],dp[maxn][maxn];

void floyd() {
    for (int k=1; k<=n; ++k)
        for (int i=1; i<=n; ++i) {
            if (grid[i][k]!=inf && i!=k){
                for (int j=1; j<=n; ++j) {
                    if (k==j || i==j) continue;
                    if (grid[i][j]>grid[i][k]+grid[k][j]) {
                        grid[i][j] = grid[i][k]+grid[k][j];
                        dp[i][j] = dp[i][k] + dp[k][j] - 1;
                    } else if (grid[i][j]==grid[i][k]+grid[k][j] &&
                            dp[i][j]<dp[i][k]+dp[k][j])
                        dp[i][j] = dp[i][k] + dp[k][j] - 1;
                }
            }
        }
}
void init() {
    for (int i=1; i<=n; i++) {
        for (int j=1; j<=n; j++) {
            grid[i][j] = inf;
            dp[i][j] = 2;
        }
        dp[i][i] = 1;
        grid[i][i] = 0;
    }
}
int findThesame(int& s1,int& e1,int& s2,int& e2) {
    int ans = 0;
    if (grid[s1][e1]==inf || grid[s2][e2]==inf) return ans;
    for (int i=1; i<=n; ++i)
        for (int j=1; j<=n; ++j)
            if (grid[s1][i]+grid[i][j]+grid[j][e1]==grid[s1][e1]
                    && grid[s2][i]+grid[i][j]+grid[j][e2]==grid[s2][e2])
                ans = max(ans,dp[i][j]);
    return ans;
}
int main() {
    //freopen("1.in","r",stdin);
    while (scanf("%d%d",&n,&m)!=EOF && (n+m)) {
        init();
        int a,b,time;
        for (int i=1; i<=m; ++i) {
            scanf("%d%d%d",&a,&b,&time);
            grid[a][b] = grid[b][a] = min(time,grid[a][b]);
        }
        floyd();
        int s1,e1,s2,e2;
        scanf("%d%d%d%d",&s1,&e1,&s2,&e2);
        printf("%d\n",findThesame(s1,e1,s2,e2));
    }
    return 0;
}
```
