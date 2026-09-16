---
title: Orange‘s:保护模式小总结
date: '2020-07-10 18:21:00'
permalink: 2020/07/10/csdn/Orange‘s!保护模式小总结/
categories:
- 系统与底层
- 自制操作系统
---

Orange’s的中断方式我看了看和linux0.1x是一样的,时钟中断实验:

1. 回到实模式目前我认为没意义但是注意:

   > a. 要求段寄存器高速缓冲器的属性(段长度)提前设置号
   >
   > b. cs通过在32bit代码段转跳到16bit代码段来设置(描述符)
   >
   > c. 直接修改jmp编译后指令的段地址
   >
   > d. 修改的8259A和IDTR需要恢复原样
2. 开启分页后人为使物理地址和线性地址对应,好操作
3. 通过宏填出描述符后,认为修改段基地址是很好的方法,宏定义各种描述符属性
4. 选择子起始就是偏移地址,因为 第几个\*4b = 偏移地址
5. 8259A 设置

```plain
%include "pm.inc"

PageDirBase0    equ 200000h     ;2M
PageTblBase0    equ 201000h     ;2M + 4k
PageDirBase1    equ 210000h     ;2M + 64K
PageTblBase1    equ 211000h     ;2M + 64K + 4K

LinearAddrDemo  equ 00401000h   
ProcFoo         equ 00401000h
ProcBar         equ 00501000h
ProcPagingDemo  equ 00301000h   ;调用LinearAddrDemo处的函数

org 0100h       ;DOS环境下运行
    jmp LABEL_BEGIN

[SECTION .gdt]
    LABEL_GDT:          Descriptor  0,0,0
    LABEL_DESC_NORMAL   Descriptor  0,0ffffh,DA_DRW
    LABEL_DESC_FLAT_C:  Descriptor  0,0fffffh,DA_CR|DA_32|DA_LIMIT_4K
    LABEL_DESC_FLAT_RW: Descriptor  0,0fffffh,DA_DRW|DA_LIMIT_4K
    LABEL_DESC_CODE32:  Descriptor  0,SegCode32Len-1,DA_CR|DA_32
    LABEL_DESC_CODE16:  Descriptor  0,0ffffh,DA_C
    LABEL_DESC_DATA:    Descriptor  0,DataLen - 1,DA_DRW
    LABEL_DESC_STACK:   Descriptor  0,TopOfStack,DA_DRWA|DA_32
    LABEL_DESC_VIDEO:   Descriptor  0b8000h,    0ffffh,DA_DRW

    GdtLen      equ $ - LABEL_GDT
    GdtPtr      dw GdtLen - 1
                dd 0 

    SelectorNormal  equ LABEL_DESC_NORMAL   -   LABEL_GDT
    SelectorFlatC   equ LABEL_DESC_FLAT_C   -   LABEL_GDT
    SelectorFlatRW  equ LABEL_DESC_FLAT_RW  -   LABEL_GDT
    SelectorCode32  equ LABEL_DESC_CODE32   -   LABEL_GDT
    SelectorCode16  equ LABEL_DESC_CODE16   -   LABEL_GDT
    SelectorData    equ LABEL_DESC_DATA     -   LABEL_GDT 
    SelectorStack   equ LABEL_DESC_STACK    -   LABEL_GDT
    SelectorVideo   equ LABEL_DESC_VIDEO    -   LABEL_GDT

[SECTION .data1]
ALIGN 32
[BITS 32]
LABEL_DATA:
    _szPMMessage:			db	"In Protect Mode now. ^-^", 0Ah, 0Ah, 0
    _szMemChkTitle:         db  "BaseAddrL BaseAddrH LengthLow LengthHigh   Type", 0Ah, 0
    _szRAMSize              db  "RAM size:", 0
    _szReturn               db  0Ah,0
;
    _wSPValueInRealMode     dw 0 
    _dwMCRNumber:           dd 0
    _dwDispPos:             dd (80 * 6 + 0) * 2
    _dwMemSize:             dd 0
    _ARDStruct:
        _dwBaseAddrLow:     dd 0
        _dwBaseAddrHigh:    dd 0
        _dwLengthLow:       dd 0
        _dwLengthHigh:      dd 0
        _dwType:            dd 0
    _PageTableNumber        dd 0
        
    _MemChkBuf: times 256 db 0 

    szPMMessage     equ _szPMMessage - $$
    szMemChkTitle   equ _szMemChkTitle - $$
    szRAMSize       equ _szRAMSize - $$
    szReturn        equ _szReturn - $$
    dwDispPos       equ _dwDispPos - $$
    dwMemSize       equ _dwMemSize - $$
    dwMCRNumber     equ _dwMCRNumber - $$
    ARDStruct       equ _ARDStruct  - $$
        dwBaseAddrLow   equ _dwBaseAddrLow - $$
        dwBaseAddrHigh equ _dwBaseAddrHigh - $$
        dwLengthLow     equ _dwLengthLow - $$
        dwLengthHigh    equ _dwLengthHigh - $$
        dwType          equ _dwType -   $$
    MemChkBuf       equ _MemChkBuf - $$
    PageTableNumber equ _PageTableNumber - $$

    DataLen equ $ - LABEL_DATA

[SECTION .idt]
ALIGN 32
[BITS 32]
LABEL_IDT:
%rep 32
    Gate    SelectorCode32, SpuriousHandler,    0,  DA_386IGate
%endrep
    .020h:  Gate SelectorCode32,    ClockHandler,   0,  DA_386IGate
%rep 95
    Gate    SelectorCode32, SpuriousHandler,    0,  DA_386IGate
%endrep 
    .80h:   Gate SelectorCode32,    UserIntHandler, 0,DA_386IGate

IdtLen  equ $ - LABEL_IDT
IdtPtr  dw IdtLen - 1
        dd 0 

;全局堆栈段
[SECTION .gs]
ALIGN 32
[BITS 32]
LABEL_STACK:
    times 512 db 0
TopOfStack  equ $ - LABEL_STACK - 1

[SECTION .s16]
[BITS 16]
LABEL_BEGIN:
    mov ax,cs 
    mov ds,ax 
    mov es,ax 
    mov ss,ax 
    mov sp,0100h

    mov [LABEL_GO_BACK_TO_REAL + 3],ax 
    mov [_wSPValueInRealMode],sp 

    mov ebx,0
    mov di,_MemChkBuf
.loop:
    mov eax,0E820h
    mov ecx,20 
    mov edx,0534D4150h
    int 15h 
    jc LABEL_MEM_CHK_FAIL   ;cf=1表示存在错误
    add di,20 
    inc dword [_dwMCRNumber]
    cmp ebx,0               ;是不是最后一个
    jne .loop 
    jmp LABEL_MEM_CHK_OK
LABEL_MEM_CHK_FAIL:
    mov dword [_dwMCRNumber],0
LABEL_MEM_CHK_OK:

    ;16bit代码段段 基础地址
    mov ax,cs 
    movzx eax,ax 
    shl eax,4
    add eax,LABEL_SEG_CODE16
    mov word [LABEL_DESC_CODE16 + 2],ax 
    shr eax,16
    mov byte [LABEL_DESC_CODE16 + 4],al 
    mov byte [LABEL_DESC_CODE16 + 7],ah 

    ;32bit代码段 基础地址
    xor eax,eax 
    mov ax,cs 
    shl eax,4
    add eax,LABEL_SEG_CODE32
    mov word [LABEL_DESC_CODE32 + 2],ax 
    shr eax,16
    mov byte [LABEL_DESC_CODE32 + 4],al 
    mov byte [LABEL_DESC_CODE32 + 7],ah 

    ;数据段描述符 基地址
    xor eax,eax 
    mov ax,ds 
    shl eax,4
    add eax,LABEL_DATA
    mov word [LABEL_DESC_DATA + 2],ax 
    shr eax,16
    mov byte [LABEL_DESC_DATA + 4],al
    mov byte [LABEL_DESC_DATA + 7],ah 

    ;栈段描述符
    xor eax,eax 
    mov ax,ds 
    shl eax,4
    add eax,LABEL_STACK
    mov word [LABEL_DESC_STACK + 2],ax 
    shr eax,16 
    mov byte [LABEL_DESC_STACK + 4],al 
    mov byte [LABEL_DESC_STACK + 7],ah 

    ;GDTR
    xor eax,eax 
    mov ax,ds 
    shl eax,4
    add eax,LABEL_GDT
    mov dword [GdtPtr + 2],eax 

    ;加载IDTR作准备
    xor eax,eax 
    mov ax,ds 
    shl eax,4
    add eax,LABEL_IDT
    mov dword [IdtPtr + 2],eax 

    ;加载GDTR
    lgdt [GdtPtr]

    ;关闭实模式下中断
    cli 

    ;加载保护模式下 中断向量表
    lidt [IdtPtr]

    in al,92h 
    or al,00000010b
    out 92h,al 

    mov eax,cr0 
    or eax,1 
    mov cr0,eax 

    jmp dword SelectorCode32:0

LABEL_REAL_ENTRY:
    mov ax,cs 
    mov ds,ax 
    mov es,ax 
    mov ss,ax 

    mov sp,[_wSPValueInRealMode];实模式,直接用地址

    in al,92h 
    and al,11111101b
    out 92h,al 

    sti 

    mov ax,4c00h
    int 21h

[SECTION .s32]
[BITS 32]

LABEL_SEG_CODE32:
    mov ax,SelectorData
    mov ds,ax 
    mov es,ax 
    mov ax,SelectorVideo
    mov gs,ax 

    mov ax,SelectorStack
    mov ss,ax 

    mov esp,TopOfStack

    call Init8259A
    int 080h                ;调用80h中断

    sti                     ;IF=0
    jmp $

    ;显示
    push szPMMessage
    call DispStr
    add esp,4 

    push szMemChkTitle
    call DispStr
    add esp,4 

    call DispMemSize            ;显示内存信息

    call PagingDemo             ;演示改变页目录效果
    
    jmp SelectorCode16:0

;Init8259A
Init8259A:
    ;ICW1:设置为级联和需要ICW4
    mov al,011h 
    out 020h,al 
    call io_delay 

    out 0A0h,al 
    call io_delay

    ;ICW2:重新设置对应的向量号
    mov al,020h 
    out 021h,al 
    call io_delay

    mov al,028h 
    out 0A1h,al 
    call io_delay

    ;ICW3:设置主从片对应的IR口
    mov al,004h 
    out 021h,al 
    call io_delay

    mov al,002h 
    out 0A1h,al 
    call io_delay

    ;ICW4:设置模式(和Linux0.11一样)
    mov al,001h 
    out 021h,al 
    call io_delay

    out 0A1h,al 
    call io_delay

    ;8259A已经开始工作,OCW操作它
    mov al,11111110b    ;主片开始定时中断
    out 021h,al 
    call io_delay

    mov al,11111111b    ;屏蔽所有从片中断
    out 0A1h,al
    call io_delay

    ret 

io_delay:
    nop
    nop 
    nop 
    nop 
    ret 

;时钟中断处理程序
_ClockHandler:
ClockHandler    equ _ClockHandler - $$
    inc byte [gs:((80 * 0 + 70) * 2)]
    mov al,20h 
    out 20h,al          ;发送EOI结束中断
    iretd 

_UserIntHandler:
UserIntHandler  equ _UserIntHandler - $$
    mov ah,0Ch 
    mov al,'I'
    mov [gs:((80 * 0 + 70) * 2)],ax 
    iretd 

;中断处理程序
_SpuriousHandler:
    SpuriousHandler equ _SpuriousHandler - $$ 
    mov ah,0Ch 
    mov al,'!'
    mov [gs:((80 * 0 + 75) * 2)],ax 
    jmp $
    iretd 

;启动分页机制
SetupPaging:
    xor edx,edx 
    mov eax,[dwMemSize]         ;eax=RAM实际大小
    mov ebx,400000h             ;4M
    div ebx                     ;实际内存需要多少个页表
    mov ecx,eax 
    test edx,edx 
    jz .no_remainder            ;没有余数
    inc ecx                     ;有余数就多来一个页表
.no_remainder:
    mov [PageTableNumber],ecx   ;暂存页表个数

;初始化ecx个页目录项
    mov ax,SelectorFlatRW      ;
    mov es,ax                   ;es=页目录表首地址
    mov edi,PageDirBase0        ;平坦模式
    xor eax,eax 
    mov eax,PageTblBase0 | PG_P | PG_USU | PG_RWW 
.1:
    stosd                       ;eax存放在es:edi
    add eax,4096
    loop .1 

    ;初始化所有页表
    mov eax,[PageTableNumber]   ;实际页表个数
    mov ebx,1024 
    mul ebx                     ;eax * ebx = 页表项个数
    mov ecx,eax 
    mov edi,PageTblBase0
    xor eax,eax 
    mov eax, PG_P | PG_USU | PG_RWW 
.2:
    stosd                   ;eax->es:edi edi+4
    add eax,4096
    loop .2 

    mov eax,PageDirBase0    ;页目录表基地址
    mov cr3,eax             ;加载PDTR
    mov eax,cr0             ;开启cr0的分页
    or eax,80000000h
    mov cr0,eax 

    jmp short .3 
.3:
    nop 

    ret 
;分页机制启动完毕

;测试分页机制:
PagingDemo:
    mov ax,cs 
    mov ds,ax 
    mov ax,SelectorFlatRW
    mov es,ax 

    push LenFoo         ;要复制的函数长度
    push OffsetFoo      ;源地址
    push ProcFoo        ;目的地
    call Memcpy
    add esp,12          ;手动清栈

    push LenBar
    push OffsetBar
    push ProcBar        
    call Memcpy
    add esp,12 

    push LenPagingDemoAll
    push OffsetPagingDemoProc
    push ProcPagingDemo ;目的地址
    call Memcpy
    add esp,12 

    mov ax,SelectorData
    mov ds,ax 
    mov es,ax 

    call SetupPaging    ;启动分页

    call SelectorFlatC:ProcPagingDemo;远调用
    call PSwitch
    call SelectorFlatC:ProcPagingDemo

    ret 
;切换页表  
PSwitch:
    mov ax,SelectorFlatRW
    mov es,ax 
    mov edi,PageDirBase1    ;新页目录偏移地址
    xor eax,eax 
    mov eax,PageTblBase1 | PG_P | PG_USU | PG_RWW
    mov ecx,[PageTableNumber]
.1:
    stosd 
    add eax,4096
    loop .1 

    mov eax,[PageTableNumber]
    mov ebx,1024 
    mul ebx 
    mov ecx,eax             ;页表个数
    mov edi,PageTblBase1    ;新页表偏移地址
    xor eax,eax 
    mov eax,PG_P | PG_USU | PG_RWW
.2:
    stosd 
    add eax,4096
    loop .2 

    ;得到页表项目地址(并且页表的总起始地址已经知道)
    mov eax,LinearAddrDemo
    shr eax,22 
    mov ebx,4096            ;*4KB得到页表基于基地址的偏移地址
    mul ebx 
    mov ecx,eax 
    mov eax,LinearAddrDemo
    shr eax,12 
    and eax,03FFh           ;得到中间10bit
    mov ebx,4
    mul ebx                 ;得到页表项在页表中的偏移地址
    
    add eax,ecx             ;页表中偏移地址+页表的偏移地址
    add eax,PageTblBase1    ;+页表总的基地址 = 页表的偏移地址
    mov dword [es:eax],ProcBar | PG_P | PG_USU | PG_RWW

    mov eax,PageDirBase1
    mov cr3,eax             ;页目录寄存器指向新页目录表

    jmp short .3 
.3:
    nop 

    ret 

PagingDemoProc:
    OffsetPagingDemoProc    equ PagingDemoProc - $$
    mov eax,LinearAddrDemo
    call eax                ;进调用
    retf 
LenPagingDemoAll    equ $ - PagingDemoProc

;两个显示各自名字的函数
foo:
    OffsetFoo   equ foo - $$
    mov ah,0ch                      ;0000黑色 1100红色
    mov al,'F'
    mov [gs:((80 * 17 + 0) * 2)],ax 
    mov al,'o'
    mov [gs:((80 * 17 + 1) * 2)],ax 
    mov [gs:((80 * 17 + 2) * 2)],ax 
    ret 
    LenFoo      equ $ - foo 

bar:
    OffsetBar   equ bar - $$
    mov ah,0Ch 
    mov al,'B'
    mov [gs:((80 * 18 + 0) * 2)],ax 
    mov al,'a'
    mov [gs:((80 * 18 + 1) * 2)],ax 
    mov al,'r'
    mov [gs:((80 * 18 + 2) * 2)],ax 
    ret 
    LenBar      equ $ - bar 

DispMemSize:
    push esi 
    push edi 
    push ecx 

    mov esi,MemChkBuf
    mov ecx,[dwMCRNumber];得到了多少个数据结构
.loop:
    mov edx,5;显示结构中的5个成员
    mov edi,ARDStruct
.1:
    push dword [esi]    ;将读取的信息打印出来
    call DispInt
    pop eax 
    stosd               ;填写到es:edi中
    add esi,4
    dec edx 
    cmp edx,0
    jnz .1              ;执行5次 
    call DispReturn     ;打印换行
    cmp dword [dwType],1;判断内存类型
    jnz .2              ;转跳到.2说明是被占用的
    mov eax,[dwBaseAddrLow]
    add eax,[dwLengthLow]
    cmp eax,[dwMemSize] ;求最大的可用内存上限
    jb .2 
    mov [dwMemSize],eax 
.2:
    loop .loop 

    call DispReturn
    push szRAMSize
    call DispStr        ;打印RAM字符串
    add esp,4 

    push dword [dwMemSize]
    call DispInt        ;RAM大小
    add esp,4 

    pop ecx 
    pop edi 
    pop esi 
    ret 

%include "lib.inc"

SegCode32Len    equ $ - LABEL_SEG_CODE32

[SECTION .s16code]
ALIGN 32
[BITS 16]
LABEL_SEG_CODE16:
    mov ax,SelectorNormal
    mov ds,ax 
    mov es,ax 
    mov fs,ax 
    mov gs,ax 
    mov ss,ax 

    mov eax,cr0 
    and eax,7FFFFFFEh   ;关闭分页和保护模式
    mov cr0,eax 

LABEL_GO_BACK_TO_REAL:
    jmp 0:LABEL_REAL_ENTRY

Code16Len   equ $ - LABEL_SEG_CODE16
```

通过DOS提供保护模式环境(那么此时已经不是裸机环境,)

```makefile
#写入软盘的makefile
SRC:=pmtest9.asm
BIN:=$(subst .asm,.bin,$(SRC))

.PHONY : everything

everything : $(BIN)
	sudo mount -o loop /work/pm.img /mnt/
	sudo cp $(BIN) /mnt/ -v
	sudo umount /mnt/

$(BIN) : $(SRC)
	nasm $< -o $@
# $<第一个依赖文件 $@目标文件
```

杂:

1. cr0.wp位,与页表的R/W位有关

   > Supervisor(CPL < 3)的写保护位,Wp=1,Supervisor不能写R/W没有置位的页
   >
   > ​ wp=0,Supervisor可以写任何页面
   >
   > 对于User (CPL = 3),无论wp是什么,都不能写R/W没有置位的页
   >
   > 所以WP对CPL<3的用户有效
2. [TLB原理](https://www.cnblogs.com/alantu2018/p/9000777.html)
3. Makefile中函数用法`$(<function> <arguments>)`

   例:

   `$(subst <from>,<to>,<test>)`,参数`,`分割

   [写Makefile](%5Bhttps://wiki.ubuntu.org.cn/%E8%B7%9F%E6%88%91%E4%B8%80%E8%B5%B7%E5%86%99Makefile:%E4%BD%BF%E7%94%A8%E5%87%BD%E6%95%B0%5D(https://wiki.ubuntu.org.cn/%E8%B7%9F%E6%88%91%E4%B8%80%E8%B5%B7%E5%86%99Makefile:%E4%BD%BF%E7%94%A8%E5%87%BD%E6%95%B0))
4. .PHONY: Targets

   直接假设目标每次都需要被更新,clean: rm xxx,如果存在clean文件,那么clean始终是最新的
5. ndisasm反汇编,例如引导扇区代码org 0x7c00h

   `ndisasm -o7c00h boot`
6. nasm预处理 [nasm预处理](https://blog.51cto.com/cobbage/982220)

   %rep 循环次数 %endrep
7. IOPL和IO bitmap的关系

   IO敏感指令CPL <= IOPL时才能执行

   当CPL>IOPL时则根据TSS的IO bitmap对应的IO端口是否打开

   IO bitmap地址是已TSS基地址的偏移,大于TSS段界限则无效
