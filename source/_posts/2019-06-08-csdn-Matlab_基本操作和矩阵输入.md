---
title: Matlab_基本操作和矩阵输入
date: '2019-06-08 11:34:00'
permalink: 2019/06/08/csdn/Matlab_基本操作和矩阵输入/
categories:
- 编程语言
- MATLAB
---

> 1.输出格式

```livecodeserver
format short  
format long  
format shortE  
format longE  
format bank  (小数点后两位)  
format hex  (16进制)
```
> 2.terminal command

```powershell
clc 清屏
clear x 清除变量  
clear 清除所有变量  
who 显示所有变量名字  
whos 显示所有变量的信息
```
> 3.Array index(矩阵索引)
>
> > ## 1.index从上到下按列计数
> >
> > ## `a(index)` index按列数从上往下数
> >
> > ## `a([i1 i2 i3...])` 取出a(i1) a(i2) a(i3)… **取出后按向量初始化的方式排序**
> >
> > ## `a([i1 i2;i1 i3])` **形成ans = [a(i1) a(i2);a(i1) a(i3)]的新矩阵**
> >
> > ## 2.按 行 , 列 取
> >
> > syntax:  
> > j:k -> [j,j+1,j+2,..,j+m]  
> > j:i:k -> [j,j+i,j+2i;j+3i;j+ki]  
> > –  
> > `a(1,2)` 第一行第二个  
> > –  
> > `a([i1 i2],[i3 i4])`  **行取i1,i2行,列取i3,i4列**  
> > –

> ## 4.colon operator (冒号操作)
>
> ## `m = begin : step : end` (生成行向量,中间是步数)
>
> ## `m = [1:1:5;2:1:6;....]` (冒号生成矩阵)
>
> ## `str = 'a' : 1 : 'z'`

#### 小练习

将 a = [1 0 0;5 0 0;31 0 7] 转化为a = [1 0 0;5 0 0]  
即消掉第三行

> solution1(重新赋值).  
>  `a = a([1:2],[1:3]) (索引访问)`  
> solution2(赋成`[]`空向量)  
> `a(3,:) = []`  
> syntax:`A() = [] delete rows or columns of A,从A中删除行或者列`

> 5.矩阵拼接  
> `a = [a b]` 增广矩阵  
> `a = [a;b]` 换到下一行拼接的矩阵  
> `a = [a:b]` 矩阵`a`起始坐标作为开始点,`b`起始坐标 作为结束点 的**行向量**

> ## 6.矩阵运算
>
> `k = 2(常数) a = [1:3;2:4] b = [3:5;7:9]`  
> `a = a + k 每个元素加`  
> `a = a / k 每个元素除`  
> `a = a./ k 还是每个元素除`  
> `a = a^2 等价于 a*a 矩阵乘法`  
> `a = a.^2 矩阵每个元素2次幂`  
> `a' a的逆矩阵`  
> `a+b 对应位置每个元素相加`  
> `a * b 对应维数相同的矩阵 做乘法`  
> `a .* b 对应位置元素做乘法`  
> `a./b 对应位置元素除法`  
> `a / b 近似等价于 a * b'`

> 7. some special matrix function
>    > 1.`eye(n) nxn的单位阵`
>
> –  
> 2.`zeros(n1,n2) n1xn2元素全为0的矩阵`  
> –  
> 3.`ones(n1,n2) n1xn2元素全部为1的矩阵`  
> –  
> 4.`x = rand() 随机数小数`  
> `x = rand(n) nxn的数组`  
> `x = rand(x,y,z,...) x*y*z*...的数组`  
> `x = rand([a b]) 等价于 x = rand(a,b) [a b]为大小向量`  
> –  
> 5.`x = randi([a b],n,m)`  
> `x = randi([a b],[n m])` 生成a~~b之间的nxm大小的随机整数矩阵  
> –  
> 6.`diagonal 对角的`  
> 由矩阵作为参数返回第k个对角线上的元素`diag(a)` `diag(a,k)`  
> –  
> 由向量作为参数创建对角阵  
> `diag(a)` `diag(a,k)`  
> 向量a作为第k条对角线  
> –  
> 7.`linspace(x1,x2) 缺省是100个点`  
> `linspace(x1,x2,num) 生成线性间距向量,num是x1~~x2中生成num个点`

> 8.some matrix related function
>
> > 1.`max(a)` 每一列最大值  
> > 2.`max(max(a))`无论是行向量还是列向量返回最大值  
> > 3.`min(a)` 每一列最小值  
> > 4.`sum(a)` 每一列加和  
> > 5.`mean(a)` 每一列的平均值  
> > –  
> > 1.`sort(a)` 每一列都重新排序  
> > 2.`sortrows(a,k)`每行的顺序按照第k列(**每一行的第k个**)来排,只有行变换  
> > 3.`size(a)`返回行向量,包括每一维度的长度  
> > `size(a,k)`返回第k维的长度  
> > 4.`length(a)`返回矩阵最大维度的长度 等价于`max(size(a))`
