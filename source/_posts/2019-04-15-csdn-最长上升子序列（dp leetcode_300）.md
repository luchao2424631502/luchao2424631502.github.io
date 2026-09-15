---
title: 最长上升子序列（dp leetcode_300）
date: '2019-04-15 22:57:00'
permalink: 2019/04/15/csdn/最长上升子序列（dp leetcode_300）/
categories:
- 算法
tags:
- dp
---

## 最长上升子序列

[题目](https://leetcode-cn.com/problems/longest-increasing-subsequence/)  
给定一个无序的整数数组，找到其中最长上升子序列的长度。  
样例输入：

```dns
输入: [10,9,2,5,3,7,101,18]  
输出: 4   
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
```
> 思路  
> 用一个数组来维护上升的子序列，扫描原数组的数时，用二分在新数组中找到并且加入，但是要替换掉原来的，因为要按照原数组的顺序加入，如果新数组的数都小于该数，直接push\_back

```arduino
O（n logn）
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
const int maxn=10000;
int a[maxn];
int main(){
    int n;
    cin>>n;
    for(int i=1;i<=n;i++) cin>>a[i];
    vector<int> ans;
    for(int i=1;i<=n;i++){
        vector<int>::iterator it=lower_bound(ans.begin(),ans.end(),a[i]);
        if( it == ans.end() ) ans.push_back(a[i]);
        else *it=a[i];
    }
    cout<<ans.size();
    return 0;
}
```

2019/04/15 16:19  
 重新整理下思路，有三种方法，

1. 暴力枚举所有的子序列，每个数有2个决策（选或者不选），枚举出来的数有$2^n$，时间O($2^n$),当然每次可以判断当前要选的数是否小于上一个选的数，小于就continue剪枝，时间复杂度太高
2. `dp[i]`:以第i个数为结尾的最长子序列的长度，寻找第i步与第`i-1`步的状态转移关系,第i步时将`a[i]`插入到以`a[j]`(`j<i a[j]<a[i]`)结尾子序列中,求得是最长单增子序列，插入到最长的子序列中，dp方程`dp[i]=max(dp[i],dp[j]+1) (j<i && a[j]<a[i])`
   ```arduino
O(n^2)
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if(nums.size()<=0)
            return 0;
        vector<int> d(nums.size(),1);
        for(int i=1;i<nums.size();i++){
            for(int j=i-1;j>=0;j--){//插入到满足a[j]<a[i]的最长子序列中
                if( nums[j] <nums[i]){
                    d[i]=max(d[j]+1,d[i]);
                }
            }
        }
        return *max_element(d.begin(),d.end());
    }
};
```
3. 开一个向量，遍历 `a[i]` `0<=i<n`，用二分找`ans[j]>=a[i]`，如果`a[i]`大于向量中所有值就push`a[i]`进去，否则就替换`ans[j]=a[i]`,可能你会想到 **子序列一定符合原数组数的顺序，而用`a[i]`替换`ans[j]`使的向量不满足 原数组数的顺序**，但我们要想到第i点替换了并没有改变 最长最序列的长度，即使i点后没有可以加入向量的值，替换后长度（结果）还是没有变，但是如果i点有可以加入的,（根据单增）,一定会加入到 **替换的j点的后面**，这样我们又得到新的满足单增的最长子序列。代码如上.
