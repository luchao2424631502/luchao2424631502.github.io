---
title: php留言板小demo
date: '2019-10-19 11:46:00'
permalink: 2019/10/19/csdn/php留言板小demo/
categories:
- php
tags:
- 留言板
---

### 测试环境

- 本地数据库名:`php10` user:`root`,passwd:,
- 表:`msg`,4个字段`id`,`content`,`user`, `intime`

### 一些简单sql语句

- 增: `INSERT INTO msg () VALUES ();`
- 删: `DELETE FROM msg WHERE id = 10;`  `DELETE FROM msg`
- 改: `UPDATE msg SET content='xx',user='xx'` `UPDATE msg SET content='xx',user=xx WHERE id<1 and id>9`
- 查 : `SELECT * FROM msg`  (`*`代表字段)

---

### MYSQLI 函数的使用

`test1.php`

```php
<?php 
// 提交留言且显示

$host='127.0.0.1';
$dbuser='root';
$passwd='';
$database='php10';

$db = new mysqli($host,$dbuser,$passwd,$database);

//判断连接是否成功
if ($db->connect_errno)
	die("数据库连接失败");

// 与数据库服务器 传输时的编码格式 
$db->query("SET NAMES UTF8");
$sql = 'select * from msg order by id desc;';
//执行查询语句 拿到查询结果
$myquery_result = $db->query($sql);

// var_dump($myquery_result);
 
if (!$myquery_result)
	die("查询失败");

$rows = []; //二维数组取出所有数据
while ( $row = $myquery_result->fetch_array(MYSQLI_ASSOC) ) {
	$rows[] = $row;
}

?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8"/>
	<title>留言本</title>
	<style>
	.warp {
		width:600px;	
		margin:0px auto; 
	}
	.add { overflow: hidden;}
	.add .content {
		width:598px;
		padding:0;
		margin:0;
	}
	.add .user {float:left;}
	.add .btn {float:right;}

	.msg {margin:20px 0px; background:#ccc; padding:5px;}
	.msg .info {overflow:hidden;}
	.msg .user {float:left; color:blue;}
	.msg .time {float:right; color:black;}
	.msg .content { width:100%; padding:5px; }
	</style>
</head>
<body>
	<div class='warp'>
		<div class='add' >
		<!--  表单提交给 formsave.php, 通过 formsave.php 将表单数据写入数据库 -->
		<form action="formsave.php" method="post">
			<textarea name='content' class='content' cols='50' rows='5'> </textarea>
			<input name='user' class='user' type='text'/>
			<input class='btn' type='submit' value='发表留言' />
		</form>
		</div>
		<?php
			// 通过遍历显示留言内容 
			foreach( $rows as $row) {
		?>
			<!-- 留言板显示 -->
			<div class='msg'>
				<div class='info'>
					<span class='user'> <?php echo $row['user']; ?> </span>
					<span class='time'> <?php echo date("Y-m-d H:i:s",$row['intime']); ?> </span>
				</div>
				<div class='content'>
					<span> <?php echo $row['content']; ?> </span>
				</div>
			</div>
		<?php
		} 
		?>
	</div>
</body>
</html>
```

`formsave.php`

```php
<?php 
// POST传参
$content = $_POST['content'];
$user = $_POST['user'];

function post( $content ) {
	if ( $content == '')
		return false;
	$forbid_use = ['xx','xx','xx','xx'];

	foreach($forbid_use as $i) 
		if ($content == $i)
			return false;
	return true;
}
if ( !post($content) )
	die ('留言不正确<br>');

if ( !post($user) )
	die ('用户不正确<br>');

$host = '127.0.0.1';
$dbuser = 'root';
$passwd = '';
$database = 'php10';

$db = new mysqli($host,$dbuser,$passwd,$database);
$db->query("SET NAMES UTF8");

if ($db->connect_errno) 
	die('连接数据库失败');

$time = time();

$sql = "insert into msg (content,user,intime) values ('{$content}','{$user}',$time);";
//将表单提交的数据写入数据库.
$flag = $db->query( $sql );

if (!$flag)
	die("插入数据失败");
// 转跳至 同目录下的 test1.php 
header("location: test1.php");
?>
```
