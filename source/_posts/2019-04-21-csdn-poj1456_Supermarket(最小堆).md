---
title: poj1456_Supermarket(最小堆)
date: '2019-04-21 10:20:00'
permalink: 2019/04/21/csdn/poj1456_Supermarket(最小堆)/
categories:
- 算法
tags:
- 堆
---

[题目](http://poj.org/problem?id=1456)  
思路：

- 题目给的是时间$t\_i$ 意思是：距离过期的时间，只要 $[1,t\_i]$ 之内被卖出就行了

1. 将时间从小到大排序,维护一个小根堆，
2. 堆为空，加入，
3. 当不为空时，如果 $t\_i$ `>` `que.size()` 意思是**当前物品距离过期的时间**大于**已经卖出的个数**，那么该物品一定可以卖出
4. 如果 $t\_i$ `=` `que.size()`，判断堆顶的**卖出的最小利润**是否**小于该物品利润**，小于就换成该物品，
5. 用一个ans记录利润
   ```arduino
#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;
 
struct node {
    int pro;
    int day;
    bool operator<(const node& t) const {
        return this->day>t.day;
    }
};
int main() {
//    freopen("a.txt","r",stdin);
    int n;
    while ( scanf("%d",&n) != EOF ) {
        priority_queue<int> que;
        vector<node> num;
        for (int i=1;i<=n;i++) {
            node temp;
            scanf("%d %d",&temp.pro,&temp.day);
            num.push_back(temp);
        }
        sort(num.begin(),num.end());
//        for (int i=0;i<n;i++) {
//            printf("%d %d ",num[i].pro,num[i].day);
//        }
//        printf("\n");
 
        int ans=0;
        for (int i=0;i<n;i++) {
            if( que.empty() ) {
                que.push( -num.back().pro );
                ans += num.back().pro;
                num.pop_back();
            }
            else {
                if( num.back().day == que.size() ) {
                    if( num.back().pro > -que.top() ) { //利润大才替换小堆的堆顶
                        ans += que.top();
                        ans += num.back().pro;
                        que.pop();
                        que.push(-num.back().pro);
                        num.pop_back();
                    }
                    else num.pop_back();
                } else if (num.back().day > que.size() ) {
                    ans += num.back().pro;
                    que.push(-num.back().pro);
                    num.pop_back();
                }
            }
        }
        printf("%d\n",ans);
    }
    return 0;
}
```
