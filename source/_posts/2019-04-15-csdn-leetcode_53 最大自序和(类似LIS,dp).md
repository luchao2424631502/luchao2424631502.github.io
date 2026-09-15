---
title: leetcode_53 最大自序和(类似LIS,dp)
date: '2019-04-15 22:49:00'
permalink: 2019/04/15/csdn/leetcode_53 最大自序和(类似LIS,dp)/
categories:
- 算法
tags:
- dp
---

#### dp简单题

[题目](https://leetcode-cn.com/problems/maximum-subarray/)

- 如何理解 当前子序碰到 `a[i]<0` 加不加到子序中
- 如果将`a[i]`加入到sum中，sum仍然`>0`,那么加入是有意义的，否则没有意义，即是加入`a[i] a[i]<0`使得sum减小，但我们已经记录上一个sum作为最大的自序和，并且加入`a[i]`后，`a[i+1]`更大，成为新的最大子序和。
- 因为求最大子序的和，当$sum[i-1]+a[i]<=a[i]$加入到自序和中，是没有任何意义的，说明$sum[i]<=0$,那么开始记录新的子序和 $sum[i]=a[i]$
- `dp[i]=max(a[i],dp[i-1]+a[i])`即是 $dp[i-1]+a[i]>=a[i]$ 第i步才开始判断i-1步的sum的和是否为`<0`，
  ```arduino
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int len=nums.size();
        if( len == 0) return 0;
        vector<int> dp(len);
        dp[0]=nums[0];
        for(int i=1;i<len;i++) dp[i]=max(dp[i-1]+nums[i],nums[i]);
        return *max_element(dp.begin(),dp.end());
    }
};
```

```fortran
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int len=nums.size();
        if( len == 0) return 0;
        int ans=nums[0],sum=nums[0];
        for(int i=1;i<len;i++){
            if( sum>0 ) sum+=nums[i];//先判断sum的值是否>0
            else sum=nums[i];
            
            if(sum>ans) ans=sum;
        }
        return ans;
    }
};
```
