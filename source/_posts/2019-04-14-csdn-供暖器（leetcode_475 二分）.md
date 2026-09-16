---
title: 供暖器（leetcode_475 二分）
date: '2019-04-14 19:30:00'
permalink: 2019/04/14/csdn/供暖器（leetcode_475 二分）/
categories:
- 算法与数据结构
- 基础算法
tags:
- 二分
---

[题目](https://leetcode-cn.com/problems/heaters/)

> 只要结果在一个单调区间内，且结果两边一边满足另一边不满足，用二分查找ans，当ans特殊时，考虑用倍增  
> r=max(house[n-1],heater[m-1]) 此时半径一定能包含所有的house  
> check时 以heater为点 看house满足范围就行了  
> [二分模板](https://mp.csdn.net/mdeditor/89215142#)

```arduino
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
vector<int> house;
vector<int> heater;
int n,m;
bool check(int r){
    int i=0;
    for(int j=0;j<m;j++){
        while(abs(house[i]-heater[j])<=r && i<n) i++;
        if(i==n) return true;
    }
    return false;
}
int main(){
//    freopen("a.txt","r",stdin);
    cin>>n>>m;
    house.resize(n);
    heater.resize(m);
    for(int i=0;i<n;i++) cin>>house[i];
    for(int i=0;i<m;i++) cin>>heater[i];
    sort(house.begin(),house.end());
    sort(heater.begin(),heater.end());
    int l=0,r=max(house[n-1],heater[m-1]);
    int ans=-1;
    while( l<=r ){
        int mid=(l+r)>>1;
        if( check(mid) )   ans=mid,r=mid-1;
        else l=mid+1;
    }
    cout<<ans;
    return 0;
}
```
