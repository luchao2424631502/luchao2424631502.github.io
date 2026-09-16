---
title: 将30天中txt文件的ascii字体像素数据转为binary插入elf格式的kernel中
date: '2021-04-24 15:42:00'
permalink: 2021/04/24/将30天中txt文件的ascii字体像素数据转为binary插入elf格式的kernel中/
categories:
- 系统与底层
- 自制操作系统
tags:
- 30天自制操作系统,操作系统真相还原
---

## 将30天中的txt文件ascii字体像素数据转化为(8bits\*16)byte array放入elf文件中

> 背景: 目前在基于elephant os上将30天的图形界面加入上来,但是30天的编译链是书作者写的,此方式是用gcc等实现,此处是处理256个ascii字体文件加入到kernel.bin中

方法:[通过objcopy将二进制文件制作成.o文件](%5Bhttp://luchao.wiki/2020/12/08/%E9%80%9A%E8%BF%87objcopy%E5%B0%862%E8%BF%9B%E5%88%B6%E6%96%87%E4%BB%B6%E4%BD%9C%E4%B8%BA-o%E4%B8%AD%E7%9A%84%E4%B8%80%E4%B8%AA%E6%AE%B5/%5D(http://luchao.wiki/2020/12/08/%E9%80%9A%E8%BF%87objcopy%E5%B0%862%E8%BF%9B%E5%88%B6%E6%96%87%E4%BB%B6%E4%BD%9C%E4%B8%BA-o%E4%B8%AD%E7%9A%84%E4%B8%80%E4%B8%AA%E6%AE%B5/))

[作者提供的hankaku.txt字体文件](https://github.com/yourtion/30dayMakeOS/blob/master/05_day/hankaku.txt)

将开头的几个日文删除,发现有个特点是`. 和 *`只代表0和1,那么只需要统计这2个字符而不管其它的字符,自己来记住对应的字体index,生成纯2进制文本对应8bits\*16字体像素.

### 将hankaku.txt转化为二进制文件

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main()
{
  unsigned char font[256][16];

  FILE *fp = fopen("hankaku.txt","r+");
  FILE *out = fopen("3.in","w+");

  int off[8] = {0x80,0x40,0x20,0x10,0x8,0x4,0x2,0x1};

  char ch;
  unsigned char data = 0;
  int index = 0;
  int num = 0;
  int count = 0;
  bool flag = 0;
  while (!feof(fp))
  {
    fread(&ch,1,1,fp);
    if (!(ch == '*' || ch == '.'))
      continue;
     // printf("|%d ",index);
    // printf("%c",ch);
    if (ch == '*')
      flag = 1;
    else 
      flag = 0;
    if (flag)
      data = data | off[count];
    count++;
    if (count == 8)
    {
      count = 0;
      font[index][num] = data;
      num++;
      if (num == 16)
      {
        num = 0;
        index++;
      }
      data = 0;
    }
  }

  for (int i=0; i<256; i++)
  {
    for (int j=0; j<16; j++)
    {
      //生成16进制对应的bitmap
      unsigned char ch = font[i][j];
      fwrite(&ch,1,1,out);

       // char buf[5];
       // sprintf(buf,"%d ",font[i][j]);
       // fwrite(buf,strlen(buf),1,out);
    }
  }
  return 0;
}
```

用`xxd 3.in`通过16进制查看生成的二进制文件,发现对应上了每个字体的16字节,

### 接下来将 binary 文件制作成i386下的.o 使得ld链接到kernel.bin,这样就能使用全局符号来访问字体资源

查看kernel.bin其中一个.o的文件的架构格式信息

![1](/images/Selection021.png)

则使用`objcopy -I binary -O elf32-i386 -B i386 1.in font_binary.o`命令就可以制作成x86下的.o文件了,现在成功了90%

在makefile中作为.o添加一条target,然后链接进入kernel.bin

![2](/images/Selection022.png)

make后查看kernel.bin的符号表是否生成了对应的全局符号

![3](/images/Selection023.png)

左边是这3个符号的值,

`c00091c0`表示二进制文件(font字体的像素字节)生成到虚拟地址为`0xc00091c0`

`c000a1c0`结束的虚拟地址

`0x1000`二进制文件的大小(正好是16\*256 = 4096)

### 用代码测试`0xc000a1c0`处开始的值

> 以前是将这3个符号声明为char 类型,有点问题,但是我发现声明为xxx []比较好

![4](/images/Selection017.png)

查看的是第0x12和第0x13个字节的值

原本的二进制文件:

![5](/images/Selection018.png)

bochs中运行结果(没有在图形下debug是还没做图形下的debug\_print功能):

![6](/images/Selection019.png)

> 完全一致,将二进制字库文件插入kernel.bin中成功!

### 使用新增的ascii字体的效果

![7](/images/Selection020.png)

### 代码目录[github](https://github.com/luchao2424631502/os2/tree/graphics/graphics)
