---
title: IA-32架构 (Intel Architecture 32-bit)概览 和 8086小总结
date: '2020-05-01 17:13:00'
permalink: 2020/05/01/csdn/IA-32架构 (Intel Architecture 32-bit)概览 和 8086小总结/
categories:
- X86实模式和保护模式
---

### IA-32架构 (Intel Architecture 32-bit)概览 和 8086小总结

#### 寄存器

##### 8086

> 1. 8个通用寄存器
>
> > `AX BX CX DX SI DI BP SP`
>
> 32bit处理器在此通用寄存器扩展到32bit
>
> `EAX EBX ECX EDX ESI EDI EBP ESP`
>
> 实模式下也可以使用,**但是`32bit`寄存器的高`16`位不可独立使用**
>
> 32bit处理器拥有自己的工作模式:**保护模式(使用32跟地址线,寻址范围4GB)**

##### 32bit

`EIP`扩展到32位那么可以访问到所以的内存地址,不在需要像8086一样分段访问,但是IA-32也是基于分段模型,依旧以段为段位访问内存

##### 平坦模式(`Flat Mode`)

因为`EIP`可以访问到所有内存地址,可不分段,段基址=`0x00000000`,长度=`4GB`

---

##### 段

8086下程序可以访问和修改不属于自己的内存地址,32bit下,加载程序要求:

**定义程序拥有的段,特权级别,类型的属性**,程序访问一个段时,处理器检查防止对内存的违规访问

8086的段寄存器`CS,SS,DS,ES`在32Bit下变成—>段选择器(选择要访问的段),段寄存器还包括一个不可见部分(即**描述符高速缓存器**)，给cpu提供了段的基地址+各种访问属性

32bit下新增2个段寄存器`FS`和`GS`

---

##### 基本工作模式

- 1982年处理器`80286`,16bit,但是又24根地址线(寻址16MB)，**首次提出保护模式概念**

1. 段寄存器不在是段地址(实际段地址位于描述符高速缓存器中,24bit) ,所以段可以位于内存中的任何地址，而8086中因为段地址转成实际内存地址要左移4位置(乘以16进制的10),所以段地址和16字节对齐
2. 偏移地址仍是16位,所以一个段最长不能超过64KB

---

3. 因为段长度的限制16位的保护模式很少人知道

- 1985年80386处理器,32跟地址线

1. 刚刚加电,处理器处于实模式,->经过设置才到保护模式
2. 除了保护模式,32bit处理器还提供 **虚拟8086模式(V86)**:

   IA-32处理器模拟成多个8086处理器并行工作,`V86`模式属于保护模式的一种,意义:当时兼容8086程序多有用,现在意义不大

##### 现代处理器结构特点

1. 多级流水线细分子任务
2. 已知寄存器由SRAM(静态),内存DRAM(通电刷新),在内存和处理器之间添加SRAM的高速缓存（**程序的局部性原理**）

   在高速缓存未命中的情况下,处理器在取得数据前必须重新装载高速缓存,**这段额外的时间等待从内存载入高速缓存 称为 不中惩罚**

   每款处理器的缓存可能核心共享的不一样,并且有多级高速缓存
3. 乱序执行

   指令拆成微指令同时执行
4. 寄存器重命名

   通用寄存器个数有限但是在cpu内部临时寄存器个数较多,多个指令中用到某寄存器且可以乱序执行,则用临时寄存器代替,最后临时寄存器的内容写回,**称为引退**
5. 分支目标预测

   当流水线中遇到一条转移指令,则后面的指令都无效,此时需要**清空流水线，转跳到目标地址重新开始流水线的执行**,流水线越长,用错误的分支填充流水线导致浪费的时间越多

   1996年Pentium Pro引入分支预测(`Branch prediction`):

   例如`loop`,第一次转跳时,在分支目标缓存器(`Branch target buffer`)记录当前指令的地址、分支目标地址、本次分支预测结果，下次执行时查看BTB，如果预测失败,清空流水线和BTB

---

#### 8086总结

- 分段内存管理机制:

  20根地址线,寻址能力`1MB`,16位寄存器不能满足,才有内存地址 = 段地址\*16+偏移地址.16位的偏移地址决定了一个段最大为64K,

> 外围设备的地址直接映射到内存中,读写IO端口=访问内存

---

理解书中通过写一个加载器理解内存机制

```c
app_lba_start equ 100 ;逻辑扇区号=100

SECTION mbr align=16 vstart=0x7c00

    mov ax,0
    mov ss,ax
    mov sp,ax

    mov ax,[cs:phy_base]
    mov dx,[cs:phy_base+0x02]
    mov bx,16
    div bx          ;求出加载程序的段基址
    mov ds,ax
    mov es,ax

    xor di,di
    mov si,app_lba_start    ;ds:si扇区地址
    xor bx,bx               ;ds:bx 内存地址
    call read_hard_disk_0       ;先读取第一个扇区到

    mov dx,[2]
    mov ax,[0]
    mov bx,512
    div bx
    cmp dx,0
    jnz @1
    dec ax
@1:
    cmp ax,0
    jz direct

    push ds
    mov cx,ax
@2:
    mov ax,ds
    add ax,0x20
    mov ds,ax

    xor bx,bx
    inc si
    call read_hard_disk_0
    loop @2

    pop ds

direct:
    mov dx,[0x08]
    mov ax,[0x06]
    call calc_segment_base
    mov [0x06],ax   ;实际段地址写回去

    mov cx,[0x0a]
    mov bx,0x0c
realloc:
    mov dx,[bx+0x02]
    mov ax,[bx]
    call calc_segment_base
    mov [bx],ax
    add bx,4
    loop realloc

    jmp far [0x04]
calc_segment_base:;由实际的内存地址计算段的基地址
    push dx

    add ax,[cs:phy_base]
    adc dx,[cs:phy_base+0x02]
    shr ax,4
    ror dx,4
    and dx,0xf000
    or ax,dx

    pop dx
    ret

read_hard_disk_0:

    push ax
    push bx
    push cx
    push dx

    mov dx,0x1f2
    mov al,1
    out dx,al           ;读写的扇区数量

    inc dx
    mov ax,si
    out dx,al           ;扇区号的低位

    inc dx
    mov al,ah
    out dx,al           ;扇区的高位

    inc dx
    mov ax,di
    out dx,al
    
    inc dx
    mov al,0xe0         ;LBA模式+主盘
    or al,ah
    out dx,al

    inc dx
    mov al,0x20
    out dx,al

.waits:;读取io接口的状态
    in al,dx
    and al,0x88
    cmp al,0x08
    jnz .waits

    mov cx,256
    mov dx,0x1f0

.readw:
    in ax,dx
    mov [bx],ax
    add bx,2
    loop .readw

    pop dx
    pop cx
    pop bx
    pop ax

    ret
    
phy_base dd 0x10000

times 510-($-$$) db 0
db 0x55,0xaa
```

程序:

```c
SECTION header vstart=0
    program_length  dd program_end

    code_entry      dw start
                    dd section.code_1.start
    realloc_tbl_len dw (header_end-code_1_segment)/4
    
    code_1_segment  dd section.code_1.start
    code_2_segment  dd section.code_2.start
    data_1_segment  dd section.data_1.start
    data_2_segment  dd section.data_2.start
    stack_segment   dd section.stack.start

    header_end:
SECTION code_1 align=16 vstart=0
put_string:
    mov cl,[bx]
    or cl,cl
    jz .exit
    call put_char
    inc bx
    jmp put_string
.exit:
    ret
put_char:
    push ax
    push bx
    push cx
    push dx
    push ds
    push es
;从索引寄存器中取出当前25*80字符模式的光标位置
    mov dx,0x3d4
    mov al,0x0e     ;索引寄存器偏移地址
    out dx,al
    
    mov dx,0x3d5
    in al,dx        ;光标 高 8位数据
    mov ah,al

    mov dx,0x3d4
    mov al,0x0f
    out dx,al
    mov dx,0x3d5
    in al,dx        ;ax中16位光标凑齐
    mov bx,ax

    cmp cl,0x0d     ;回车符号？
    jnz .put_0a     ;不是
    mov ax,bx       ;重定位到行首
    mov bl,80
    div bl
    mul bl
    mov bx,ax
    jmp .set_cursor

.put_0a:
    cmp cl,0x0a     ;换行符?
    jnz .put_other  ;不是,
    add bx,80
    jmp .roll_screen
.put_other:
    mov ax,0xb800
    mov es,ax
    shl bx,1
    mov [es:bx],cl

    shr bx,1
    add bx,1
.roll_screen:
    cmp bx,2000
    jl .set_cursor

    mov ax,0xb800
    mov ds,ax
    mov es,ax
    cld 
    mov si,0xa0
    mov di,0x00
    mov cx,1920
    rep movsw
    mov bx,3840
    mov cx,80
.cls:
    mov word [es:bx],0x0720
    add bx,2
    loop .cls

    mov bx,1920
.set_cursor:
    mov dx,0x3d4
    mov al,0x0e     ;偏移寄存器
    out dx,al

    mov dx,0x3d5
    mov al,bh       
    out dx,al       ;设置高位

    mov dx,0x3d4
    mov al,0x0f     ;偏移寄存器
    out dx,al

    mov dx,0x3d5
    mov al,bl
    out dx,al       ;设置低位

    pop es
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax

    ret

    start:
        mov ax,[stack_segment]
        mov ss,ax
        mov sp,stack_end

        mov ax,[data_1_segment]
        mov ds,ax
        
        mov bx,msg0
        call put_string

        push word [es:code_2_segment]
        mov ax,begin
        push ax

        retf
    continue:
        mov ax,[es:data_2_segment]
        mov ds,ax

        mov bx,msg1
        call put_string

        jmp $

SECTION code_2 align=16 vstart=0
    begin:
    push word [es:code_1_segment]
    mov ax,continue
    push ax

    retf
SECTION data_1 align=16 vstart=0
    msg0 db '  This is NASM - the famous Netwide Assembler. '
            db 'Back at SourceForge and in intensive development! '
            db 'Get the current versions from http://www.nasm.us/.'
            db 0x0d,0x0a,0x0d,0x0a
            db '  Example code for calculate 1+2+...+1000:',0x0d,0x0a,0x0d,0x0a
            db '     xor dx,dx',0x0d,0x0a
            db '     xor ax,ax',0x0d,0x0a
            db '     xor cx,cx',0x0d,0x0a
            db '  @@:',0x0d,0x0a
            db '     inc cx',0x0d,0x0a
            db '     add ax,cx',0x0d,0x0a
            db '     adc dx,0',0x0d,0x0a
            db '     inc cx',0x0d,0x0a
            db '     cmp cx,1000',0x0d,0x0a
            db '     jle @@',0x0d,0x0a
            db '     ... ...(Some other codes)',0x0d,0x0a,0x0d,0x0a
            db 0
SECTION data_2 align=16 vstart=0
    msg1 db '  The above contents is written by LeeChung. '
            db '2011-05-06'
            db 0
SECTION stack align=16 vstart=0
    resb 256
stack_end:

SECTION trail align=16
program_end:
```

加载器放在主引导记录中,开机载入内存`0x7c00:0`,加载位于磁盘逻辑扇区100的程序到内存`0x10000`处执行

- 无论用masm或者nasm编译,注意程序编译出来的地址从0开始,在nasm中用vstart指定段内数据标号的偏移地址起始地址

---

参考：  
《X86实模式到保护模式》  
《汇编语言》
