---
title: 最短Hamilton路（二进制状态压缩）
date: '2019-04-09 16:08:00'
permalink: 2019/04/09/csdn/最短Hamilton路（二进制状态压缩）/
categories:
- 算法与数据结构
- 图论
tags:
- 二进制状态压缩
---

## 二进制状态压缩

二进制数的最低位从0开始计数  
操作 | 实现  
—|—  
取出第k位 | $(n>>k)&1$  
取出第0-（k-1）位 | n& ( (1<<K)-1 )  
n的二进制数第k位取反 | n^(1<<K)  
n的二进制数第k位赋值为1 | n|(1<<k)  
n的二进制数第k位赋值为0 | n&(~1<<K)

## 状态压缩dp例题

### 最短Hamilton路

> 给定n个顶点的带权无向图（n<=20），顶点从0-(n-1）编号，求最短的Hamilton路

> Hamilton路定义：0-（n-1）每个点不重不漏恰好经历一次

#### 思路

- 数i的二进制每一位代表点i是否走过，1代表走过，0代表还未走过
- 用`F[i,j]`代表点被经历的状态，i是二进制数，处于点j时的最短路径和
- 状态转移：`F[i,j]=min{F[i xor (1<<j) , k ] + weight[k,j] }`  
  xor代表异或  
  到点j的距离=所有已经走过的点k路径和+ 点k到点j的权值 的最小值

```arduino
#include<iostream>
#include<string.h>
using namespace std;
int weight[20][20];
int f[1<<20][20];//点的编号（0~19）
int main(){
    int n;
    cin>>n;
    memset(f,0x3f,sizeof f);
    memset(weight,0,sizeof weight);//点到该点自身 权值为0
    for(int i=0;i<n;i++){
        for(int j=i+1;j<n;j++){
            cin>>weight[i][j];
            weight[j][i]=weight[i][j];//无向图
        }
    }
    f[1][0]=0;//从0点开始
    for(int i=1;i<(1<<n);i++){//数i代表每一步所有点是否遍历过的状态
        for(int j=0;j<n;j++){//j代表当前状态的所在的点
            if( (i>>j)&1 == 1){//如果j点已经走过
                for(int k=0;k<n;k++){//找到j上一次遍历过的点
                    if(  (i^(1<<j))>>k & 1)//第j位取反（因为上一步没有j点还没走到） k位为1则k位走过
                    f[i][j]=min(f[i][j],f[i^(1<<j)][k]+weight[k][j]);//更新到j点的最短距离
                }
            }
        }
    }
    cout<< f[(1<<n)-1][n-1];
    return 0;
}
```
