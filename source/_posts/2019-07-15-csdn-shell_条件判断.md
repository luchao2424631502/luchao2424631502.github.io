---
title: shell_条件判断
date: '2019-07-15 17:16:00'
permalink: 2019/07/15/csdn/shell_条件判断/
categories:
- 工具与效率
- Shell与命令行
tags:
- shell
---

- `sort`

1. `-n`:按数字排序,默认是按照字符串排序.
2. `-r`:`reverse`反排序
3. `-k a,b`:排序的范围,第`a`到`b`列
4. `-t ":"`:修改分隔符，例如:  
   `cp /etc/passwd /tmp/sh`  
   `sort -n -k 3,4 -t ":" student | awk 'BEGIN{FS=":"}{print $3 "\t" $4}'`  
   `sort -n -r -k 3,4 -t ":" student | awk 'BEGIN{FS=":"}{print $3 "\t" $4}'`

回顾： `$?`:代表上一条命令是否执行正确   
 `echo $?`  
或者用逻辑表达  
`[ -f /root ] && echo yes || echo no`

#### 条件判断

- 判断的2组格式
  > 1. `test -e /root/install.log`
  > 2. `[ -e /root/install.log ]`
- 文件类型判断(常用选项)

| -e | **文件**存在为真 |
| --- | --- |
| -f | 文件存在且为**普通文件**则真 |
| -d | 文件存在且为**目录**则真 |

> 1. `test -e /root/install.log`
> 2. `[ -e /root/install.log ]`

- 文件权限(任意用户有权限都算)

| -r | read |
| --- | --- |
| -w | write |
| -x | execute |

> 1. `test -w /root/install.log`
> 2. `[ -r /root/install.log ]`

#### 硬链接(`hard link`)与软链接(`soft link`)区别

![ZIBfeK.jpg](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9zMi5heDF4LmNvbS8yMDE5LzA3LzE0L1pJQmZlSy5qcGc)

- `hard link`
  > - 硬链接是**仅文件名字不同但是inode号相同**的文件
  > 2. 硬链接和`原file`有相同的`inode`和`date block`
  > 3. 不能对目录建立
  > 4. 不能再交叉文件系统建立硬链接,因为`inode`在不同文件系统不一样
  > 5. 删除一个硬链接不影响相同`inode`文件
- `soft link`
  > - 拥有自己的`inode`和`block`,存放的是指向文件的路径,类比于windows的快捷方式
  > 1. 可以对目录创建
  > 2. **不存在**的**文件和目录**也可以创建
  > 3. 可以在交叉的文件系统创建
- 文件时间比较

| file1 -nt file2 | new time 修改时间是否新 |
| --- | --- |
| file1 -ot file2 | `old time` |
| file1 -ef file2 | `equal file`,判断文件`inode`是否相同,即是否为同一文件 |

`test /etc/passwd -nt /tmp/temp && echo 1 || echo 2`

`[ /etc/passwd -nt /tmp/temp ] ; echo $?`

- 整数之间的比较

| `eq` `equal` | 相等 |
| --- | --- |
| `ne` `not equal` | 不相等 |
| `gt` `greater than` | 大于 |
| `ge` `greater equal` | 大于等于 |
| `it` `lower than` | 小于 |
| `ie` `lower equal` | 小于等于 |

`test 1 -eq 2 && echo yes || echo no`

`[ 1 -eq 2] ; echo $?`

- 字符串之间的比较

| `-z` | **为空则真** |
| --- | --- |
| `-n` | **非空则真** |
| `!=` | 相等 |
| `==` | 不相等 |

`test -z "string" && echo yes || echo no`

`[ -z "string" ] ; echo $?`

- 逻辑判断

| `-a` `and` | `[ -z "" -a -z "addd"] ; echo $?` |
| --- | --- |
| `-o` `or` | `[ -z "" -o -z "dd" ] ; echo $?` |
| `!` | `[ ! -z "ad" ] ; echo $?` |
