---
title: 服务器内存小导致mysql服务停止解决方案+wordpress搭建
date: '2019-08-04 00:03:00'
permalink: 2019/08/04/csdn/服务器内存小导致mysql服务停止解决方案+wordpress搭建/
categories:
- Linux学习
tags:
- mariadb performance_schema
---

## wordpress搭建

- 域名现在要实名
- 买了国外服务器后(可以使用默认的dns服务器,一般都能解析),然后修改`dns 解析设置`,设置为服务器的ip
- ~~好像修改dns服务器要等几个小时才能成功~~
- `dig yourdomain`或者`nslookup youdomain`查看是否域名解析到`ip`是否成功

#### lnmp环境搭建

1. 安装 `nginx mariadb php-fpm`…
2. `nginx`配置文件修改(写入内容是~~抄~~的): `vim /etc/nginx/conf.d/web.conf`

- `server_name`:自己的域名
- `root`:表示`nginx`站点根目录
  ```nginx
#======================== WEB options ============================
server {
        listen       80;
        server_name  yourdomain;
        root         /var/wordpress;
	index        index.php index.html;
	charset	     utf-8;
#======================== Pseudo static ==========================
        location / {
	if (-f $request_filename/index.html){ rewrite (.*) $1/index.html break; }
	if (-f $request_filename/index.php){ rewrite (.*) $1/index.php; }
	if (!-f $request_filename){ rewrite (.*) /index.php; }
	}
#======================== PHP options ============================
	location ~ \.php {
		root    /var/wordpress;
		fastcgi_pass    127.0.0.1:9000;
		fastcgi_index   index.php;
		fastcgi_param   SCRIPT_FILENAME  $document_root$fastcgi_script_name;
		include         fastcgi_params;
	}
#======================== Error page =============================
        error_page 400 403 404 /40x.html;
            location = /40x.html {
        }
        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```

3. 配置`php`服务  
   `vim /etc/php-fpm.d/www.conf`

- `nginx`用户使用`php-fpm`服务,权限设置
  ```crmsh
user = nginx
group = nginx
```

4. 创建一个数据库给`wordpress`使用

   > 1. `mysql`
   > 2. `create database xxx`
   > 3. 创建该数据库的账户密码  
   >    `grant all privileges on wpdb.* to '账户1'@'localhost' identified by '密码1';`  
   >    账户名:`账户1`,密码:`密码1`
   > 4. 看看已有的数据库  
   >    `show databases;`
5. 开启所有服务

   > 1. `systemctl enable mariadb`  
   >    `systemctl start mariadb`
   > 2. `systemctl enable php-fpm`  
   >    `systemctl start php-fpm`
   > 3. `systemctl enable nginx`  
   >    `systemctl start nginx`
6. 下载`wordpress`到`/var/wordpress`(站点根目录)

- `wget`下载解压打包看别的`blog`
- 修改`/var/wordpress`的所属组和用户
- `chmod 755 -R /var/wordpress`
- `chown nginx:nginx -R wordpress`
- ~~`wordpress`的权限给`nginx`避免一些权限报错~~

7. 域名访问来安装`wordpress`

### 关于~~低配便宜辣鸡~~服务器,`mariadb(mysql)`服务自动终止原因

- `vim /var/log/mariadb/mariadb.log`查看报错

```sql
140521 08:26:40 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
140521 08:26:41 mysqld_safe mysqld from pid file /var/run/mysqld/mysqld.pid ended

mysqld: Out of memory (Needed 128917504 bytes)之类的报错

Fatal error: cannot allocate memory for the buffer pool
无法在内存中分配内存.服务器内存小.
```

原因:

```pgsql
Well, the issue here is Performance Schema, and not making it obvious.
When starting up, it allocates all the RAM it needs.
By default, it will use around 400MB of RAM,
which isn’t noticible with a database server with 64GB of RAM,
but it is quite significant for a small virtual machine.
```

- `默认是性能模式且不明显,sql启动时会分配它需要的RAM,默认会使用400MB,大服务器上这点不算什么.但是在小虚拟机上很重要`
- ~~好像我的`Plugins`(插件)服务也因为内存的原因不能用~~

  #### 修改配置文件`vim /etc/my.cnf`,在`[mysqld]`项下.

  添加:`performance_schema = off`

### 当运行环境正常和域名解析正确时,如果还是访问不了,说明服务器的防火墙关闭了`80端口`

1. 关闭防火墙
2. 开启`80端口`
   ```routeros
firewall-cmd --zone=public --add-port=80/tcp --permanent
systemctl restart firewalld
```
