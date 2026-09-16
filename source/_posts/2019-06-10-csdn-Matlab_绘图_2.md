---
title: Matlab_绘图_2
date: '2019-06-10 15:40:00'
permalink: 2019/06/10/csdn/Matlab_绘图_2/
categories:
- 编程语言
- MATLAB
---

1.双y轴图象

```apache
x = linspace(0,10); %默认有100个点
y1 = sin(3*x);
yyaxis left
plot(x,y1);

y2 = sin(3*x).*exp(0.5*x);
yyaxis right
plot(x,y2);
ylim([-150,100])
```

- `yyaxis left` 激活当前坐标中左侧的y轴,同理`yyaxis right`激活右侧y轴

  #### 统计图形

1. histogram (直方图)  
   `randn(n,m)`返回正态分布的标量 n x m矩阵  
   `randm(n)`n阶矩阵

---

`randi([min,max],n,m)`返回的是随机整数

```plain
subplot(2,1,1);
hist(y,5);%第二个参数是多少列
title('bins = 10');
subplot(2,1,2);
hist(y,500);
xlim([-4,4])
title('bins = 50');
```

2. bar chart 条形图

   ```ini
x = [3 2 1 9 8];
y = [x;5:9];
subplot(1,4,1); bar(x);
subplot(1,4,2); bar(y);
subplot(1,4,3); bar3(x);
subplot(1,4,4); bar3(y);
```
3. pie chart (圆饼图)

   ```gcode
a = [10 5 20 30];
subplot(1,4,1); pie(a);
subplot(1,4,2); pie(a,[0 1 0 1]);%将每一小块分开,提上来
subplot(1,4,3); pie3(a);%三维 块不分开
subplot(1,4,4); pie3(a,[0 0 1 1]);%三维且块分开的图
```
4. shairs chart and stem chart(阶梯图和茎干图)

   ```apache
x = linspace(0,4*pi,40);
y = sin(x);
subplot(1,2,1); stairs(y);
subplot(1,2,2); stem(y);
```

   #### fill (填充图形)
5. 画出一个警告牌

   ```matlab
%t = (1:2:15)'* pi/8;
t = (0:1/2:2)*pi;
x = sin(t);
y = cos(t);
fill(x,y,'g'); %在画出的8边型 填充颜色
axis square %成矩形
axis off %关闭边框
% 在(x,y)处键入文本
text(0,0,'Wait','Color','w','FontSize',80,...
    'FontWeight','bold','HorizontalAlignment','center');
saveas(gcf,'wait','jpg');
```
6. 49:00 开始三维做图 (颜色先放一下)

   #### 3D plots

- 三维图像需要(x,y)轴上的点数目对应,因为`plot3`是 `line`类型,将 所有的`(x,y,z)`点都连接起来的图象,所以`x,y`个数对应不起来就无法作图
- 其实通过x,也就变相的确定了`y`的地位
- example

  ```matlab
x = 0:0.1*pi:2*pi;
y = sin(x);
z = 0:0.1*pi:2*pi;
plot3(x,y,z);
%%
x = 0:0.1:3*pi;
y1 = zeros(size(x)); %size(x)=1,95,和x的维度要对应,所以相当于固定y1 = 0
y3 = ones(size(x)); %同理
y2 = y3./2 - sin(x);%在x,y对应数目相同的情况下,改变每一个y的值
z1 = sin(x); z2 = sin(2*x); z3 = sin(3*x);
plot3(x,y1,z1,'r',x,y2,z2,'b',x,y3,z3,'g')
grid on
xlabel('x-axis');
ylabel('y-axis');
zlabel('z-axis');
%%
t = 0:pi/50:10*pi;
plot3(sin(t),cos(t),t);
saveas(gcf,'圆圈','pdf')
%%
turns = 40 * pi;
t = linspace(0,turns,4e3);
x = cos(t) .* (turns - t);
y = sin(t) .* (turns - t);
z = t ./ sec(x);
plot3(x,y,z);
grid on
axis tight
saveas(gcf,'立体蚊香','pdf');
```

  ### 3D surface plots
- `meshgrid(x,y)` 相当于求出x,y给出所有线的交点,每一个参数都返回一个交点矩阵,对应位置是该点的坐标
- `mesh(x,y,z) 啮合nie` 画的是三维grid图,但是 小格子 没有上色
- `surf(x,y,z)`,画的三维上色的grid图
- `contour(x,y,z)轮廓` 相当于 `projection 投影 矩阵的等高线图`

```matlab
x = 1:0.1:3;
y = -2:0.1:2;
[x y] = meshgrid(x,y);
%每一个x线与y线相交,
%得到的交点的集合,x,y,每一个对应位置都是一个点
z = x .* exp(-x .^ 2 - y .^ 2);
figure 
subplot(1,2,1); mesh(x,y,z); 
subplot(1,2,2); surf(x,y,z);
%%
x = -3.5 : 0.2 : 3.5;
y = -3.5 : 0.2 : 3.5;
[x y] = meshgrid(x,y);%每一个参数返回的都是矩阵
z = x .* exp(-x.^2-y.^2);
subplot(1,3,1); mesh(x,y,z); axis square; 
subplot(1,3,2); surf(x,y,z); axis square;
subplot(1,3,3); contour(x,y,z); axis square
```
