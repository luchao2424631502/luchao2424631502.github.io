---
title: Debian下cpupower设置记录
date: '2020-03-17 10:36:00'
permalink: 2020/03/17/csdn/Debian下cpupower设置记录/
categories:
- 系统与底层
- Linux基础
---

- `Linux`内核调频知识 [链接](https://wiki.archlinux.org/index.php/CPU_frequency_scaling_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#cpupower)

---

> 查看当前cpu调度器
>
> `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`  
> 查看cpu支持调度
>
> `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors`
>
> 查看当前cpu频率
>
> `cat /proc/cpuinfo | grep MHz`
>
> (高版本内核可能不适用查看cpu频率)

`Debian`下(我用的`deepin`):

1. `sudo apt install linux-cpupower` (`Debian`下不会有默认配置文件在`/etc/default/cpupower`)
2. 创建`cpupower`配置文件`/etc/default/cpupower`(可以参考其他发行版本下`cpupower`的配置文件

   ```bash
# 自己设置调度
CPUPOWER_START_OPTS="frequency-set -g performance"
CPUPOWER_STOP_OPTS="frequency-set -g powersave"
```
3. 创建`systemd`服务,`vim /usr/lib/systemd/system/cpupower.service`

   ```bash
[Unit]
Description=Configure CPU power related settings
After=syslog.target

[Service]
Type=oneshot
RemainAfterExit=yes
EnvironmentFile=/etc/default/cpupower
ExecStart=/usr/bin/cpupower $CPUPOWER_START_OPTS
ExecStop=/usr/bin/cpupower $CPUPOWER_STOP_OPTS

[Install]
WantedBy=multi-user.target
```
   - 注意`EnvironmentFile`,其他发行版本换成相应配置文件的路径
4. 开启服务

   `systemctl daemon-reload`

   `systemctl enable cpupower.service` 开机自动启动

   `systemctl start cpupower.service`当前启动

---

- 也不一定要创建服务,写个脚本定时执行`cpupower -c all frequency-set -g 调度类型`就行

---

- `cpupower`之类命令记录

  ```bash
cpupower -c all frequency-info #查看所有cpu info
cpupower -c all frequency-set -g xxx #修改所有cpu调度类型
cat /proc/cpuinfo | grep MHz #查看当前cpu频率
```

---

- 参考

  [blog1](https://wsgzao.github.io/post/cpupower/)

  [systemd](https://huataihuang.gitbooks.io/cloud-atlas/os/linux/redhat/system_administration/systemd/cpupower.html)

  [Arch wiki](https://wiki.archlinux.org/index.php/CPU_frequency_scaling_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#cpupower)

  [blog2](https://kknews.cc/digital/bpn4qgn.html)
