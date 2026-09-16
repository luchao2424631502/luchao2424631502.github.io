---
title: Orange‘s:FAT12认识和Boot引导
date: '2020-07-12 11:02:00'
permalink: 2020/07/12/csdn/Orange‘s!FAT12认识和Boot引导/
categories:
- 系统与底层
- 自制操作系统
tags:
- 于渊    操作系统  Orange S
---

> 前2章实验都是借助DOS提供保护模式环境来实验(因为在引导扇区512byte限制下提供不了保护模式),
>
> 为了让OS进入保护模式而引导扇区又不能解决,通过boot把磁盘中的loader加载进内存,然后通过loader进入保护模式并且加载kernel
>
> 这样就突破了512byte的限制

boot->loader->kernel

此书将软盘做成FAT12格式

1. bximage制作1.44MB大小的fd
2. dd写入符合规则(BPB)的引导扇区则软盘被做成FAT12格式,(被dos或者linux识别后自动补充根目录)

## FAT12

1. 引导扇区格式  
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200712110144463.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

2. FAT12软盘结构:  
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200712110158404.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)
3. 目录区条目结构  
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200712110215233.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTUx,size_16,color_FFFFFF,t_70#pic_center)

---

boot主要思路:

**把根目录区读取到内存中遍历找到LOADER.BIN文件名目录项,得到数据区开始的簇数**

**根据数据区簇数在FAT表中找到(FAT读到OffsetLoader前4k内存处)下一个簇数,把loader读取到OffsetLoader处(覆盖掉了没作用的根目录表)**

**转跳到Loader**

---

磁盘寻址方式:

不是在磁道上连续的,而是先把每一个面上下对应的扇区从上到下读(磁头),然后到下一个扇区继续,然后换磁道

---

因为FAT表一项12字节,根据从数据区得到的所在扇区的**偏移个数**要转换到8字节是**偏移多少个**,偶数个数恰好开头就是需要的12byte，奇数个数距离真正的FAT项还差8byte,**又因为读到ax 16bit寄存器中**,所以偶数去掉最后最后4Byte,奇数去掉开头不属于自己的4byte

> 读取2个连续扇区因为FAT项可能跨扇区

---

#### 在求FAT项目时在OffsetLoader前4K出将FAT表读取内存,讲道理4K大小是不够的,FAT表9扇区4.5K大小,但是loader不会太大,4K应该足够 (???

---

loader载入内存后,boot完成工作,控制转移给Loader

---

### 将pmtest9.asm作为loader运行

#### 1.为什么OffsetLoader=0100h,Loader.asm org=0100h？

我尝试改小变为0x80h 段错误(段长度限制) ,但是变大为0x200h 没错?**这里为什么不能同时修改偏移地址我还不清楚**

**偏移100h是为了兼容DOS的.COM文件直接运行**

修改一下makefile后运行

```makefile
BOOT:=boot.asm
LDR:=pmtest9.asm
BOOT_BIN:=$(subst .asm,.bin,$(BOOT))
LDR_BIN:=loader.bin

everything:$(BOOT_BIN) $(LDR_BIN)
	dd if=$(BOOT_BIN) of=/work/a.img bs=512 count=1 conv=notrunc
	sudo mount -o loop /work/a.img /mnt/
	sudo cp $(LDR_BIN) /mnt/ -v
	sudo umount /mnt/


$(BOOT_BIN):$(BOOT)
	nasm $< -o $@
$(LDR_BIN):$(LDR)
	nasm $(LDR) -o $(LDR_BIN)
```

[boot.asm](https://github.com/luchao2424631502/os/tree/master/boot)

---

有关问题:

1. [一个操作系统的实现–freedos中edit问题](https://blog.csdn.net/baidu_33268787/article/details/51974132)
2. [NASM org 0100h](https://blog.csdn.net/ruyanhai/article/details/7177904)
