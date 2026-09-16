---
title: shell_流程控制语句
date: '2019-07-19 17:21:00'
permalink: 2019/07/19/csdn/shell_流程控制语句/
categories:
- 工具与效率
- Shell与命令行
tags:
- shell
---

#### if

- `if`开头,`fi`结尾
- 单分支`if`语句

```fortran
if [ 判断 ];then
    program
fi
```
```fortran
if [ 判断 ]
    then
        program
fi
```

统计根分区使用率写提醒脚本

```bash
#!/bin/bash
rate=$(df -h | grep "/dev/vda1" | awk 'print $5' | cut -d "%" -f 1)

if [ $rate -lt 80]
    then 
        echo "/dev/vda1 is lower than 80%"
fi
```

---

```bash
#!/bin/bash
rate=$(df -h | grep /dev/vda1 | awk '{print $5}' | awk 'BEGIN{FS="%"}{print $1}')
if [ $rate -lt 80 ];then
    echo "/dev/vda1 's capacity lower than 80"
fi
```

注意:

1. 用awk也行
   ```reasonml
rate=$(df -h | grep /dev/vda1 | awk '{print $5}' | awk 'BEGIN{FS="%"}{print $1}')
```
2. 比较中,`$rate`前面加`\$`引用变量

- 多分支
  ```fortran
if [ 判断 ]
    then 
        program
    else 
        program
fi
```
  打包备份`/etc`目录:
  ```gradle
#!/bin/bash
date=$(date +%y%m%d)
size=$(du -sh /etc)
if [ -d /tmp/dbback ]
    then
        echo "Date is:$date">/tmp/dbback/db.txt
        cd /tmp/dbback
        tar -zcf etc_$date.tar.gz /etc db.txt &> /dev/null
        rm -rf /tmp/dbback/db.txt
    else 
        mkdir /tmp/dbback
        echo "Date is:$date" > /tmp/dbback/db.txt
        cd /tmp/dbback
        tar -zcf etc_$date.tar.gz /etc db.txt &> /dev/null
        rm -rf /tmp/dbback/db.txt
fi
```
  解释:

1. 判断是否存在`/tmp/dbback`这个目录
2. 有就备份,没有就创建
3. 进入这个目录作为相对路径
4. 打包后 删除原来的文件  
   一个

- `yum -y install nmap`安装远程扫描命令
- `yum -y install httpd`安装`apache`
- `nmap -sT ip地址` 看80端口开了没  
  `nmap -sT ip | grep 'http$' | awk '{print $2}'`,截取端口状态  
  写一个脚本
  ```bash
#!/bin/bash
port=$(nmap -sT ip | grep 'http$' | awk '{print $2}')
if [ "$port" == "open" ];then
    echo "$(date) httpd is open!" >> /tmp/autostart.acc.log
    else 
        #没有启动则重启
        /etc/rc.d/init.d/httpd start &> /dev/null
        echo "$(date) restart httpd ">> /tmp/autostart.err.log
fi
```

  #### if elseif else

  ```fortran
if [ 判断 ];then
    program
elif 
    then
        program
else 
    program
fi
```

---

```fortran
if [ 判断 ]
    then
        program
elif
    then 
        program
else 
    program
fi
```

##### 判断文件类型脚本

```bash
#!/bin/bash
read -p "Please input a filename:" file

if [ -z "$file" ] 
    then 
        echo "Error,please input a filename"
        exit 1
elif [ ! -e "$file" ] 
    then 
        echo "Your input is not a file"
        exit 2
elif [ -f "$file" ] 
    then 
        echo "$file is a regular file"
elif [ -d "$file" ]
    then 
        echo "$file is a directory"
else 
    echo "$file is an other file"
fi
```

#### case 语句

1. 和`if`一样,结束语都要导致
2. `program`语句要以`;;`结尾
   ```bash
case $val in
    1)
        echo "1";;
    2)
        echo "2";;
    3) 
        echo "3";;
    4)
        echo "other";;
esac
```
   例如:
   ```bash
#!/bin/bash
read -t 30 -p "Please input you choose" choose
case $choose in
    1)
        echo "1";;
    2) 
        echo "2";;
    3)
        echo "3";;
    *)
        echo "other";;
esac
```

#### for

1. 在文件中操作
   ```fortran
for 变量 in value1 v2 v3...
    do
        program
    done
```

---

```bash
#!/bin/bash
for i in 1 2 3 4 5
    do 
        echo $i
    done
```

- 例:统计当前文件夹下`.sh`文件数量
  ```bash
#!/bin/bash
cd /tmp/sh/
cnt=0
for i in $(ls *.sh)
    do 
        cnt=$(( $cnt + 1 )) 
        echo "$i"
    done
echo "文件数量=$cnt"
```

2. c语法,在`(( ))`数值运算符内
   ```fortran
for ((i=1; i<=100; i++))
    do
        program
    done
```
   例:
   ```bash
#!/bin/bash
cnt=0
for ((i=1; i<=100; i++))
    do
        cnt=$(( $cnt + $i )) 
    done
echo $cnt
```

#### while / until

1. ```bash
#!/bin/bash
i=100
while [ $i -ge 10 ]
    do
        echo "$i"
        i=$(( $i - 1 ))
    done
```
2. `until`:直到 条件成立 就 终止
   ```bash
#!/bin/bash
sum=0; i=1
until [ $i -gt 100 ]
    do
        $sum=$(( $sum + $i ))
        $i=$(($i+1))
    done
echo $sum
```
