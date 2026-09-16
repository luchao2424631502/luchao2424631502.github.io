---
title: Matlab_变量数据类型及函数
date: '2019-06-09 15:06:00'
permalink: 2019/06/09/csdn/Matlab_变量数据类型及函数/
categories:
- 编程语言
- MATLAB
---

1. `string`可以类比c++中`string`
2. 类,`struct`
   ```less
%直接写 例如
student(1).grade(1,1)
field %struct 里面 变量名字
fieldnames(student)
rmfield(student,'name')
rmfield(student,'id')
```

- 结构体循环嵌套
- 第一个是 `xx` 代表`field`的名字,后面跟着的是内容,
- 可以直接声明,`student.name`,也可以`struct(,,...)`初始化
  ```ini
A = struct('data',[1 2 3;8 0 1],'next',...
    struct('tesenum','Test 1',...
    'xdata',[4 2 8],'ydata',[7 1 6]));
A(2).data = [9 3 2;7 6 5];
A(2).next.tesenum = 'Text 2';
A(2).next.xdaya = [1 2 3];
A(2).next.ydata = [5 0 9];
A(2);
A(2).data;
A(2).next;
A(1).data; 
A.data %输出的是A所有的data
A
```

3. cell array (元胞数组)

- 相当于分块矩阵,但是每个元素可以为不同类型  
  声明`cell`两种不同方式
  ```matlab
a{1,1} = [12 3 ;12 3];
a{1,2} = 'nihao';
a{2,1} = 9*i + 9;
a{2,2} = -pi:pi:pi;
a

%%
a(1,1) = { [12 3;12 3] };
a(1,2) = {'nihao'};
a(2,1) = {9*i + 8};
a(2,2) = {-pi:pi:pi};
a
```
- `cell array`每个元素是一个**指针**,指向不同的数据类型
- `a(1,1) %显示指向数据的类型`
- `a{1,1} %显示指向的内容`
  ```matlab
b{1,1} = 'This is the first cell';
b{1,2} = [5+j*6 4+j*5];
b{2,1} = [1 2 3;4 5 6;7 8 9];
b{2,2} = {'Tim' 'Chris'}; % cell包含cell
b
%access array
b(1,1) % 显示指向的数据类型
b(2,2)
b{2,2} % 和创建的时候是一样的
b{1,1} % 显示指向数据的内容
```
- `{}` 相当于 `int* p; *p = 1;`,**类型变了(取出所指向地址的值)**
- 而`()` 相当于`int *q; q = p;`,**类型不变(得到p的地址)**
  ```mipsasm
b{1,1} = 'This is the first cell';
b{1,2} = [5+j*6 4+j*5];
b{2,1} = [1 2 3;4 5 6;7 8 9];
b{2,2} = {'Tim' 'Chris'}; % cell包含cell
% access array
c = b(2,1); % 显示指向的数据类型
d = b{2,1};% 和创建的时候是一样的
c; %c此时是一个1x1的cell
e = c{1};
e(1,2)
```
- `cell`相当于一个**指针矩阵**
- 总结:创建有2种方式,访问有一种方式,`a{1,1}...`

4. num2cell
   ```ini
a = magic(3);
b = num2cell(a);//每个元都转成cell
```

   ### 5. `mat2cell` (矩阵转cell,用切割来理解)

   ```matlab
c = mat2cell(a,[1 1 1],[1 1 1])
%相当于横着切了三刀(y=1,2,3),竖着切了三刀(x=1,2,3)
c = mat2cell(a,[2,1],3)
%相当于横着切了1刀,一个是2行的,下一个是1行的,3是一个数字说明竖着不切,还是一个整体
c = mat2cell(a,3,3)
%相当于每切,所以是整体转为一个cell
```
5. concatenation 并列,并置
   ```gcode
a = [1 2;3 4];
b = [2 3;4 5];
cat(1,a,b); %第一维拼接(row)
cat(2,a,b); %第二维拼接(column)
car(3,a,b); %第三维 (layer)
```

- cat()
  ```dust
a{1,1} = [1 2;4 5];
a{1,2} = 'name';
a{2,1} = 2-4*i;
a{2,2} = 7;
b{1,1} = 'name2';
b{1,2} = 3;
b{2,1} = 0:1:3;
b{2,2} = [4 5]';
cat(3,a,b)
```
- reshape 重新改变形状
  ```armasm
a = ones(r1,c1);
b = reshape(a,r2,c2);
%要求满足 r1*c1 = r2*c2
```

7.存数据

- 注意 -ascii 前面的 符号
  ```vim
save xxx.mat %matlab压缩后存
save xxx.mat -ascii %ascii可以用文档看

load('xxx.mat') %以matlab压缩方式打开
load('xxx.mat','-ascii') %以ascii的方式打开
```
- 显示文件内容  
  `type filename(sinx.txt)`
- 存到`txt`中
  ```matlab
 x = 0:pi/20:3*pi;
y = sin(x);
fid = fopen('sinx.txt','w');%fid = file id,注意fopen有返回值

for i=1:21
    fprintf(fid,'%5.3f %8.4f\n',x(i),y(i));%fprintf写入
end
fclose(fid); %关闭文件
type sinx.txt %type显示文件
```
