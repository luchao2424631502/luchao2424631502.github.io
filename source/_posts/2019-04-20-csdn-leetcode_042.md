---
title: leetcode_042
date: '2019-04-20 19:32:00'
permalink: 2019/04/20/csdn/leetcode_042/
categories:
- 算法
---

[题目](https://leetcode-cn.com/problems/trapping-rain-water/comments/)  
思路：先找到最大值，分别从两边开始遍历，遍历时用head记录当前最高的，遇到`height[i]< height[head]`就算入面积中

```cpp
#include <iostream>
using namespace std;

const int maxn=20005;
int h[maxn];
int ans;
int main() {
//    freopen("a.txt","r",stdin);
    int n;
    scanf("%d",&n);
    if ( n<3 ) {
        printf("%d",0);
        return 0;
    }
    for (int i=0; i<n; i++) scanf("%d",&h[i]);
    int area = 0;
    int head = 0;
    int max_index = 0;
    for (int i = 0; i<n; i++) {
        if ( h[i] > h[max_index] ) max_index=i;
        if ( h[head] > h[i] ) {
            area += (h[head] - h[i]);
        } else {
            head = i;
            ans += area;
            area = 0;
        }
    }

//    cout << max_index<<endl;
    head = n-1;
    area = 0;
    for (int i=n-1; i>=max_index; i--) {
        if ( h[i] < h[head] ) {
            area += ( h[head] - h[i] );
        } else {
            ans += area;
            area = 0;
            head = i;
        }
    }
    printf("%d",ans);
    return 0;
}
```
