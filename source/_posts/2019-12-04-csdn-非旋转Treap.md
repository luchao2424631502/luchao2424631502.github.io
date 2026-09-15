---
title: 非旋转Treap
date: '2019-12-04 12:00:00'
permalink: 2019/12/04/csdn/非旋转Treap/
categories:
- 算法
tags:
- 非旋转Treap
---

### 非旋转Treap

> 通过**节点的优先级**来维护树的平衡, 下面是**普通非旋转Treap** (弱平衡,

#### 性质

1. Treap是笛卡尔树的一种,只是 **节点优先级是随机的**
2. $Tree+Heap$: 二叉搜索树+堆的性质
3. 2个核心操作 **分裂+合并**

#### 分裂 split

> 按照 **节点权值**分裂或者**值的排名**分裂

1. $split\_val$

   > 将一颗`treap`分裂成2个`treap`,第一个`treap`**所有节点的权值**$\le key$ , 第二个`treap`**所有节点的权值**$\gt key$

   ---

   > 判断**节点权值$val[index]$** 是否 $\le key$,
   >
   > 1. 若$val[index]\le key$,则第一个$treap$就是 $index$及其左子树, 但右子树可能还有节点权值$\le key$,所以再去$index$的右子树去分裂
   > 2. 若$val[index] \gt key$,则第二个$treap$就是$index$及其右子树.但左子树可能还有节点权值$\gt key$ ,所以再去$index$左子树去分裂```c
// oi-wiki 上的指针版
pair<node *, node *> split(node *u, int key) {
  if (u == nullptr) {
    return make_pair(nullptr, nullptr);
  }
  if (key < u->key) {
    pair<node *, node *> o = split(u->lch, key);
    u->lch = o.second;
    return make_pair(o.first, u);
  } else {
    pair<node *, node *> o = split(u->rch, key);
    u->rch = o.first;
    return make_pair(u, o.second);
  }
}
```
2. $split\_kth$

   > 和$split\_val$一样, **注意一下去了右子树减去前面所有排名**

#### 合并 merge

> 合并2个$treap$是有顺序的,子树$x$的中序遍历`3,5,7`,子树$y$的中序遍历`1,4,8`,那么合并$(x,y)$后$treap$的中序遍历为`3,5,7,1,4,8`, **将$y$树代表的序列拼接到$x$树代表的序列**
>
> 为了**保持平衡**, 根据节点的优先级来合并
>
> ---
>
> 例如$merge(x,y)$,判断节点的优先级$priority$
>
> 1. $priority[x] < priority[y]$ ,那么$x$作为根节点，$y$和$x$的右子树去合并 (因为$y$要接在$x$序列后面,根据中序遍历的性质,所有要去$x$的右子树)
> 2. $priority[x] \ge priority[y]$,那么$y$作为根节点, $x$和$y$的左子树去合并,(因为中序遍历的性质,去$y$的左子树)
>
> ---
>
> ```c
// oi-wiki 指针版
node *merge(node *u, node *v) {
  if (u == nullptr) {
    return v;
  }
  if (v == nullptr) {
    return u;
  }
  if (u->priority > v->priority) {
    u->rch = merge(u->rch, v);
    return u;
  } else {
    v->lch = merge(u, v->lch);
    return v;
  }
}
```

#### 其他操作 (都是基于分裂和合并)

1. 建树(~~我现在只会一个一个插入~~)
2. $insert(val) = split\_val + new\_node + merge$
3. $delete(val) = split\_val + split\_kth + merge$
4. $rank(val) = split\_val + merge$
5. $kth(k) = split\_kth\*2 + merge$
6. $pre(val) = split\_val + split\_kth + merge$
7. $nxt(val) = split\_val + split\_kth +merge$

[Luogu 平衡树](https://www.luogu.com.cn/problem/P3369)

```java
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5+10;

int ch[maxn][2],size[maxn],val[maxn],priority[maxn];
int tot,root;

void maintain(int x) { size[x] = size[ch[x][0]] + size[ch[x][1]] + 1; }

void split_val(int index,int value,int &x,int &y) {
    if (!index) {
        x = y = 0;
        return ;
    }
    if (val[index] <= value) {
        x = index;
        split_val(ch[index][1],value,ch[index][1],y);
    } else {
        y = index;
        split_val(ch[index][0],value,x,ch[index][0]);
    }
    maintain(index);
}

void split_kth(int index,int k,int &x,int &y) {
    if (!index) {
        x = y = 0;
        return ;
    }
    if (k <= size[ch[index][0]]) {
        y = index;
        split_kth(ch[index][0],k,x,ch[index][0]);
    } else {
        x = index;
        split_kth(ch[index][1],k-1-size[ch[index][0]],ch[index][1],y);
    }
    maintain(index);
}

int merge(int x,int y) { // 合并x 和 节点,y接在x后面
    if (!x || !y) return x + y;
    if (priority[x] < priority[y]) {
        // x 作为根节点,要满足中序遍历则,去x的右子树
        ch[x][1] = merge(ch[x][1],y);
        // 回溯时维护大小
        maintain(x);
        return x;
    } else { // y 作为根节点,为了满足中序遍历,x去左子树
        ch[y][0] = merge(x,ch[y][0]);
        maintain(y);
        return y;
    }
}

int new_node(int value) {
    val[++tot] = value;
    size[tot] = 1;
    return tot; // 返回节点编号
}

// 初始化节点的优先级
void init() {
    srand(time(0));
    for (int i=0; i<maxn-1; ++i)
        priority[i] = rand();
}

int n,i,x,r1,r2;

int main() {
    init();
    scanf("%d",&n);
    while (n--) {
        scanf("%d%d",&i,&x);
        if (i == 1) {
            // 在恰当的分裂 合并新的点
            split_val(root,x,root,r1);
            root = merge(root,merge(new_node(x),r1));
        }
        if (i == 2) { // 删除一个x值
            split_val(root,x-1,root,r1);
            split_kth(r1,1,r2,r1);
            root = merge(root,r1);
        }
        if (i == 3) { // x值的排名
            split_val(root,x-1,root,r1);
            printf("%d\n",size[root]+1);
            root = merge(root,r1);
        }
        if (i == 4) { // 查询排名为x的值
            split_kth(root,x-1,root,r1);
            split_kth(r1,1,r1,r2);
            printf("%d\n",val[r1]);
            root = merge(root,merge(r1,r2));
        }
        if (i == 5) { // x 的前驱
            split_val(root,x-1,root,r1);
            split_kth(root,size[root]-1,root,r2);
            printf("%d\n",val[r2]);
            root = merge(root,merge(r2,r1)); // 合并的时候注意r2,r1的顺序
        }
        if (i == 6) { // x 的后继
            split_val(root,x,root,r1);
            split_kth(r1,1,r1,r2);
            printf("%d\n",val[r1]);
            root = merge(root,merge(r1,r2));
        }
    }
    return 0;
}
```

---

[oi-wiki Treap](https://oi-wiki.org/ds/treap/)

[%%%% 大佬非旋Treap](https://www.cnblogs.com/akakw1/p/9892156.html)  
杂: 1天+1早上
