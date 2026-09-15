---
title: lowbit()
date: '2019-04-07 19:45:00'
permalink: 2019/04/07/csdn/lowbit()/
categories:
- 算法
---

# lowbit 运算

> 定义：自低位的1及其后面所有位为0构成的数值

例如：  
n=10= $(1010)\_2$ ans=10

#### 推导：

设 n>0 且k位为1，第0~k-1为都为0  
**先取反在+1**

---

> 包括最高位  
> n1=10010000  
> n2=01101111  
> n3=01110000  
> an=00010000 ans=n&(~n+1)

---

看数值大小还是看原码  
**正数**原码取反+1（正数补码=原码）表示数值大小为 -n

`-n=(~n+1)`

##### 公式

`lowbit(n)=n&(-n)`

#### 通过Lowbit求二进制所有是1的位

```cpp
#include<iostream>
#include<cmath>
using namespace std;
int lowbit(int k){//k>0
    k=k&(-k);
    return k;
}
int main(){
    int n;
    cin>>n;
    int bits=-1;
    while(n){//n！=0
        bits=lowbit(n);//求出的是100...0
        cout<<log2(bits)<<endl;//代表位数
        n=n-lowbit(n);//n恰好是所有1后面全部补0的数值
    }
    return 0;
}
```

n=9=(1001)  
n1=1=0001  
n2=8=1000  
规律：`n=n-lowbit(n)`  
通过Hash代替log2();

1. > 直接建立vis数组进行标记

   ```cpp
#include<iostream>
using namespace std;
const int maxn=1<<20;
int vis[maxn];
int main(){
    int n;
    cin>>n;
    for(int i=0;i<=20;i++)    vis[1<<i]=i;//存的是素质代表的位数
    while(n){
        cout<<vis[ n&-n ]<<" ";
        n-=n&(-n);
    }
    return 0;
}
```
2. > 数学技巧  
   > 所有的$$ k\in[0,35],2^k \bmod 37 $$的值都不相同  
   > n&(-n)都是 $2^k$次幂 并且对37取mod后的值都不同

   ```cpp
#include<iostream>
using namespace std;
const int maxn=37;
int vis[maxn];
int main(){
    int n;
    cin>>n;
    for(int i=0;i<=20;i++)  vis[(1<<i)%37]=i;
    while( n ){
        cout<<vis[ (n&(-n))%37 ]<<" ";
        n-=n&(-n);
    }
    return 0;
}
```

***总结***：最重要的还是  
`n-=n&(-n)`求出下一个$2^k$次幂
