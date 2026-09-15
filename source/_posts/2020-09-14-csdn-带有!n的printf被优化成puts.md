---
title: 带有\n的printf被优化成puts
date: '2020-09-14 10:21:00'
permalink: 2020/09/14/csdn/带有!n的printf被优化成puts/
categories:
- 编译链接
---

#### 带有\n的printf被优化成puts

test.c

```c
#include <stdio.h>

int func(int a)
{
    return 0;
}
int main()
{
    printf("Hello world\n");
    return 0;
}
```

编译成可重定位文件.o `gcc -c test.c`

1. 查看elf section table `readelf -S test.o`

   ![在这里插入图1片描述](https://img-blog.csdnimg.cn/20200914102101600.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

2. 找到.strtab序号,查看字符串表
3. 查看.strtab内容`readelf -p 11 test.o`

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200914102119356.PNG#pic_center)

---

去掉\n

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200914102134271.PNG#pic_center)
