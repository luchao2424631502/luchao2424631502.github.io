---
title: 最优树（Huffman）
date: '2019-04-27 20:58:00'
permalink: 2019/04/27/csdn/最优树（Huffman）/
categories:
- 算法
tags:
- 最优树
---

- 最优树可以记忆为：越是距离根节点近的点的权值越大，离根节点越远的点的权值越小，
- 节点`i`,权值 $w\_i$ ,深度为 $l\_i$ ,使得 $\Sigma\_{i}^{i=n} w\_i \* l\_i$ 最小，那么此数就是Huffman树

### 二叉Huffman树

> 通过最小堆来从树的**叶子节点**建树，
>
> > 1.n个节点 $w\_i$ push进入`priority_queue`(优先队列来模拟最小堆),

> > 2.连续取出2个堆顶元素`w1,w2`作为当前节点，将`w3=w1+w2`作为他们的父亲节点,push进入queue中, $\Sigma$ = `ans += w3`

> > 3.重复此操作，当 **队列大小为1**时，说明该值为根节点的值，那么建树完成.

### k叉Huffman树

> 原理还是一样的，

- 不同的是，当我们建树到了根节点的下一层时，队列中的值不够用来组成当前层所需要的节点,不满足最优的情况,解决方法：在开始之前加入权值为=0的节点，
- 使得树的总节点个数满足 $(n-1)\ mod\ (k-1) =0$
- 我对该公式的推导：

1. 任取中间层，发现 第一个节点（是由下一层相加得到的权值和，那么不包括在给出的n个节点中），典型的就是根节点
2. 则总节点数`N`： `N= k(倒数第一层需要的节点数)+ k-1 + k-1 + …… + k-1` ，这个画个图就可以看出来，  
   设常数`C`, `N`满足`N = C(k-1)+1`->`N-1 = C(k-1)` -> `(N-1) mod (k-1) = 0`
3. 在建树之前加入 `t` 个 `w=0`的节点 使得`N`满足公式

例题：  
[合并果子](http://acm.ncst.edu.cn/contest_problem.php?cid=1028&pid=9)  
思路 ： 合并的过程就是建树的过程，记录 $\Sigma$ 的和就行了

```arduino
#include <iostream>
#include <queue>
using namespace std;
priority_queue<int> que;
int main() {
    freopen("a.txt","r",stdin);
    int n;
    scanf("%d",&n);
    for (int i=0;i<n;i++) {
        int t;
        scanf("%d",&t);
        que.push(-t);
    }
    int ans =0;
    while ( que.size() != 1 ) {
        int val1,val2,val;
        val1 = -que.top(); que.pop();
        val2 = -que.top(); que.pop();
        val = val1 + val2;
        ans += val;
        que.push(-val);
    }
    printf("%d",ans);
    return 0;
}
```
