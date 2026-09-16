---
title: Orange‘s chapter10缺少的elf.h文件定义
date: '2020-09-15 20:28:00'
permalink: 2020/09/15/csdn/Orange‘s chapter10缺少的elf.h文件定义/
categories:
- 系统与底层
- 自制操作系统
---

#### Orange’s操作系统源码chapter 10,缺少的elf.h文件以及get\_kernel\_map()函数

1. elf.h只用到elf\_header和section\_header,以及魔数 (**写出部分定义就可以,剩下的没用**)

   ```cpp
#ifndef _ORANGES_ELF_H_
#define _ORANGES_ELF_H_

typedef u32 Elf32_Word,Elf32_Addr,Elf32_Off;
typedef u16 Elf32_Half;

/* ELF header */
typedef struct
{
    unsigned char e_ident[16];
    Elf32_Half      e_type;
    Elf32_Half      e_machine;
    Elf32_Word      e_version;
    Elf32_Addr      e_entry;
    Elf32_Off       e_phoff;
    Elf32_Off       e_shoff;
    Elf32_Word      e_flags;
    Elf32_Half      e_ehsize;
    Elf32_Half      e_phentsize;
    Elf32_Half      e_phnum;
    Elf32_Half      e_shentsize;
    Elf32_Half      e_shnum;
    Elf32_Half      e_shstrndx;
}Elf32_Ehdr; 

/* program header程序表头 (段描述头) */
typedef struct
{
    Elf32_Word      p_type;
    Elf32_Off       p_offset;
    Elf32_Addr      p_vaddr;
    Elf32_Addr      p_paddr;
    Elf32_Word      p_filesz;
    Elf32_Word      p_memsz;
    Elf32_Word      p_flags;
}Elf32_Phdr;

/* section header节表头 */
typedef struct 
{
    Elf32_Word      sh_name;
    Elf32_Word      sh_type;
    Elf32_Word      sh_flags;
    Elf32_Addr      sh_addr;
    Elf32_Off       sh_offset;
    Elf32_Word      sh_size;
    Elf32_Word      sh_link;
    Elf32_Word      sh_info;
    Elf32_Word      sh_addralign;
    Elf32_Word      sh_entsize;
}Elf32_Shdr;

/* 定义elf魔数 */
// #define ELFMAG  0x464c457f
#define ELFMAG  1179403647
/* 定义elf mag长度 */
#define SELFMAG 4

/* sh_type字段定义 */
#define SHT_NULL        0
#define SHT_PROGBITS    1
#define SHT_SYMTAB      2
#define SHT_STRTAB      3
#define SHT_RELA        4
#define SHT_HASH        5
#define SHT_DYNAMIC     6
#define SHT_NOTE        7
#define SHT_NOBITS      8
#define SHT_REL         9
#define SHT_SHLIB       10
#define SHt_DYNSYM      11

/* sh_falgs字段定义 */
#define SHF_WRITE       0x1
#define SHF_ALLOC       0x2
#define SHF_EXECINSTR   0x4
#define SHF_MASKPROC    0xF0000000

#endif
```
   > 参考[ELF文件格式](https://blog.csdn.net/xuehuafeiwu123/article/details/72963229)
   >
   > ​ [Xbook2 elf.h](https://gitee.com/hzc1998/xbook2/blob/master/src/include/xbook/elf32.h)
2. 自定义的memcmp(,,)第2个参数是void\*,所以把宏改一下

   ```c
/* 解析内核文件,获取内核镜像的内存范围 */
int get_kernel_map(unsigned int *b,unsigned int *l)
{
    struct boot_params bp;
    get_boot_params(&bp);

    /* ELF header */
    Elf32_Ehdr *elf_header = (Elf32_Ehdr*)(bp.kernel_file);
    
    unsigned int temp = ELFMAG;
    /* 确保kernel file应该是ELF格式 */
    if (memcmp(elf_header->e_ident,(void*)&temp,SELFMAG) != 0)
        return -1;

    *b = ~0;
    unsigned int t = 0;
    int i;
    for (i=0; i<elf_header->e_shnum; i++)
    {
        /* 拿到每一个section header项 */
        Elf32_Shdr* section_header = 
            (Elf32_Shdr*)(bp.kernel_file + 
                            elf_header->e_shoff + 
                            i * elf_header->e_shentsize);
        
        /* 判断此段是否需要载入内存 */
        if (section_header->sh_flags & SHF_ALLOC)
        {
            int bottom  = section_header->sh_addr;
            int top     = section_header->sh_addr+section_header->sh_size;

            if (*b > bottom)
                *b = bottom;
            if (t < top)
                t = top; 
        }
    }
    assert(*b < t);
    *l = t - *b - 1;

    return 0;
}
```
   > 因为给出的源代码并没有elf.h的定义但是又使用了,也不知道为什么,所以自己改了改

   #### [上传到Orange’s无问题源码](https://github.com/luchao2424631502/os)
