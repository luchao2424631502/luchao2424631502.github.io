---
title: poj2442Sequence(堆)
date: '2019-04-21 15:52:00'
permalink: 2019/04/21/csdn/poj2442Sequence(堆)/
categories:
- 算法
tags:
- 堆
---

[题目](http://poj.org/problem?id=2442)  
思路：  
m个长度为n的序列，每个序列中任取一个，构成 $n^m$ 个和，求其中最小的n个和

1. 当m=2时，求2个序列中，任取一个所构成和中的n个最小和，

- 将2个序列从小到大排序，最小的一定是 $A[1]+B[1]$ ,那么下一个最小的是 $min(A[1]+B[2],A[2]+B[1])$ ,若此时最小的为`A[2]+B[1]`,**下一个最小状态从当前最小状态的下标进行移动**,那么下一个最小的为 $min(A[1]+B[2],A[2]+B[2],A[3]+B[1])$ ，，`A[2]+B[2]`=`A[2]+B[1],j+1`,`A[3]+B[1]=A[2]+B[1],i+1`
- 但某个状态时`A[1]+B[2]`也能够得到`A[2]+B[2]`，会导致重复进入堆中，
- 那么我们规定如果上一次`j+1`过一次，那么此次`j`仍然只能`+1`且`i`不变,此状态下将`i = j`这一相同情况留给`i<j`这一状态来达到,所以`i = j`这一情况不会重复
- 堆将`A[i]+B[j]`作为权值，将(i,j,bool)插入堆中，每次取堆顶点形成前n个最小的和，
- m>2时，将2形成的最小和与第3个序列进行同样的操作.  
  ~~代码太长写了1.5个小时，被数据卡了~~
  ```arduino
#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;
struct node {
    int i;
    int j;
    bool flag;
    long long sum;
    bool operator<(const node& t)const {
        return (this->sum)>(t.sum);//小根堆
    }
};
priority_queue<node> que;
vector <int> min_val;
vector <int> numa,numb;
int main() {
    freopen("a.txt","r",stdin);
    int times;
    scanf("%d",&times);
    while ( times--) {
        int m,n;
        scanf("%d%d",&m,&n);//m个长度为n的序列
        for (int j=0;j<n;j++) {
            int numtemp;
            scanf("%d",&numtemp);
            numa.push_back(numtemp);
        }
        sort(numa.begin(),numa.end());

        for (int i=0;i<(m-1);i++) {//m个数列，合并m-1次
            for (int j=0;j<n;j++) {
                int numtemp;
                scanf("%d",&numtemp);
                numb.push_back(numtemp);
            }
            sort(numb.begin(),numb.end());
            //合并
//            printf("1");
//            return 0;

            node t;
            t.i=0; t.j=0; t.flag=false; t.sum=numa[0]+numb[0];
            que.push(t);
            for (int k=0;k<n;k++) {
                node t=que.top();
                que.pop();
                min_val.push_back(t.sum);

                if( t.flag == false ){
                    node a,b;
                    a.i=t.i+1; a.j=t.j; a.flag=false; a.sum=numa[a.i]+numb[a.j];
                    b.i=t.i; b.j=t.j+1; b.flag=true; b.sum=numa[b.i]+numb[b.j];
                    que.push(a);
                    que.push(b);
                } else {
                    node b;
                    b.i=t.i; b.j=t.j+1; b.flag=true; b.sum=numa[b.i]+numb[b.j];
                    que.push(b);
                }

            }
//            for (int i=0;i<n;i++) printf("%d ",min_val[i]);
//            return 0;
            for (int k=0;k<n;k++) numa[k] = min_val[k];//保留合并后的min_val数组
            while (!numb.empty() ) numb.pop_back();
            while (!que.empty() ) que.pop();
            while (!min_val.empty()) min_val.pop_back();
        }
        for (int k=0;k<n;k++) {
            printf("%d",numa[k]);
            if( k!= n-1 ) printf(" ");
            else printf("\n");
        }
        while (!numa.empty() ) numa.pop_back();
    }
    return 0;
}
```
