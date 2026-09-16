---
title: leetcode 003
date: '2019-04-14 19:20:00'
permalink: 2019/04/14/csdn/leetcode 003/
categories:
- 算法与数据结构
- 基础算法
tags:
- 字符
---

[题目](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

- 思路

想到ascii码表一共就256个字符，遍历时每次标记就行了

```cpp
class Solution {
public:
    bool vis[300];
    int len=0;
    int ans=0;
    int lengthOfLongestSubstring(string s) {
        for(int i=0;i<s.size();i++){
            len=0;
            memset(vis,0,sizeof vis);
            for(int j=i;j<s.size();j++){
                if( vis[ s[j] ] == 0){
                    vis[ s[j] ]=1;
                    len++;
                }
                else    break;
            }
            if( len > ans ) ans=len;
        }
        return ans;
    }
};
```
