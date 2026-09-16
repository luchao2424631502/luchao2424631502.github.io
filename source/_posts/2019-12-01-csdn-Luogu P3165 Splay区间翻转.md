---
title: Luogu P3165 Splay区间翻转
date: '2019-12-01 20:48:00'
permalink: 2019/12/01/csdn/Luogu P3165 Splay区间翻转/
categories:
- 算法与数据结构
- 数据结构
tags:
- 区间翻转
---

##### 脑残记录:

- 这周末2天~~只~~做了一道平衡树题目(~~2天被一道题限住~~),发现自己的很多问题,

  ```
  1. 学了算法及其性质 但是总是做不出来题目,很难利用学过的性质, 同样这种情况再次发生在今天
  ```

  2. 没有运用的能力,思维太差???

---

- 反思:
  1. 自己对算法题目的思维能力 还是不行 ( ？？？一定要想办法改变？？？ )
  2. 要对自己的学过的算法的流程 好好走一遍,

---

[Splay 练习 Luogu P3165](https://www.luogu.com.cn/problem/P3165)

- 即使$Splay$后中序遍历还是不变的. **不要和二叉查找树的左子树节点权值小于子树根节点小于右子树节点权值** 这个性质搞混了！！！！
- **前驱和后继求的都是在树中节点存的值的意义 (视具体情况**
- 如果$Splay$用来区间翻转**即节点存的是下标**, 则$size[x]$数组**意义是树节点$x$存的值(下标)所代表的数列值在数列中的位置(第几个or前面有几个数列值**, 用 **中序遍历保持不变这一性质来理解**

---

1. 此题 树节点存下标没啥作用, 技巧: `pos[val]`代表: 数列值$val$所在树节点的编号, (这样直接O(1)就找到值对应的树节点了,)
2. 值都在$(1,n)$区间中, 把重复值去掉,把重复的第一个放在前面

**非常难受,,卡我很长时间,**

- 如何找到区间下标`[1,p1],[2,p2],[3,p3]...`中的`1,2,3`在树中的编号,不然怎么旋转???

  1. $Splay$树的操作 , $kth$,
  2. **注意到每一次都把最小值刚好旋转到数列开头,而且我们要找$l-1$的下标,恰好直接利用$pos[i-1]$就行**
  - 效率差不多
    ```c
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5+10;

int ch[maxn][2],fa[maxn],size[maxn],val[maxn],tag[maxn],pos[maxn];
int tot,root,n;

struct node { int id,val; } a[maxn];

bool cmp1(node &test1,node &test2) {
    return test1.val < test2.val || (test1.val==test2.val && test1.id<test2.id);
}

bool cmp2(node &test1,node &test2) { return test1.id < test2.id; }

void maintain(int x) {
    if (x) size[x] = size[ch[x][0]] + size[ch[x][1]] + 1;
}

bool get(int x) { return x == ch[fa[x]][1]; }

void pushdown(int x) {
    if (!x || !tag[x]) return ;
    tag[ch[x][0]] ^= 1;
    tag[ch[x][1]] ^= 1;
    swap(ch[x][0],ch[x][1]);
    tag[x] = 0;
}

void rotate(int x) {
    pushdown(fa[x]),pushdown(x);
    int y=fa[x],z=fa[y],chk=get(x);

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
    for (int father; (father=fa[x])!=tar; rotate(x))
        if (fa[father] != tar) rotate(get(x) == get(father) ? father : x);
    if (!tar)
        root = x;
}

int nxt() {
    pushdown(root);
    int cur = ch[root][1];
    while (pushdown(cur),ch[cur][0]) cur = ch[cur][0];
    return cur;
}

int build(int l,int r,int father) {
    if (l > r) return 0;
    int mid = (l+r)>>1,now = ++tot;
    pos[a[mid].val]=now,val[now]= a[mid].id,fa[now]=father,tag[now]=0;
    ch[now][0] = build(l,mid-1,now);
    ch[now][1] = build(mid+1,r,now);
    maintain(now);
    return now;
}

int kth(int k) {
    int now = root;
    while (1) {
        pushdown(now);
        if (ch[now][0] && k <= size[ch[now][0]])
            now = ch[now][0];
        else {
            k -= size[ch[now][0]] + 1;
            if (k <= 0) return now;
            now = ch[now][1];
        }
    }
}

void prepare() {
    a[1].id=1,a[1].val=0;
    a[n+2].id=n+2,a[n+2].val=n+1;
    for (int i=1; i<=n; ++i) {
        cin >> a[i+1].val;
        a[i+1].id = i+1;
    }
    sort(a+2,a+2+n,cmp1);
    for (int i=1; i<=n; ++i) a[i+1].val = i;
    sort(a+2,a+2+n,cmp2);
}

int main() {
    cin >> n;
    prepare();
    root = build(1,n+2,0);
    for (int i=1; i<=n; ++i) {
        int x = pos[i];
        splay(x,0);
        cout << size[ch[x][0]] << " ";
        x = nxt();
        //int y = pos[i-1];
        int y = kth(i); // 比上面注释的稍微慢一点
        splay(y,0);
        splay(x,y);
        tag[ch[x][0]] ^= 1;
    }
    return 0;
}
```

- 先前一直调式的版本,

```c
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5+10;

int ch[maxn][2],fa[maxn],size[maxn],val[maxn],tag[maxn],pos[maxn];
int tot,root,n;
//int a[maxn];
struct node {
    int id,val;
} a[maxn];

bool cmp1(node &test1,node &test2) {
    return test1.val<test2.val || (test1.val==test2.val && test1.id<test2.id);
}
bool cmp2(node &test1,node &test2) { return test1.id < test2.id; }

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
    int y=fa[x],z=fa[y],chk=get(x);
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
    for (int father; (father=fa[x])!=tar; rotate(x))
        if (fa[father]!=tar) rotate(get(x)==get(father)?father:x);
    if (!tar)
        root = x;
}

int kth(int k) {
    int now = root;
    while (1) {
        pushdown(now);
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
    int mid = (l+r)>>1;
    int now = ++tot;
    pos[a[mid].val] = now,val[now] = a[mid].id,fa[now]=father;tag[now]=0;
    ch[now][0] = build(l,mid-1,now);
    ch[now][1] = build(mid+1,r,now);
    maintain(now);
    return now;
}

void dfs(int now) {
    pushdown(now);
    if (ch[now][0]) dfs(ch[now][0]);
    cout << a[val[now]].val << " ";
    if (ch[now][1]) dfs(ch[now][1]);
}

int nxt() {
    pushdown(root);
    int cur = ch[root][1];
    while (pushdown(cur),ch[cur][0]) cur = ch[cur][0];
    return cur;
}

int m;

int main() {
    //cin >> n;
    scanf("%d",&n);
    a[1].id = 1,a[1].val=0;
    a[n+2].id = n+2,a[n+2].val = n+1;
    for (int i=1; i<=n; ++i) {
        cin >> a[i+1].val;
        a[i+1].id = i+1;
    }
    sort(a+2,a+2+n,cmp1);
    for (int i=1; i<=n; ++i)
        a[i+1].val = i;
    sort(a+2,a+2+n,cmp2);
    root = build(1,n+2,0);
    dfs(root);
    for (int i=1; i<=n; ++i) {
        int x = pos[i];
        splay(x,0);
        //cout << size[ch[x][0]] << " ";
        printf("%d ",size[ch[x][0]]);
        x = nxt();
        int y = pos[i-1];
        splay(y,0);
        splay(x,y);
        tag[ch[x][0]] ^= 1;
    }
    return 0;
}
```

---

- 自己有时候思维太死了！！！艹
