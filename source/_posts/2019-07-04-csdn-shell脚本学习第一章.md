---
title: shell脚本学习第一章
date: '2019-07-04 19:54:00'
permalink: 2019/07/04/csdn/shell脚本学习第一章/
categories:
- 工具与效率
- Shell与命令行
---

shell脚本的开发周期:

1. 在命令行上测试,
2. 放入独立的脚本，
3. 设置权限

例如:

```bash
cat > nusers
who | wc -l
ctrl+D
chmod +x nusers
./nusers
```

- shell 会沿着路径$PATH(环境变量)来寻找命令  
  $PATH是一个以冒号分割的目录列表  
  `echo $PATH`
- 自己的脚本最好用自己的 `bin` 目录来存放,通过加入到`$PATH`中的列表来让`shell`自动找到它们
- 写脚本第一句话`#!/bin/bash`表示此脚本用什么解释器来解释,`#!`是特殊标识符

1. 变量(`variable`)

   > 直接赋值  
   > `myvar=this_is_a_long_string_that_does_not_mean_much`
   >
   > 中间有空格需要引号
   >
   > **取出变量的值需要在变量名称前面加上`$\$$`字符**
   >
   > 变量给变量赋值  
   > `oldname=$first`
   >
   > 加`""`使得字符串变量连接起来`fullname="$first $second $third"`  
   > `echo $fullname`
2. 访问shell脚本的参数  
   `who | grep root`  
   将此命令放入脚本中,抽象成参数,那么每次都能快速查到到`who`中的某位用户  
   `echo first argument is $1`  
   `echo tenth argument is ${10}`  
   参数超过9要将数字框起来

   ```python
cat > finduser
#! /bin/sh
# 查询用户登录
who | grep $1

chmod +x finduser #脚本权限
./finduser root #执行脚本
```
3. 命令的执行跟踪(`execution tracing`)  
   `sh -x nusers(这是个脚本文件)`  
   在脚本里,用`set -x`打开执行跟踪功能  
   `set +x`关闭  
   例如:

   ```vim
cat > trace1.sh
#! /bin/sh
set -x 
echo 1st echo 
set +x 
echo 2nd echo

执行：
chmod +x trace1.sh
./trace1.sh
```

   可以看到命令被打印出来

1.`echo`输出

> 1. `echo -e "a\tb\n"`激活转义字符
> 2. `echo -e "\e[0;31mThis is red text\e[0m"`
>    > `\e[1;31m`颜色码:重置=0,`31m xxm`等  
>    > `\e[0m`数字参数:0关闭所有属性,1 设置高亮…
> 3. echo -n “Enter your name” 省略换行符

2. 以`|`建立管道,`program1 | program2`可将`program1`的标准输出作为`program2`的标准输入
3. 特殊文件`/dev/null`

   > 位桶`bit bucket`,传送到此文件的数据都会被操作系统**丢掉**
4. `chmod 755 /tmp/hello.sh`赋予权限

   > 1. `/tmp/hello` 绝对路径直接运行
   > 2. `/bin/bash /tmp/hello.sh`  
   >    `bash /tmp/hello.sh`
5. `history`：历史命令记录

   > 1. `history -c`清空历史命令
   > 2. `history -w`将缓存中的命令写入历史命令保存文件  
   >      
   >      
   >    保存文件路径:`~/.bash_history`   
   >      
   >      
   >    `vim /root/.bash_history`查看历史命令
6. 历史命令的调用

   > `!n`执行第n条命令  
   > `!!`执行上一条命令
7. 命令与文件补全

   > `Tab`键自动补全
8. 命令别名

   > `alias`查看别名.
   >
   > 1. `alias vi='vim'`暂时更改别名(关机之前)
   > 2. `/root/.bashrc`,`alias`保存文件

- `shell`自带命令没有执行文件`whereis ls`  
  `whereis cd`
- `rc : run commands:从档案中取出一系列命令来执行的功能` 任何脚本类文件的后缀

9. bash常用快捷键

   > 1. `ctrl+c`强行中止当前命令
   > 2. `ctrl+l`==`clear`
   > 3. `ctrl+u`剪切光标之前的内容
   > 4. `ctrl+k`剪切光标之后的内容
   > 5. `ctrl+y`粘贴
10. 输入输出重定向

    > `linux`中输入输出重定向符号挺简单的,

- 正确重定向输出
  > 1. `ls -l > log11`覆盖的方式写入文件
  > 2. `ls -l >> log11`追加的方式写入文件
- 错误输出重定向
  > 1. `lst 2> log11`覆盖
  > 2. `lst 2>> log11`追加
- 同时保存错误输出和正确输出
  > - `命令 > 文件 2>&1`
  > 1. `list > log11 2>&1`覆盖
  > 2. `list >> log11 2>&1`追加
  > - `命令 &> 文件`
  > 1. `ls -l / &> log11`覆盖
  > 2. `ls -l / &>> log11` 追加
  > - `命令 >文件1 2>文件2`正确的覆盖到文件1,错误的覆盖到文件2(分开写入文件)
  > 1. `ls -l /sys >log1 2>log2`
  > 2. `ls -l /etc /dev >log1 2>>log2`
  > 3. 自己组合

11. 去除无效输出

- 背景：写脚本时不希望看到有输出
  > `ls &> /dev/null`:不存在`/dev/null`这个文件,等价于回收站

备注:

- `wc`:统计文本 行数,单词数,字节，字符`word line character ans byte count`
  > 1. `wc /tmp/sh/log1`缺省顺序:行数,单词数,字符数
  > 2. `-l line`行数  
  >    `-w word`单词数  
  >    `-c char`字符数  
  >    `wc -lwc log1 == wc log1`  
  >    `-m bytes`字节数

12. 多命令顺序执行(3种情况)
    > 1. `a;b`同时执行,错误命令报错,不影响后续命令
    > 2. `a && b`逻辑与,第一个正确才能执行下面一个
    > 3. `a||b`异或的关系，只能执行第一个对的,

- `grep`:`globe search regular expression and print out the line`(全局搜索正则表示式并打印)
  > 1. `grep "xxx" filename`  
  >      
  >     `grep xxx filename`
  > 2. `-n` 行数
  > 3. `--color=auto`关键字颜色
