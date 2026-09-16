---
title: 荷马史诗(Huffman编码)
date: '2019-04-28 20:28:00'
permalink: 2019/04/28/csdn/荷马史诗(Huffman编码)/
categories:
- 算法与数据结构
- 数据结构
tags:
- huffman树
---

## Huffman编码

- huffman树的路径来存字符，节点的权值来存字符串的数量 ，满足 $\Sigma\_{i} ^{i=n} w\_i \* l\_i$ ，则新字符串的总长度最小，
- 求最长字符串的最小值：在合并的过程中，合并一个就加入到队列中，如果`val`值相同，那么每次合并**合并次数最少**(即**深度最小**)的点，这样能使**合并次数多**的字符串（子树大的）往根节点靠拢（画图理解，子树往中间填，而不是往长的地方填），那么数的最长字符串长度就会**缩短**，所以我们记录一下已经**合并次数**（深度）

小结：

1. 从下到上建树，最小面深度为0，
2. 转成K进制代表建k叉数，注意k叉数 **到最后一层建树的时候 是否队列中有足够的节点来建树**，否则不满足 $\Sigma$ 最小，公式我推到过
3. 权值相同，按照**合并次数来建树**，记录所有节点的值`ans`，

```arduino
#include <iostream>
#include <queue>
using namespace std;
struct node {
    long long val;
    long long dep;
    node (long long a,long long b) {
        val=a;
        dep=b;
    }
    bool operator< (const node& t) const {
        return (val>t.val) || ( t.val==val && dep>t.dep );
    }
};
priority_queue<node> que;
int main() {
    freopen("a.txt","r",stdin);
    int n,k;
    scanf("%d%d",&n,&k);
    for (int i=0;i<n;i++) {
        long long temp;
        scanf("%lld",&temp);
        que.push(node(temp,0));
    }
    int dif =0;
    if ( (n-1)%(k-1) ) dif = k-1-(n-1)%(k-1);
    for (int i=1;i<=dif;i++) que.push(node(0,0));
    long long ans =0;
    int cnt=dif+n;
    while (cnt>1) {
        long long len=0,temp=0;
        for (int i=1;i<=k;i++) {
            temp += que.top().val;
            len = max(len,que.top().dep);
            que.pop();
        }

        ans += temp;
        que.push( node(temp,len+1) );
        cout << que.top().dep << endl;
        cnt -= k-1;
    }
    cout << ans << endl << que.top().dep ;
    return 0;
}
```
