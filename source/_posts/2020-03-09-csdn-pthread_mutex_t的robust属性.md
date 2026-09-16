---
title: pthread_mutex_t的robust属性
date: '2020-03-09 14:56:00'
permalink: 2020/03/09/csdn/pthread_mutex_t的robust属性/
categories:
- 系统与底层
- Unix系统编程
tags:
- linux
---

### `mutex`的`robust`属性

- **健壮属性**与**多个进程间共享互斥量有关**

---

#### 使用背景

多进程共享数据块同步时,持有互斥量的进程终止时,那么其他进程会一直阻塞下去(死锁),通过`robust`解决进程间一个`mutex`导致死锁的问题

```c
// 获取\设置robust属性
pthread_mutexattr_getrobust(const pthread_mutexattr_t *restrict attr,int *restrict ans);

pthread_mutexattr_setrobust(pthread_mutexattr_t *attr,int robust);
```

#### `robust`属性作用解释

1. 健壮属性默认值是`pthread_mutex_stalled`,**持有互斥量的进程终止时不采取任何动作**,其他进程一直被阻塞
2. `pthread_mutex_robust`:

   > #### 一致性:
   >
   > **健壮的互斥锁的所有者在持有互斥锁的同时终止,则该互斥锁将变得不一致(`inconsistent`)**,通过返回值`EOWNERDEAD`通知获取互斥锁的下一个线程,
   >
   > ### 但是要 互斥锁 状态要标记为一致(`consistent`),互斥锁才能使用(互斥锁状态恢复)
   >
   > 所以检测`pthread_mutex_lock`的返回值 (在进程共享内存同步情况下) 有3种:
   >
   > ```
   >  1. 不需要恢复的成功
   > 2. 失败
   > 3. (新增)需要恢复的成功(恢复锁的一致性)
   > ```

#### 多进程通信例子(一个`mutex`):

[高级IO+进程通信暂时没学,借鉴dalao博客](https://blog.csdn.net/q1007729991/article/details/62424302)

1. `init`程序的作用是申请共享内存，并在共享内存中分配互斥量等。
2. `destroy`用来回收共享内存中的互斥量，并销毁共享内存。
3. `buyticket` 是从共享内存的数据中抢票的。

#### `init.c`

```c
#include "init.h"
 
#define PERR(msg) \
	do { perror(msg); exit(-1); } while(0)
#define PPERR(err,msg) \
	do { err=errno; perror(msg); exit(-1); } while(0)

struct ticket {
	int remain;
	pthread_mutex_t lock;
};

// 打印mutex的　进程共享属性
void 
printshared(pthread_mutexattr_t *attr) {
	int err,shared;
	err = pthread_mutexattr_getpshared(attr,&shared);
	if (err != 0) PPERR(err,"pthread_mutexattr_getshared");
	
	if (shared == PTHREAD_PROCESS_PRIVATE)
		puts("shared = PTHREAD_PROCESS_PRIVATE");
	else if (shared == PTHREAD_PROCESS_SHARED)
		puts("shared = PTHREAD_PROCESS_SHARED");
	else 
		puts("shared = ???");
}

// 打印mutex的　健壮属性
void 
printrobust(pthread_mutexattr_t *attr) {
	int err,robust;
	err = pthread_mutexattr_getrobust(attr,&robust);
	if (err != 0) PPERR(err,"pthread_mutexattr_getrobust");
	if (robust == PTHREAD_MUTEX_STALLED)
		puts("robust = PTHREAD_MUTEX_STALLED");
	else if (robust == PTHREAD_MUTEX_ROBUST)
		puts("robust = PTHREAD_MUTEX_ROBUST");
	else 
		puts("robust = ???");
}

int main(int argc,char *argv[]) {
	int err,shared,robust = 0,flag = 1;
	//if (argc >= 2) 
	robust = 1;
	key_t key = 0x8888;

	// 创建共享内存
	int id = shmget(key,getpagesize(),IPC_CREAT | IPC_EXCL | 0666);
	if (id < 0) PERR("shmget");

	// 挂载共享内存
	struct ticket *t = (struct ticket *)shmat(id,NULL,0);

	if (t == (void *)-1) PERR("shmat");

	t->remain = 10;

	pthread_mutexattr_t mutexattr;
	err = pthread_mutexattr_init(&mutexattr);
	if (err != 0) PPERR(err,"pthread_mutexattr_init");

	printshared(&mutexattr);
	printrobust(&mutexattr);

	shared = PTHREAD_PROCESS_SHARED;
	err = pthread_mutexattr_setpshared(&mutexattr,shared);
	if (err != 0) PPERR(err,"pthread_mutexattr_setpshared");
	
	if (robust) {
		err = pthread_mutexattr_setrobust(&mutexattr,PTHREAD_MUTEX_ROBUST);
		if (err != 0) PPERR(err,"pthread_mutexattr_setrobust");
	}

	puts("modify attribute ----------------------");
	printshared(&mutexattr);
	printrobust(&mutexattr);

	// 用attr初始化mutex
	pthread_mutex_init(&t->lock,&mutexattr);
	// 反初始化　attr
	err = pthread_mutexattr_destroy(&mutexattr);
	if (err != 0) PPERR(err,"pthread_mutexattr_destroy");
	
	err = shmdt((void *)t);
	if (err != 0) PERR("shmdt");
	return 0;
}
```

#### `destroy.c`

```c
#include "init.h"

#define PERR(msg) do { perror(msg); exit(-1); } while(0)
#define PPERR(err,msg) do { err=errno; perror(msg); exit(-1); } while(0)

struct ticket {
	int remain;
	pthread_mutex_t lock;
};
 
int main(int argc,char *argv[]) {
	int err;
	key_t key = 0x8888;
	int id = shmget(key,0,0);
	if (id < 0) PERR("shmget");

	struct ticket *t = (struct ticket*)shmat(id,NULL,0);

	if (t == (void *)-1) PERR("shmat");

	err = pthread_mutex_destroy(&t->lock);
//	if (err != 0) PPERR(err,"pthread_mutex_destroy");

	err = shmdt((void *)t);
	if (err != 0) PERR("shmdt");

	err = shmctl(id,IPC_RMID,NULL);
	if (err != 0) PERR("shmctl");
	return 0;
}
```

#### `buyticket.c`

```c
#include "init.h"

#define PERR(msg) do { perror(msg); exit(-1); } while(0) 
#define PPERR(err,msg) do { err=errno; perror(msg); exit(-1); } while(0)

struct ticket {
	int remain;
	pthread_mutex_t lock;
};

int main(int argc,char *argv[]) {
	if (argc < 2) {
		printf("Usage: %s <name>\n",argv[0]);
		exit(-1);
	} 

	char *name = argv[1];
	int err,shared,flag = 1;
	key_t key = 0x8888;
	int id = shmget(key,0,0);
	if (id < 0) PERR("shmget");

	struct ticket *t = (struct ticket*)shmat(id,NULL,0);

	if (t == (void *)-1) PERR("shmat");

	while (flag) {
		err = pthread_mutex_lock(&t->lock);
		// 需要恢复的成功
		if (err == EOWNERDEAD) {
			puts("EOWNERDEAD");
			// 拥有互斥锁的进程终止后,互斥量就变成inconsistent(不一致性)
			// 恢复锁的一致性,此时进程还是获得锁的状态
			err = pthread_mutex_consistent(&t->lock);
			if (err != 0) {
				printf("consistent error\n");
				exit(-1);
			}
		}
		// 失败
		else if (err == ENOTRECOVERABLE) {
			puts("ENOTRECOVERABLE");
		} 
		// 不需要恢复的成功
		int remain = t->remain;
		if (remain > 0) {
			sleep(1);
			--remain;
			t->remain = remain;
			printf("%s buy a ticket\n",name);
			sleep(3);
		} else 
			flag = 0;
		pthread_mutex_unlock(&t->lock);
		sleep(2);
	}
	err = shmdt((void *)t);
	if (err != 0) PERR("shmdt");
	return 0;
}
```

#### `init.h`

```c
#ifndef INIT_H
#define INIT_H

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#include <pthread.h>

#endif
```

- 每个`.c`编译参数 `gcc a.c -o a -lpthread`

---

#### 总结

设置`robust`属性后,通过判断`pthread_mutex_lock`的返回值来**恢复`pthread_mutex_t`的一致性(再次获得锁)**
