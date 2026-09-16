---
title: DNS本地服务器配置+samba配置
date: '2019-07-26 21:21:00'
permalink: 2019/07/26/csdn/DNS本地服务器配置+samba配置/
categories:
- 网络与服务
- 计算机网络
tags:
- DNS学习
---

- 一种`DNS`配置文件`/etc/resolv.conf`

  ## `CIFS (common internet file system )`又称网络文件共享系统
- 是一种**应用层网络传输协议**

1. `cifs`也称**服务器消息块**`Server Message Block`,

- `cifs`一般面向`windows`端

  ### `samba`
- 配置文件`/etc/samba/smb.conf`

---

1. `yum -y install samba`安装samba  
   `useradd alice -s /sbin/nologin`  
   `useradd jack -s /sbin/nologin`  
   `smbpasswd -a alice` 添加samba用户  
   `smbpasswd -a jack`

---

> `-a` 将linux系统用户添加为samba用户  
> `-d` 冻结用户  
> `-e` 恢复用户  
> `-x` 删除用户

---

启动`samba`的2个服务`nmb`,且修改配置文件  
和`smb`  
`centos 6`  
`service nmb start;chkconfig nmb on`  
`service smb start;chkconfig smb on`

- 配置文件修改
  ```jboss-cli
vim /etc/samba/smb.conf
[data]
    path = /data
    writable = yes #都有写的权限
    # valid user = alice jack
```

### `windows`客户端

1. `windows + R`
2. `\\ip`(`ip`是`samba`服务器地址) 输入`samba`账号
3. **映射网络服务器**相当于将**共享文件夹(磁盘) 挂载到 windows的目录下**

   ### `Linux`客户端

- `yum -y install samba-client cifs-utils` `samba 客户端`

1. 查看存储端共享  
   `smbclient -L ip --user=alcie`
2. 手动挂载  
   `mount -t cifs -o user=alice,pass=1 //192.168.44.132/data /mnt/cifs`
3. `vim /etc/fstab`  
   添加  
   `//192.168.44.132/data /mnt/cifs cifs defaults,user=alice,pass=1 0 0`  
   `mount -a`

   ## DNS

- 以前是`Netbios 网络输入输出系统`名:`baidu`.由`wins`服务提供解析
- `FQND (fully qualified domain name) 完全合格的域名` ：`www.baidu.com`.由2中方法解析

1. `hosts`文件  
   作用:实现名字解析.主要为本地主机名.集群节点提供快速解析
2. `DNS`服务器解析(将主机名解析成ip)

---

1. 命名空间: 互联网主机命名机制
2. `DNS`数据库`Datebase`: 分布式数据库
3. 根域

---

### DNS服务器基本配置(`cache only`惟缓存DNS服务器:可称为`dns转发`)

- 此`dns`是:非域内权威服务器,也是向上访问寻求解析  
  环境:2个虚拟机ip  
  `dns服务器端`:`192.168.44.132`  
  `dns客户端`:`192.168.44.133`
- `tianyun.me`:自己随便起的局域网内的域名(且`http`搭载到`192.168.44.133`这个虚拟机上,让`192.168.44.132`服务器上的`DNS`服务器帮我们解析域名)

1. 修改客户端`dns服务器ip地址`.  
   先让没装`dns服务器的虚拟机来解析`.  
   `vim /etc/resolv.conf`  
   `nameserver 192.168.44.132`

- `dns`通信时使用`udp`协议

2. `yum -y install tcpdump`  
   抓客户端的包看一下  
   服务器端抓(`53`端口的包):  
   `tcpdump -i eth0 -nn port 53`  
   同时客户端  
   `ping www.baidu.com`  
   抓到包,但是由于还没配`dns服务器环境`所以无法解析

具体一点抓包  
`tcpdump -i eth0 -nn host 192.168.44.133`

3. 使用`bind`搭建`dns`域名解析服务器  
   `yum -y install bind bind-chroot`

- `bind`服务器配置文件`/etc/namd.conf`
- 域的数据:`/var/lib/named`

> 1. 将配置文件`/etc/named.conf`中
>
> **端口53(`dns端口`)访问改成任何人可以访问`listen-on port 53 { any; };`**
>
> **或者删除**  
> 2. 开启`dns`服务  
> `centos 6`: `service named start`  
> 3. 开防火墙  
> `service iptables restart`  
> 4. 服务端再次`ping www.baidu,com`成功

---

## `DNS`正区向解析设置

- 正向解析:`域名`解析为`ip`
- 反向解析: `ip`解析为`域名`

1. 修改主配置文件`vim /etc/named.conf/`.添加域

```nginx
#directory "/var/named"; 表示数据存放的目录
zone "tianyun.me" {
    type master;
    file "tianyun.me.zone"#数据存放文件名
};
```

2. 创建数据库文件`vim /var/named/名字相同`
   ```dns
#www.tianyun.com. = www
tianyun.me. IN  SOA dns.tianyun.me  root.tianyun.me.    ( 2019072600 1H 15M 1W 1D )
tianyun.me  IN  NS  dns
dns IN  A   192.168.44.132 #dns服务器ip地址(本机)
www IN  A   192.168.44.133  #客户端(需要域名解析)的ip地址,将www.tianyun.me 解析为这个Ip
#ftp    IN  A   192.168.44.1 将ftp.tianyun.me 解析为192.168.44.1,
# @代表域名 .  直接对域名进行解析
@   IN  A   192.168.44.133 # 即ping tianyun.me 也能通
```

---

第一行()内容意义:

1. `20190700`(自定义的**版本号**).辅助`dns`服务器通过这个判断是否与主`dns`服务器同步
2. `1H`.每隔`1h`.辅助`dns`服务器开始同步
3. `15M`.若连接不上主`dns`服务器.`15分钟`代表尝试连接的时间
4. `1W`.若尝试连接时间超过`1周`就过期
5. `1D`缓存时间`TTL(Time to live)`,**域名解析在DNS服务器中保留的时间**

- 都可以写成以`3600`(秒)为单位,也可以带单位

```less
SOA : 起始授权记录 (必须)
NS : DNS服务器记录  (必须)
A : 主机记录
CNAME : 别名记录
@：域名
```

---

3. `service named restart`
4. 客户端`ping tianyum.me`或者`ping www.tianyun.me` 都行

#### 客户端查询解析

- 权威名称服务器:存储提供`某个区域的实际数据`
- 非权威名称服务器:仅缓存`DNS`服务器.不存储实际数据

1. `nslookup baidu.com`
2. `host www.baidu.com`
   ```excel
-t //指定查询域名信息类型
host -t A luchaocloud.com
host -t SOA tianyun.me
```
3. `dig ip` //使用配置文件的`DNS`解析  
   `dig @8.8.8.8 baidu.com` //使用指定`DNS`服务器解析

   #### `DNS`解析流程
4. 查询自己缓存(`windows`下缓存包含`hosts记录`,`linux`下不包括),没有就发送给设置的`DNS`服务器
5. 如果本地`DNS`服务器具有权威答案,则发送到客户端
6. 否则(不具有权威性),如果本地`DNS`服务器查看缓存是否有请求的信息.若有(非权威答案)发送到客户端
7. 如果缓存没有.该`DNS`将搜索权威`DNS`服务器已查找信息  
   a. 从跟区域开始,按照`DNS`层次结构向下搜索.找到后在自己的缓存中保留  
   b. 转发给其他`DNS`服务器
