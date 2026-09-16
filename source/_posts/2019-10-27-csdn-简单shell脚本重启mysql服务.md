---
title: 简单shell脚本重启mysql服务
date: '2019-10-27 13:41:00'
permalink: 2019/10/27/csdn/简单shell脚本重启mysql服务/
categories:
- 工具与效率
- Shell与命令行
---

- shell脚本定时检测mariadb状态,实现崩溃后重启服务

  - 检测mysql状态多种方法（监听端口之类）, (`centos7 systemctl`中服务名称为`mariadb`也能用`pgrep -x mysqld`)
  - 检测`pgrep` 命令返回值 然后重启服务```gradle
# !/bin/bash
time=$(date)
pgrep -x mysqld &> /dev/null

if [ $? -ne 0 ]; then
    echo "break_time:$time " > /root/1.in
    systemctl restart mariadb
fi
```
- 添加定时任务

  - 脚本当前路径`/root/mysql_listen.sh`
  - `crontab -e`添加定时任务 , 5分钟检测一次: `*/5 * * * * /root/mysql_listen.sh`
- 当前目录下: 修改`.sh`权限使其能够执行 `chmod 755 mysql_listen.sh`
