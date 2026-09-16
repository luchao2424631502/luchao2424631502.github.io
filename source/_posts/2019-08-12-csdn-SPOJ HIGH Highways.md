---
title: SPOJ HIGH Highways
date: '2019-08-12 18:07:00'
permalink: 2019/08/12/csdn/SPOJ HIGH Highways/
categories:
- 算法与数据结构
- 图论
---

[SPOJ HIGH Highways](https://www.spoj.com/problems/HIGH/en/)

- 无向图生成树计数裸题
  ```cpp
#include <iostream>
#include <algorithm>
#include <string.h>
using namespace std;
const int maxn = 205;
#define ll long long 
ll b[maxn][maxn];
// 学过线代都知道求行列式的方法之一就是化成上\下三脚矩阵,对角线元素乘积是行列式值
ll determina(int n) {
	ll res = 1;
	for (int i = 1; i <= n; i++) {
		if (!b[i][i]) { //若果对角线元素为0,把此行都一都移到下一行去
			bool flag = false;
			for (int j = i + 1; j <= n; j++) { //从i+1行开始找i列中的第一个不为0的元素，与现在的行交换
				if (b[j][i]) {//找到了该列不为0的元素,
					flag = 1; //标记,交换
					for (int k = i; k <= n; k++) swap(b[i][k], b[j][k]);
					res = -res;// 换行系数变为负数
					break; //退出.
				}
			}
			if (!flag) return 0; //这一行全部为0,行列式值为0
		}

		for (int j = i + 1; j <= n; j++) {
			while (b[j][i]) { //从下面的行找一个不为0的元素与第i行进行消元
				ll t = b[i][i] / b[j][i];
				for (int k = i; k <= n; k++) {
					b[i][k] = b[i][k] - t * b[j][k];
					swap(b[i][k], b[j][k]);//消元后,把0的行换到下面来。
				}
				res = -res;
			}
		}
		res *= b[i][i];//对角线元素相乘
//		res %= mod;
	}
	return res;
}

int main() {
//	freopen("a.txt","r",stdin);
	int times; cin >> times; 
	while (times--) {
		memset(b, 0, sizeof b); 
		int n, m ,u ,v; scanf("%d%d",&n,&m);
		if (n == 1) {
			printf("1\n");
			continue;
		}
		for (int i = 1; i <= m; i++) {
			scanf("%d%d",&u,&v);
			b[u][u]++; b[v][v]++;
			b[u][v] = b[v][u] = -1;
		}
		printf("%lld\n", determina(n -1) );
	}
	return 0;
}
```
