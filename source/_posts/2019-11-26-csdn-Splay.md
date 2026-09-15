---
title: Splay
date: '2019-11-26 13:43:00'
permalink: 2019/11/26/csdn/Splay/
categories:
- 算法
tags:
- splay操作
---

### [从oi-wiki学来及自己总结](https://oi-wiki.org/ds/splay/)

### Splay树

- 用$Splay$维护二叉查找树

##### 节点维护的信息

| root | tot | fa[i] | ch[i][0/1] | val[i] | cnt[i] | size[i] |
| --- | --- | --- | --- | --- | --- | --- |
| 根节点编号 | 节点个数 | 节点i的父亲节点 | 节点i的左右儿子编号 | 节点i存的值 | 节点i存的值出现的次数 | 节点i子树的大小 |

#### 旋转操作

- 本质: 将树上某个节点上移一个位置

#### 旋转总结:

> - 以**节点$x$右旋转为例, 其父亲节点为$y$,且$y$父亲节点为$z$**
>
> 1. 断开$x$与右子树的边和断开$x$与父亲节点$y$的边
> 2. 节点$x$上移来到$y$的位置,
>
>    1. 原来$x$的右子树作为$y$的左子树
>    2. $y$点下移作为$x$的新右子树
> 3. 如果$y$是$z$的左节点,那么现在$x$是$z$的左节点(反之同理),(保持原来以$y$为根节点子树的位置)

---

- 右旋会了左旋一样, **rotate操作厉害在于rotate后中序遍历保持不变**

---

#### Splay操作(3种)

- **每访问一个节点后需要旋转到根节点 (旋转 点x)**

1. $x$父亲是根节点,直接 左旋/右旋 $x$
2. $x$父亲不是根节点, **$x$与父亲节点类型相同**,则先旋转父亲,在旋转$x$
3. $x$父亲不是根节点,**$x$与父亲节点类型不同**,则**先旋转x,然后再一次旋转x**

---

- 其余操作看oi-wiki解释

```c
#include <bits/stdc++.h>
using namespace std;
const int maxn = 1e5+10;

int rt,tot,fa[maxn],ch[maxn][2],val[maxn],cnt[maxn],size[maxn];

struct Splay {
    // 基本操作
    void maintain(int x) { size[x] = size[ch[x][0]] + size[ch[x][1]] + cnt[x]; }
    bool get(int x) { return x == ch[fa[x]][1]; }
    void clear(int x) { ch[x][0] = ch[x][1] = fa[x] = val[x] = size[x] = cnt[x] = 0; }

    // 旋转
    void rotate(int x) {
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
    // 旋转到根节点
    void splay(int x) {
        for (int f=fa[x]; f=fa[x],f; rotate(x))
            if (fa[f]) rotate(get(x) == get(f) ? f : x);
        rt = x;
    }
    void ins(int k) {
        // 树为空 插入到根节点
        if (!rt) {
            val[++tot] = k;
            cnt[tot]++;
            rt = tot;
            maintain(rt);
            return ;
        }
        int cnr = rt,f = 0;
        while (1) {
            // 恰好k == 当前值
            if (val[cnr] == k) {
                cnt[cnr]++;
                maintain(cnr);
                maintain(f);
                splay(cnr);
                break;
            }
            f = cnr;
            // 判断去左树还是右树
            cnr = ch[cnr][val[cnr] < k];
            // 到了叶节点,插入新的节点
            if (!cnr) {
                val[++tot] = k;
                cnt[tot]++;
                fa[tot] = f;
                ch[f][val[f] < k] = tot;

                maintain(tot);
                maintain(f);
                splay(tot);
                break;
            }
        }
    }
    // 给一个数k 查它的排名
    int rk(int k) {
        int res = 0,cnr = rt;
        while (1) {
            if (k < val[cnr])
                cnr = ch[cnr][0];
            else {
                res += size[ch[cnr][0]];
                if (k == val[cnr]) {
                    splay(cnr);
                    return res+1;
                }
                // 加上该节点的值
                res += cnt[cnr];
                cnr = ch[cnr][1];
            }
        }
    }
    // 给出排名k, 查询数
    int kth(int k) {
        int cnr = rt;
        while (1) {
            if (ch[cnr][0] && k <= size[ch[cnr][0]])
                cnr = ch[cnr][0];
            else {
                k -= size[ch[cnr][0]] + cnt[cnr];
                if (k <= 0) return val[cnr];
                cnr = ch[cnr][1];
            }
        }
    }
    // 根节点左子树最大值
    int pre() {
        int cnr = ch[rt][0];
        while(ch[cnr][1]) cnr = ch[cnr][1];
        return cnr;
    }
    // 根节点右子树最小值
    int nxt() {
        int cnr = ch[rt][1];
        while(ch[cnr][0]) cnr = ch[cnr][0];
        return cnr;
    }
    // 删除 值为k的节点
    void del(int k) {
        // 查k的排名将它旋转到根节点
        rk(k);
        // 多个k, 减去一个然后退出
        if (cnt[rt] > 1) {
            cnt[rt]--;
            maintain(rt);
            return ;
        }
        // 子节点都不存在
        if (!ch[rt][0] && !ch[rt][1]) {
            clear(rt);
            rt = 0;
            return ;
        }
        // 左节点不存在
        if (!ch[rt][0]) {
            int cnr = rt;
            rt = ch[rt][1];
            fa[rt] = 0;
            clear(cnr);
            return ;
        }
        // 右节点不存在
        if (!ch[rt][1]) {
            int cnr = rt;
            rt = ch[rt][0];
            fa[rt] = 0;
            clear(cnr);
            return ;
        }
        // 否则将x的左子树最大值旋转上来作为新 ,删除根节点后右子树接上来
        int x = pre(),cnr = rt;
        splay(x);
        // 修改原右子树的父亲节点
        fa[ch[cnr][1]] = x;
        // 新左子树
        ch[x][1] = ch[cnr][1];
        clear(cnr);
        maintain(rt);
    }
} tree;

int n;

int main() {
    cin >> n;
    while (n--) {
        int index,temp;
        cin >> index >> temp;
        if (index == 1) {
            tree.ins(temp);
        } else if (index == 2) {
            tree.del(temp);
        } else if (index == 3) {
            cout << tree.rk(temp) << endl;
        } else if (index == 4) {
            cout << tree.kth(temp) << endl;
        } else if (index == 5) {
            tree.ins(temp);
            cout << val[tree.pre()] << endl;
            tree.del(temp);
        } else if (index == 6) {
            tree.ins(temp);
            cout << val[tree.nxt()] << endl;
            tree.del(temp);
        }
    }
    return 0;
}
```

---

- 2019/11/30 15:35:34 改blog 重新理解Splay

---

- 二叉搜索树的增删查 + Splay(伸缩) = Splay树

1. 增  
    插入一个值仍满足二叉搜索树的性质
2. 删  
    在二叉搜索中删除一个值
3. 查 (4个查询
   1. 查询树中权值第k大的值
   2. 给出一个值,查询是多大的值
   3. 前驱: 查询树的根节点**代表的权值**, 小于该值的最大值
   4. 后继: 查询树的根节点**代表的权值**, 大于该值的最小值

- oi-wiki的代码重写了一下, 加深一下理解

```c
#include <bits/stdc++.h>
using namespace std;

const int maxn = 1e5+10;

int root,tot;
int fa[maxn],ch[maxn][2],val[maxn],cnt[maxn],size[maxn];

void maintain(int x) {
    size[x] = size[ch[x][0]] + size[ch[x][1]] + cnt[x];
}

bool get(int x) {
    return x == ch[fa[x]][1];
}

void clear(int x) {
    ch[x][0] = ch[x][1] = fa[x] = val[x] = size[x] = cnt[x] = 0;
}

void rotate(int x) {
    // chk代表的是 x父节点的左树则右旋,否则左旋
    int y=fa[x],z=fa[y],chk=get(x);
    //
    ch[y][chk] = ch[x][chk^1];
    fa[ch[x][chk^1]] = y;
    //
    ch[x][chk^1] = y;
    fa[y] = x;
    //
    fa[x] = z;
    if (z) ch[z][y == ch[z][1]] = x;
    maintain(y);
    maintain(x);
}

void splay(int x) {
    for (int f=fa[x]; (f=fa[x]),f; rotate(x))
        if (fa[f]) rotate(get(x) == get(f) ? f : x);
    root = x;
}

void ins(int x) {
    // 树为空
    if (!root) {
        val[++tot] = x;
        cnt[tot]++;
        root = tot;
        maintain(root);
        return ;
    }
    int cur = root,f = 0;
    while (1) {
        if (val[cur] == x) {
            cnt[cur]++;
            maintain(cur);
            maintain(f);
            splay(cur);
            break;
        }
        f = cur;
        cur = ch[cur][val[cur] < x];
        if (!cur) {
            val[++tot] = x;
            cnt[tot]++;
            fa[tot] = f;
            ch[f][val[f] < x] = tot;
            maintain(tot);
            maintain(f);
            splay(tot);
            break;
        }
    }
}

int find(int x) {
    int cur = root,res=0;
    while (1) {
        if (x < val[cur])
            cur = ch[cur][0];
        else {
            res += size[ch[cur][0]];
            if (x == val[cur]) {
                splay(cur);
                return res+1;
            }
            res += cnt[cur];
            cur = ch[cur][1];
        }
    }
}

int kth(int index) {
    int cur = root;
    while(1) {
        if (ch[cur][0] && index <= size[ch[cur][0]])
            cur = ch[cur][0];
        else {
            index -= size[ch[cur][0]] + cnt[cur];
            if (index <= 0)
                return val[cur];
            cur = ch[cur][1];
        }
    }
}

int pre() {
    int cur = ch[root][0];
    while (ch[cur][1]) cur = ch[cur][1];
    return cur;
}

int nxt() {
    int cur = ch[root][1];
    while (ch[cur][0]) cur = ch[cur][0];
    return cur;
}

void del(int x) {
    find(x);
    if (cnt[root] > 1) {
        cnt[root]--;
        maintain(root);
        return ;
    }

    if (!ch[root][0] && !ch[root][1]) {
        clear(root);
        root = 0;
        return ;
    }

    if (!ch[root][0]) {
        int cur = root;
        root = ch[root][1];
        fa[root] = 0;
        clear(cur);
        return ;
    }

    if (!ch[root][1]) {
        int cur = root;
        root = ch[root][0];
        fa[root] = 0;
        clear(cur);
        return ;
    }
    // 根节点的左右节点都存在
    int val = pre(),cur = root;
    splay(val);
    fa[ch[cur][1]] = val;
    ch[val][1] = ch[cur][1];
    clear(cur);
    maintain(root);
}

int main() {
    int n; cin >> n;
    while (n--) {
        int index,temp;
        cin >> index >> temp;
        if (index == 1)
            ins(temp);
        else if (index == 2)
            del(temp);
        else if (index == 3)
            cout << find(temp) << endl;
        else if (index == 4)
            cout << kth(temp) << endl;
        else if (index == 5) {
            ins(temp);
            cout << val[pre()] << endl;
            del(temp);
        } else if (index == 6) {
            ins(temp);
            cout << val[nxt()] << endl;
            del(temp);
        }
    }
    return 0;
}
```

- 我真的好弱 艹tmd
