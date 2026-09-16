---
title: Splay 区间翻转（文艺平衡树）
date: '2019-11-26 12:35:00'
permalink: 2019/11/26/csdn/Splay 区间翻转（文艺平衡树）/
categories:
- 算法与数据结构
- 数据结构
tags:
- 区间翻转
---

### Splay树 区间翻转 操作

- 将数组的下标存到树中, 题目给出逆转的区间下标,那么在树中操作下标
- 利用子树都是存的是数组中连续的一段,(类似线段树)

---

- 翻转区间`[l,r]`

1. 在二叉查找树中对 数组区间翻转 只需要 更改子树中每一个节点左右的左右子树
2. 如何将整个**区间(搬离到根节点附近去)** ? 利用$Splay$的性质: **rotate后中序遍历保持不变**

   1. 将$l-1$节点通过$Splay$到根节点
   2. 将$r+1$节点通过$Splay$到根节点的右儿子

##### 给出数列 [1,2,3,4,5,6,7], 翻转 [3 4] 的流程:

![流程](https://img-blog.csdnimg.cn/20191126122658302.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70)

- 最后翻转就在以4为节点的子树中进行就行了
- 也可以给节点打一个标记,访问到时再真正旋转且下传标记 (类似线段树延迟标记)

---

###### [Luogu 文艺平衡树](https://www.luogu.com.cn/problem/P3391)

```c
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5+10;
const int inf = 0x3f3f3f3f;

int ch[maxn][2],f[maxn],size[maxn],val[maxn],tag[maxn];
int a[maxn];
int tot,root,n,m;

void maintain(int x) {
    if (x)
        size[x] = size[ch[x][0]] + size[ch[x][1]] + 1;
}

int get(int x) {
    return x == ch[f[x]][1];
}

// 当前层的
void pushdown(int x) {
    if (!x || !tag[x]) return ;
    // 传递给子树
    tag[ch[x][0]] ^= 1;
    tag[ch[x][1]] ^= 1;
    // 区间元素逆转就是 将二叉树左右子树
    swap(ch[x][0],ch[x][1]);
    // 取消此层标记
    tag[x] = 0;
}

void rotate(int x) {
    // 旋转时涉及到x即其父节点
    pushdown(f[x]);
    pushdown(x);
    // splay旋转操作
    int y = f[x],z=f[y],chk=get(x);
    ch[y][chk] = ch[x][chk^1];
    f[ch[x][chk^1]] = y;

    ch[x][chk^1] = y;
    f[y] = x;

    f[x] = z;
    if (z) ch[z][y == ch[z][1]] = x;

    // 维护节点大小信息
    maintain(y);
    maintain(x);
    return ;
}

// tar标记当前根节点,普通splay不rotate(0)
// 这里改成不rotate(tar)
void splay(int x,int tar) {
    for (int father;(father=f[x])!=tar; rotate(x))
        if (f[father]!=tar) rotate(get(x) == get(father) ? father : x);
    // 第一次需要换到根节点,第二次不需要,所以不记录
    if (!tar)
        root = x;
}

// 找到 找到区间下标k在树中的位置
int kth(int k) {
    int now = root;
    while (1) {
        // 每一层下传标记
        pushdown(now);
        if (ch[now][0] && k <= size[ch[now][0]])
            now = ch[now][0];
        else {
            k -= (size[ch[now][0]] + 1);
            if (k <= 0) return now;
            now = ch[now][1];
        }
    }
}

// 线段树式 建树
int build(int l,int r,int fa) {
    if (l > r) return 0;
    int mid = (l+r)>>1;
    int now = ++tot;
    val[now] = a[mid],f[now]=fa,tag[now]=0;
    ch[now][0] = build(l,mid-1,now);
    ch[now][1] = build(mid+1,r,now);
    maintain(now);
    return now;
}

void dfs(int now) {
    // 既然要查询, 下传标记
    pushdown(now);
    if (ch[now][0]) dfs(ch[now][0]);
    // 中序 遍历 输出
    if (val[now]>0 && val[now]<=n) cout << val[now] << " ";
    if (ch[now][1]) dfs(ch[now][1]);
    return ;
}

int main() {
    cin >> n >> m;
    a[1] = 0,a[n+2]=n+1;
    for (int i=1; i<=n; ++i) a[i+1] = i;
    root = build(1,n+2,0);
    while (m--) {
        // 输入要操作的区间值
        int l,r; cin >> l >> r;
        //树存的是区间下标,l和r是区间下标在树中编号
        l = kth(l), r = kth(r+2);
        // 节点l伸缩到根节点
        splay(l,0);
        // 节点r到根节点的右子树
        splay(r,l);
        int right = ch[root][1];
        tag[ch[right][0]] ^= 1;//标记待翻转区间的树
    }
    // 中序遍历
    dfs(root);
    return 0;
}
```

---

- 2019/11/30 16:35:7 重新理解了 在二叉树中区间翻转

---

1. 上面这一个题目有一点特殊, 序列的值和下标是相同的,但理解后知道BST存的是下标就行了,
2. 通过$kth()$得到**下标**在**树中的编号**, ***为什么不通过$val[]$值的大小往下搜索呢*** ????,
   1. 子树翻转后只满足**中序遍历顺序不变**,
   2. 但**子树根节点的权值不一定大于左子树节点的权值或者小于右子树节点的权值, 因为子树左右儿子翻转后肯定这一性质变了,**,
   3. **所以不能通过$val[]$值的大小来找下标**,$kth()$能找是因为**某个子树的左儿子还是一段连续区间,即使翻转了,是通过节点的大小来找,**

- 重新写了一下,`fa[]`保持和自己写的`splay`中`fa[]`相同,
  ```c
#include <bits/stdc++.h>
using namespace std;

const int maxn = 1e5+10;
const int  inf = 0x3f3f3f3f;

int ch[maxn][2],fa[maxn],size[maxn],val[maxn],tag[maxn];
int a[maxn];
int tot,root,n;

void maintain(int x) {
    if (x)
        size[x] = size[ch[x][0]] + size[ch[x][1]] + 1;
}

int get(int x) {
    return x == ch[fa[x]][1];
}

void pushdown(int x) {
    if (!x || !tag[x]) return ;
    tag[ch[x][0]] ^= 1;
    tag[ch[x][1]] ^= 1;
    swap(ch[x][0],ch[x][1]);
    tag[x] = 0;
}

void rotate(int x) {
    pushdown(fa[x]);
    pushdown(x);
    int y = fa[x],z=fa[y],chk=get(x);
    ch[y][chk] = ch[x][chk^1];
    fa[ch[x][chk^1]] = y;

    ch[x][chk^1] = y;
    fa[y] = x;

    fa[x] = z;
    if (z) ch[z][y == ch[z][1]] = x;

    maintain(y);
    maintain(x);
}

void splay(int x,int tar) {
    for (int father;(father=fa[x])!=tar; rotate(x))
        if (fa[father]!=tar) rotate(get(x) == get(father) ? father : x);
    if (!tar)
        root = x;
}

// 翻转后只有中序遍历满足性质,而左小中=右大的性质不满足
int kth(int k) {
    int now = root;
    while (1) {
        pushdown(now); // 下传标记
        if (ch[now][0] && k <= size[ch[now][0]])
            now = ch[now][0];
        else {
            k -= size[ch[now][0]] + 1;
            if (k <= 0) return now;
            now = ch[now][1];
        }
    }
}

int build(int l,int r,int father) {
    if (l > r) return 0;
    int mid = (l+r) >> 1;
    int now = ++tot;
    val[now] = a[mid],fa[now]=father,tag[now]=0;
    ch[now][0] = build(l,mid-1,now);
    ch[now][1] = build(mid+1,r,now);
    maintain(now);
    return now;
}

void dfs(int now) {
    pushdown(now);
    if (ch[now][0]) dfs(ch[now][0]);
    if (val[now]>0 && val[now] <= n) cout << val[now] << " ";
    if (ch[now][1]) dfs(ch[now][1]);
}

int main() {
    int m; cin >> n >> m;
    a[1] = 0;
    a[n+2] = n+1;
    for (int i=1; i<=n; ++i) a[i+1] = i;
    root = build(1,n+2,0);
    while (m--) {
        int l,r; cin >> l >> r;
        l = kth(l),r = kth(r+2);
        splay(l,0);
        splay(r,l);
        int right = ch[root][1];
        tag[ch[right][0]] ^= 1;
    }
    dfs(root);
    return 0;
}
```
