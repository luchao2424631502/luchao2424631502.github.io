---
title: O(n)时间求 最长回文子串 Manacher算法
date: '2019-04-30 17:06:00'
permalink: 2019/04/30/csdn/O(n)时间求 最长回文子串 Manacher算法/
categories:
- 算法与数据结构
- 字符串算法
tags:
- 回文子串
---

1. 回文字符串分为奇回文和偶回文，在字符串中间插入任意字符使得串变成奇回文串

暴力思想：肯定是找一个点往两边任意扩展,遍历一次,  
Manacher时间为O(n)

1. 开一个数组`p[]`记录 以点`i`为中点 的**最长回文串的半径**,
2. 假设前`i-1`个点的`p[]`都已经求出来来，现在考虑`p[i]`如何推导  
   ![网上找来的图片](https://img-blog.csdn.net/20170521181144124?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvenpra3N1bmJveQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**重点：**  
3. `R`是`p[1]~p[i-1]`中推出来的**右端最远**最长回文子串的右端点,且用`pos`记录下来，每一步更新`pos+R`,既然`R`知道了,`L`也知道（没啥意义）  
4. 当前遍历到`i`点，`j`是与`i`对称的点,且 $j=pos-(i-pos)$ `->` $j=2pos-i$，我们可以通过`j`点来得到`i`点的`p[i]`值  
5. 此时`i j R` 有三种情况  
a. 第一个图中红色都在`[L,R]`范围内，`R-i>p[j]`,直接得到`p[i]`的值，`p[i]=p[j]`  
b.  
 ![](https://img-blog.csdn.net/20170521181152562?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvenpra3N1bmJveQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)  
此时`j`点的回文子串只有一部分在`[L,R]`(最大的回文子串)中，那么超出范围的肯定不符合要求，`R-i<p[j]`所以`p[i]=R-i`  
c. 剩下一个情况应该都看出来了,就是`i>=R`,现在只能往两边暴力扩展了

### 总结步骤：

1. 先更新`p[]`，有三种情况
2. 向两边暴力扩展回文字符串,满足前两种情况这一步肯定扩展不出来新的回文串，所以不需要特殊判断是否`if(p[i]==1)`,所以这一步往两边扩展
3. 更新`[L,R]`**右端最远的回文子串**,并且记录`pos`的值，
4. 这是（插入字符的奇数字符串）上的一系列操作，我们要转化成**源字符串**上的**位置**与**长度** 这里是2个结论，~~自己对比就可以知道了~~，  
   原字符串的位置：`index = (resid - reslen)/2`  
   源字符串的长度：`len = reslen-1`

- 在第一个添加一个与其他都不同的字符，就是为了`index`正确求出来

```arduino
#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    string t;
    while ( cin>>t && t!="END" ) {
        string s("%#");
        for (int i=0; i<t.size(); i++) {
            s += t[i];
            s += "#";
        }
        vector<int> p(s.size(),0);
        int id=0, mx=0, resid=0, reslen=0;
        for (int i=1; i<s.size(); i++) {
            p[i] = mx > i ? min(p[2*id-i],mx-i):1;
            while ( s[i-p[i]] == s[i+p[i]] ) ++p[i];
            if ( mx<i+p[i] ) {
                mx = i+p[i];
                id = i;
            }
            if ( reslen < p[i] ) {
                reslen = p[i];
                resid = i;
            }
        }
        string ans=t.substr( (resid-reslen)/2 , reslen-1 );//求出来的最长回文子串
        cout << ans.size() << endl;//长度
    }
    return 0;
}
```
