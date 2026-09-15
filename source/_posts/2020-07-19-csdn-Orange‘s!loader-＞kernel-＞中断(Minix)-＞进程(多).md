---
title: Orange‘s:loader-＞kernel-＞中断(Minix)-＞进程(多)
date: '2020-07-19 11:12:00'
permalink: 2020/07/19/csdn/Orange‘s!loader-＞kernel-＞中断(Minix)-＞进程(多)/
categories:
- 编写操作系统之路
---

#### 从kernel.bin中根据elf文件格式执行内核

加载kernel.bin步骤和加载loader.bin步骤一样,将kernel.bin加载到内存后,

因为kernel的编译参数`-Ttext 0x30400`指定了程序入口(可以在`/boot/include/load.inc`中修改,并且修改kernel编译参数`-Ttext`就能加载到自己指定的内存地址处).

因为\*\*kernel被编译成elf格式,而非纯二进制,那么根据elf格式在把kernel程序段加载到内存中(program header中指定了,本书并未选择作内存映射,而是直接根据编译结果),\*\*如果是纯二进制的话,也是应该加载到内存并且找到kernel执行入口处,控制转移就行了

---

此时esp和GDT还在loader中

把IDT和GDT以及一些全局变量定义在`global.c`中

---

### gcc编译除去内建函数

就是自己写的函数和printf这种函数重名,指定编译参数来避免冲突,不包含内建函数（内）

```c
int printf(int i);
int printf(int i)
{
	return i;
}
int main()
{
	return printf(10);
}
```

gcc默认选项是`built-in function`,指定`-fno-builtin`或者只需要指定某个函数名`-fno-builtin-printf`,解决冲突`gcc -fno-builtin test.c -o test`

---

kernel的主要作用就是和c一起设置GDT和IDT,

---

#### 内核-添加中断:

整体思路:**在kernel.asm中编写每个中断处理例(因为 门描述符 需要偏移地址,),其他的函数通过c编写,添加cpu中断异常(每个单独写) -> 8259A15个硬件中断(nasm宏实现) -> 向8259A写OCW开启键盘中断测试**

在内核完善中断时,因为门描述符填充处理例程的物理地址(平坦模式),在kernel/kernel.asm中写基本中断能够确定中断函数所在位置(kernel开头处),填IDT中例程偏移地址和disp交给c来做

[kernel/](https://github.com/luchao2424631502/os/tree/master/kernel)

#### 从kernel.bin中根据elf文件格式执行内核

加载kernel.bin步骤和加载loader.bin步骤一样,将kernel.bin加载到内存后,

因为kernel的编译参数`-Ttext 0x30400`指定了程序入口(可以在`/boot/include/load.inc`中修改,并且修改kernel编译参数`-Ttext`就能加载到自己指定的内存地址处).

因为\*\*kernel被编译成elf格式,而非纯二进制,那么根据elf格式在把kernel程序段加载到内存中(program header中指定了,本书并未选择作内存映射,而是直接根据编译结果),\*\*如果是纯二进制的话,也是应该加载到内存并且找到kernel执行入口处,控制转移就行了

---

此时esp和GDT还在loader中

把IDT和GDT以及一些全局变量定义在`global.c`中

---

### gcc编译除去内建函数

就是自己写的函数和printf这种函数重名,指定编译参数来避免冲突,不包含内建函数（内）

```c
int printf(int i);
int printf(int i)
{
	return i;
}
int main()
{
	return printf(10);
}
```

gcc默认选项是`built-in function`,指定`-fno-builtin`或者只需要指定某个函数名`-fno-builtin-printf`,解决冲突`gcc -fno-builtin test.c -o test`

---

kernel的主要作用就是和c一起设置GDT和IDT,

---

#### 内核-添加中断:

整体思路:**在kernel.asm中编写每个中断处理例(因为 门描述符 需要偏移地址,),其他的函数通过c编写,添加cpu中断异常(每个单独写) -> 8259A15个硬件中断(nasm宏实现) -> 向8259A写OCW开启键盘中断测试**

在内核完善中断时,因为门描述符填充处理例程的物理地址(平坦模式),在kernel/kernel.asm中写基本中断能够确定中断函数所在位置(kernel开头处),填IDT中例程偏移地址和disp交给c来做

[kernel/](https://github.com/luchao2424631502/os/tree/master/kernel)

#### OS的第一个进程:

​ 由kernel进程提前填好进程表信息以及TSS和进程的LDT,通过iret实现r0->r1的转移,并且在打开栈中eflags的IF标志,r0->r1也开启了中断(kernel中设置8259A打开了时钟中断)

​ 中断重入: 如果在中断过程中发送EOI后,中断过程执行时间长,导致中断重入问题:(目前采取 全局变量暴力维护只允许一个中断存在,另一个进入后判断存在个数后退出)

​ **位于中断例程时,根据TSS的esp0此时位于进程表栈,如果通过中断来调度进程那么首先要切换到内核栈中**

​ **多进程**下中断退出前设置好TSS的esp0,给下次r1->r0使用

#### 添加进程,通过中断进行进程切换()

```
1. 通过`task_table`填写进程表信息(自动化添加进程,并且选择子权限),根据NR_TASKS提前在int_prot中初始化LDT描述符
 2. 目前的进程切换很简单:中断一次切换到下一个进程:
```

3. 添加进程暂时通过修改

   > 1. 在global.c中task\_table添加一项
   > 2. proc.h修改nr\_tasks,定义堆栈大小,修改stack\_size\_total
   > 3. proto.h添加函数声明

4. 修改中断,定义成宏,让所有中断解决重入和栈切换的问题,把设置中路处理例程封装起来,引入`irq_table`

---

到目前的思路:

|———-引导扇区中加载loader

|———-控制权给loader,加载kernel

|———-控制权跳到kernel,将loader中的GDT移动到kernel中

|———-init\_prot()

​ |———-初始化8259A

​ |———-初始化IDT

​ |———-初始化唯一TSS以及其描述符, 和(开始时第一个进程)多进程的LDT描述符

|———-kernel\_main()

​ |———-根据task\_table[]初始化进程表,(regs,寄存器选择子以及权限等)

​ |———-开启时钟中断,指定时钟中断处理程序

​ |———-restart():正式从kernel进入到第一个进程(本质上时r0 -> r1的转换)

|———-多进程开始运转(目前3个,并且通过时钟中断进行调度,(简单的顺序调度),并且中断重入已解决)

[整体](https://github.com/luchao2424631502/os)
