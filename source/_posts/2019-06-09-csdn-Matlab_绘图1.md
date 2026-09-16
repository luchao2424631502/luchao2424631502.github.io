---
title: Matlab_绘图1
date: '2019-06-09 20:47:00'
permalink: 2019/06/09/csdn/Matlab_绘图1/
categories:
- 编程语言
- MATLAB
---

`plot(x,y(x));`  
`plot(y(x));` x的长度从1~length(y)

1.同时画多个图,上一个会被`refresh`,用`command`  
`hold on` `hold off`,能在一个窗口上**叠加画**图像

```matlab
hold on
plot(cos(0:pi/20:2*pi));
plot(sin(0:pi/20:2*pi));
hold off
————————
hold on
plot(cos(0:pi/20:2*pi),'or');
plot(sin(0:pi/20:2*pi),'xg')
hold off
```

- `plot(x,y,'str')`

1. str包括三种
2. `Data markers`**数据标记** (x点的形状)
3. `Line types` **连接点之间的线**
4. `Colors` 线的颜色  
   例 `plot(x,cos(x),'x--g')`

- 也可以不用`hold on`来画多个图

  ```gml
x = 0:0.5:4*pi;
y = sin(x);
h = cos(x);
w = 1 ./ (1+exp(-x));
g = (1/(2*pi*2)^0.5).*exp((-1.*(x-2*pi).^2)./(2*2^2));
plot(x,y,'bd-',x,h,'gp ',x,w,'ro-',x,g,'c^-');
legend('sin()','','gauss');
```
- `plot(,,,...)`参数多次声明就行了,
- 标记出来每个函数的名字  
  `legend('','',...)`,参数是按照`plot`函数参数的顺序来计算的
- 图 `X Y Z`轴的`label 标签`,和图的`title` (`title ans ?label`)

  ```matlab
x = 0:0.1:2*pi;
y1 = sin(x);
y2 = exp(-x);
plot(x,y1,'--*',x,y2,':o');
xlabel('t = 0 to 2\pi');
ylabel('values of sin(t) ans e^{-x}');
title('Function Plots of sin(t) and e^{-x}');
legend('sin(t)','e^{-x}');
text(1,2,'这里也有md数学公式语法,看文档')
```
- `text(x,y,'str')` 在`(x,y)`处**添加文本**
- 注意 函数指针 和 函数 作为`plot()`参数时的写法

  ```matlab
f = @(x) x .* x; 
g = sin(2 * pi .* x);
x = 1:0.002:2;
plot(x,f(x),x,g);
% 标签
xlabel('Times(ms)')
title('Mini Assignment #1')
ylabel('f(t)');
legend('t^2','sin(2\pit)');
```

  #### Figure adjustment(图象设置)

  `get(gca) %get current axes的属性`  
  同理`get(gcf) %get current figure 的属性`

  ```matlab
set(gca(指针|句柄|handle),'XLim',[0,2*pi]);%给定x轴的范围
set(gca,'YLim',[-1.2,1.2]);

或者
xlim([0,2*pi]);
ylim([-1.2,1.2]);
```

  例如 $sin(x) [0,2\pi]$

  ```matlab
x = linspace(0,2*pi,1000);
y = sin(x);
point = plot(x,y); % point指向的是 line
 %get current axes
set(gca,'XLim',[0,2*pi]); %将x轴的限制从7改为6,只是为了好看
set(gca,'XTick',0:pi/2:2*pi)%将x轴的刻度变为 pi/2,开始规范刻度
set(gca,'XTickLabel',{'0','\pi/2','\pi','3\pi/2','2\pi'});%将刻度标签改为pi,为了显示出Pi
```
- 由`point`来修改`line`的属性

  ```lasso
set(point,'LineStyle','-.',...
    'LineWidth',2,);
属性后面跟着设定值,
```
- 删除对象(指针)释放内存,`delete(point)`

  #### 设置 线上的点的边

  ```sas
x = rand(1,20);
set(gca,'FontSize',18);
plot(x,'-md','LineWidth',0.7,'MarkerEdgeColor','k',...
     'MarkerFaceColor','g','MarkerSize',10);%点的颜色,和边的颜色
set(gca,'XLim',[1,20]);%x轴的范围
```
- `figure`创建图窗窗口(多个窗口)

  ```apache
x = -10:0.1:10;
y1 = x .^2 - 8;
y2 = exp(x);
figure, plot(x,y1);
figure, plot(x,y2);
figure %创建了一个空窗口
```

  `gcf , gca`指向最后生成的窗口
- `subplot(n,m,1) %several small plots 'in a figure',几个图像在一个窗口中`  
  将一个窗口分为`n x m`个,指定下一个画图区域  
  `axis style`的应用

  ```apache
t = 0:0.1:2*pi;
x = 3*cos(t);
y = sin(t); %椭圆
subplot(2,2,1); plot(x,y); axis normal
subplot(2,2,2); plot(x,y); axis square
subplot(2,2,3); plot(x,y); axis equal
subplot(2,2,4); plot(x,y); axis equal tight
```
  ```nginx
axis off %关闭坐标轴
```
- 2种常用存图 **对比存数据多了as,即saveas**

  ```stylus
saveas(gcf,'filename','格式')
saveas(gcf,'a','jpg')
saveas(gcf,'b','pdf')
```
