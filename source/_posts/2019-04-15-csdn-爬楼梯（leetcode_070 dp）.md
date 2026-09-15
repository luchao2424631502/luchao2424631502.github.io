---
title: 爬楼梯（leetcode_070 dp）
date: '2019-04-15 23:00:00'
permalink: 2019/04/15/csdn/爬楼梯（leetcode_070 dp）/
categories:
- 算法
tags:
- dp
---

[题目](https://leetcode-cn.com/problems/climbing-stairs/)  
非常简单容易理解的线性dp，有n阶台阶，一次爬1或2个，爬到n阶有多少种方法，  
有1阶 dp[1]=1  
有2阶 dp[2]=2 (1+1 0+2)  
依次类推

> dp[i]:代表到第i阶台阶的方法，  
>  第i阶台阶可以分别由 `i-2` 走2步 和 `i-1`走1步到达  
>  dp方程 `dp[i]=dp[i-1]+dp[i-2]`

[最小花费爬楼梯](https://leetcode-cn.com/problems/min-cost-climbing-stairs/)  
在上一题原理上+每层台阶的花费

- ***需要注意爬到最高层有2种情况***
- 已经在第n层
- 在第n-1层可以不需要花费跳过第n层到达最高层，~~有点无语~~
  ```arduino
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int len=cost.size();
        if(len==0)  return 0;
        vector<int> dp(len);
        dp[0]=cost[0];
        dp[1]=cost[1];
        for(int i=2;i<len;i++) dp[i]=min(dp[i-1],dp[i-2])+cost[i];
        return min(dp[len-1],dp[len-2]);
    }
};
```
