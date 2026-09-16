---
title: Matlab_结构化程序及自定义函数
date: '2019-06-09 09:06:00'
permalink: 2019/06/09/csdn/Matlab_结构化程序及自定义函数/
categories:
- 编程语言
- MATLAB
---

1. `%注释`
2. `%% section == 节 -> runsection`
3. c中是`!=` matlab是`~=`
4. end 作为代码块结束语句
5. `disp('xx') == printf()`
6. switch
   ```matlab
input_num = 1;
switch input_num
case -1
    disp('');
case 0
    disp('');
case 1
    disp('');
otherwise
    disp('');
end
```
7. while
   ```matlab
prod(1:n) %计算阶乘 
prod(a)
1.向量的话,计算每个元素乘积
2.非空矩阵 计算每一列的元素乘积然后行向量
```
   ```matlab
%%
n = 1
sum = 0
while n<=999
    sum = n + sum
    n = n + 1
end
disp(sum) 
%%
n = 1
while prod(1:n) < 1e100
    n = n + 1
end
disp(n)
```
8. for
   ```matlab
for variable = start:increment:end
    commands
end
% 标准
```

```matlab
cnt = 0;
a = [] %感觉这里其实还是声明了一个数组,在空间中就是向量
for n = 1:10
    a(n) = 2^n
end
disp(a)
```

9.

```matlab
%%
tic
clear
a = zeros(2000,2000);
for ii = 1:size(a,1);
    for jj = 1:size(a,2);
        a(ii,jj) = ii + jj;
    end
end
toc
时间已过 0.084059 秒。
%%
tic
clear
for ii = 1:2000;
    for jj = 1:2000;
        a(ii,jj) = ii + jj;
    end
end
toc
时间已过 5.491574 秒。
```

- 预先声明内存耗时非常少(具体看内存使用情况)
- `tic toc`用来在代码块中计时
- `;`的作用是:是否显示在命令行

10.

```matlab
clear 清除所有变量内存,每次执行脚本最好清除
clear xx 清除变量xx
close all 关闭所有图形
ctrl + c 在命令行强行终止程序
```

## `...`代表换行

```ini
a = [1 2 3;...
     4 5 6;...
     8 9 10];
```


- matlab中 function 以 文件 的形式写
- 打开一个缺省函数定义`edit(which('mean.m'))`
- 用 `function`这个 keyword 来建一个自己的函数,并且`filename == functionname`
- `function y = filename(a,b,c)`
- 建议用`.*` 或者`./`,因为如果参数是向量
- 如果是`script`,就不会有`function` 这个 `keyword`

12. `functions with multiple inputs ans outputs 函数有 多种输入和输出`
    ```matlab
function [a F] = acc(v2,v1,t2,t1,m)
a = (v2 - v1) ./ (t2 - t1);
F = m .* a;
```
    调用
    ```matlab
tic
[a b] = acc(2,1,2,1,1)
[c d] = acc(4,1,2,1,0.5)
[Acc Force] = acc([2 4],[1 1],[2 2],[1 1],[1 0.5]);
%Acc和Force分别是用行向量来存每一组的结果,但是将每一组对应结果就转成列向量看
[Acc' Force'] %转成列向量看每一组的结果
toc
```
13. function handle(函数句柄)

- 相当于创建一个函数指针
  ```matlab
f = @(x) cos(x)
f 指向 cos 这个函数
%等价于
f.m
function y = f(x)
y = cos(x)
```

14.输入

```matlab
x = input("你需要显示的字符串")
str = input("你输入的是字符串",'s')

%也可以和c中一样,fprintf()写入文本或在屏幕上显示
fprintf("%d",x)
```

#### 小练习

1.摄氏温度转华氏温度function

```zephir
function y = temperature(t1)
y = (t1-32) ./ 1.8;
% 调用
temperature(74)
```

带输出输入

```matlab
x = input("Temperature in C:");
while x;
    fprintf("Temperature in C = %f\n",temperature(x));
    x = input("Temperature in C:");
    if isempty(x)
        break;
    end    
end
```
