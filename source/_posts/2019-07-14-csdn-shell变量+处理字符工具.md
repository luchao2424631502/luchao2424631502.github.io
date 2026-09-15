---
title: shell变量+处理字符工具
date: '2019-07-14 16:44:00'
permalink: 2019/07/14/csdn/shell变量+处理字符工具/
categories:
- Linux学习
tags:
- awk cut sed
---

- `\`放在命令最后表示连接下一行

#### 变量规则

1. Bash中变量默认的是字符串型,如要进行数值运算,需要修改变量的类型,指定为数值型
2. 变量赋值等号两边不能有空格

   #### 变量分类
3. 用户自定义变量
4. 环境变量,保存操作系统环境相关数据
5. 预定义变量,(相当于脚本传入变量)

- `set` 打印系统所有变量
- `unset name` 变量删除 `unset time`
- `PATH`系统查找命令的路径  
  临时修改环境变量`PATH="$PATH:/tmp"`,`PATH`是由冒号分割的

  ##### `PS1`定义系统提示符的变量

  #### 位置参数变量分类(预定义变量的一种)

1. `$n` `n=0`代表当前命令本身,其他的参数按顺序排,超过`9` 用`${10}`
2. `$0`：输出命令本身.
3. `$@`:所有参数看成独立,`$*`：所有参数看成整体.
   ```bash
#!/bin/bash
for i in "$*"
    do
        echo $i
    done
for i in "$@"
    do
        echo $i
    done
```

   #### 预定义变量
4. `$?`:命令的返回值.最后一次执行命令是否成功,`0`代表**成功**,其余表错误
5. `$\$\$$`:当前进程的**进程号**
6. `$!`:后台运行的最后一个进程号

#### read

1. `-s`:隐藏输入,
2. `-t`:允许输入的时间
3. `-p`:输入打印的字符
4. `-n`:输入的**字符数**  
   `read [选项] [变量名]`  
   `read -p "your name " -s -t 30`  
   `read -n 2 -s -p "Pleasr enter your name" -t 30 name`

#### 数值运算(shell中变量默认为字符串类型)

```bash
#!/bin/bash
a=11
b=22
c=$a+$b
echo $c
```

1. `declare`: 声明变量类型
   > 1. `-p`:显示变量类型  
   >    `declare -p PATH`
   > 2. `-i`:声明为`integer`
   > 3. `-x`:声明为环境变量

- 声明为`int`在运算
  ```bash
#!/bin/bash
a=1
b=2
declare -i c=$1+$2
echo $c
----
#!/bin/bash
a=1
b=1
c=$a+$b
echo $c
daclare -i c=$a+$b
echo $c
```
- $((运算式)) 或者 $[运算式]

#### 变量测试与变量替换

1. abc这个变量名字可以任意替换,将abc这个变量理解为`x=${y-0}`
   ```bash
x=${y-abc}
echo $x
```
2. 1 `y为空`,则`x=abc`
3. 2 `y=1`,则`x=1`
4. 用的时候查表

#### 一些配置文件

1. `/root/.bash_logout`注销时的配置文件
2. `/root/.bash_history`历史命令保存的文件(注销之后才**写入**)
3. shell登录信息
4. 本地终端的登录信息`/etc/issue`
5. 远程登录`/etc/issue.net`,配置文件不生效的原因是`ssh`的配置文件`/etc/ssh/sshd_config`决定,修改`Banner /etc/issue.net`这行,会显示`/etc/issue.net`
6. 登录后的信息(远程或本地登录都会生效) `/etc/motd`

#### 通配符用来匹配文件名

- 通配符是**完全匹配**,
- `ls find cp`这些命令不支持正则,
- `ls -l f*`

#### 正则表达式匹配字符串

- 在文件中匹配符合条件的字符串
- **包括匹配**

#### 字符截取命令

1. `cut`:对比`grep`提取行,`cut`和`awk`是用来提取列中文字
   > 1. `-d`:默认分割符:列之间的换行符`tab`,修改分隔符
   > 2. `-f`:提取的列数  
   >    `cat /etc/passwd | grep /bin/bash | cut -d ":" -f 1,3`
2. `printf` 格式化输出,  
   `printf "%s %s\n" $(cat student)` `$(cat student)`引用系统命令
   > 系统有`printf`没有`print`命令,`awk`中2个都有,  
   > `print`比`printf`会**自动加入换行符**
3. `awk`
   > `awk '[pattern1]{act1}[pattern2]{act2}' 文件名`  
   > `awk '模式1{动作1} 模式2(条件2){动作2}' 文件名`
   >
   > 1. 可以从行中提取列  
   >    `awk '{printf $2"\t"$4"\n""} student'`
   > 2. `df -h | awk '{printf $1 "\t" $2 "\t" $4 "\n"}'`  
   >    `df -h | awk '{print $1 "\t" $3 "\t" $4}'`  
   >    效果相同
   > 3. `cut`、`awk` 、`grep`混用  
   >    `df -h | grep "vda1" | awk '{print $5}' | cut -d "%" -f 1`,  
   >    用`cut`将`7%`中`%`作为分隔符,数字作为第1列提取出来

> 4. `BEGIN`后的`{}`列出来的操作,在读入输入之前执行,`END`后的`{}`列出来的操作在读入输入完成后执行

> 5. `awk`默认识别的分隔符是**制表符,或者空格**  
>    `FS`内置变量,来指定**分隔符**,  
>    `awk '{FS=":"}{print $2 "\t" $4}' /etc/passwd`

> 6. 在指定`FS=":"`时,先读入第一行再来指定分隔符,使用`BEGIN`在读入之前修改**分隔符**  
>    `awk 'BEGIN{FS=":"}{print $2 "\t" $5}' /etc/passwd`

> 7. 通过条件对数据进行筛选, 例：  
>    `cat student | grep -v "Name" | awk '$6>90{print $2}BEGIN{print "Who is best"}END{print "The end"}'`

#### sed(轻量级流编辑器)

- `sed [option] 'command' file`  
  `sed 选项 '命令' 文件名`
- 选项:
  > 1. `-n`,`sed`一般会将所有的数据打印,`-n`只打印经过处理的行
  > 2. `-i`:同时修改源文件,不打印在屏幕上
  > 3. `-e`:多条`sed`命令编辑
- 命令:
  > - `sed -n '2,3p' student`:`2,3p`表示第2行到第3行.
  > 1. `sed -n '1p' student` :`p`打印第一行  
  >    `sed '1p' student`,对比缺少`-n`的效果  
  >    `df -h | sed -n '2p'`
  > 2. `sed ‘2d’ studen
  > - 字符串替换
  > 1. `sed 'ns\原内容\新内容\g' student`:  
  >    `n`表示第n行,否则全部原内容被替换  
  >    `s`:替换指定字符  
  >    `g`:获得内存缓冲区的内容,代替当前模板(文件)内的文本  
  >    `sed '3s\84\90\g' student`
  > - `-e` 多sed命令,**中间是`;`**  
  >   `sed -e 's\Gao\Anthony\g ; s\Sc\Sb\g' student`   
  >   `sed -e 's\Gao\ \g ; s\Sc\ \g' student`
