---
title: 使用mutex和条件变量对比
date: '2020-03-06 12:02:00'
permalink: 2020/03/06/csdn/使用mutex和条件变量对比/
categories:
- 系统与底层
- Unix系统编程
tags:
- pthread
---

使用`mutex`和条件变量对比

#### 问题

> 学生线程写作业，老师线程检查作业。要求：只有学生线程写完作业了，老师线程才能检查作业。

1. 使用`mutex`

```c
#include "apue.h" 
#include <pthread.h>

int finished = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *do_homework(void *arg) {
	sleep(5);

	pthread_mutex_lock(&lock);
	finished = 1;
	pthread_mutex_unlock(&lock);
}

void *check_homework(void *arg) {
	sleep(1);
	pthread_mutex_lock(&lock);
	printf("老师:作业写完了吗\n");
	while (finished == 0) {
		printf("学生:没有写完\n");
		pthread_mutex_unlock(&lock);
		printf("老师:好的,你接着写\n");
		printf("-------\n");
		sleep(1);
		//上面的空档期让学生来写
		pthread_mutex_lock(&lock);
		printf("老师:作业写完了吗?\n");
	}
	printf("学生写完了\n");
	pthread_mutex_unlock(&lock);
	printf("老师开始检查\n");
}
 
int main(int argc,char *argv[]) {
	pthread_t tid1,tid2;
	pthread_create(&tid1,NULL,do_homework,NULL);
	pthread_create(&tid2,NULL,check_homework,NULL);

	pthread_join(tid1,NULL);
	pthread_join(tid2,NULL);
    exit(0);
}
```

- 缺点:老师线程轮循检查,(占用`cpu`导致浪费)

2. 使用`mutex`配合条件变量(条件+变量)

```c
#include "apue.h" 
#include <pthread.h>

int finished = 0;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *
do_homework(void *arg) {
	// 学生睡眠5s就是先放弃竞争
	sleep(5);
	pthread_mutex_lock(&lock);
	finished = 1;
	// 在通知　睡眠的线程唤醒前,自己先要把锁释放掉
	pthread_mutex_unlock(&lock);
	
	pthread_cond_signal(&cond);
	printf("发送条件信号\n");
}

void *check_homework(void *arg) {
	sleep(1);
	pthread_mutex_lock(&lock);
	// 轮询条件
	printf("老师: 作业写完了吗?\n");
	while (finished == 0) {
		printf("学生: 没有写完\n");
		printf("老师: 接着写\n");
		printf("------------\n");
		//第一次说接着写,然后就进入了　睡眠阶段
		pthread_cond_wait(&cond,&lock);
		printf("老师: 作业写完了吗?\n");
	} 
	printf("学生: 写完了\n");
	pthread_mutex_unlock(&lock);
	printf("老师开始检查\n");
}
 
int main(int argc,char *argv[]) {
	pthread_t tid1,tid2;
	pthread_create(&tid1,NULL,do_homework,NULL);
	pthread_create(&tid2,NULL,check_homework,NULL);
	pthread_join(tid1,NULL);
	pthread_join(tid2,NULL);
    exit(0);
}
```

- 相比使用互斥量的优点,不在进行轮询,第一次询问后开始睡眠,直到线程唤醒

#### 例题:

4 个线程，线程 1 循环打印 A, 线程 2 循环打印 B, 线程 3 循环打印 C, 线程 4 循环打印 D. 输出`ABCD ABCD ......`

(非标准答案,但我不是通过时间控制执行顺序)

```c
#include "apue.h" 
#include <pthread.h>

typedef void *(*Func)(void *);

int all = 0;
int c[5];
pthread_cond_t cond[5];
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *
thread1(void *arg) {
	while (1) {
		pthread_mutex_lock(&lock);
		while (c[1] == 0) { 
			pthread_cond_wait(&cond[1],&lock);
			printf("A");
			c[1] = 1;
			c[2] = 0;
		}
		pthread_mutex_unlock(&lock);
		pthread_cond_signal(&cond[2]);
	}
}

void *
thread2(void *arg) {
	while (1) {
		pthread_mutex_lock(&lock);
		while (c[2] == 0) { 
			pthread_cond_wait(&cond[2],&lock);
			printf("B");
			c[2] = 1;
			c[3] = 0;
		}
		pthread_mutex_unlock(&lock);
		pthread_cond_signal(&cond[3]);
	}
}

void *
thread3(void *arg) {
	while (1) {
		pthread_mutex_lock(&lock);
		while (c[3] == 0) { 
			pthread_cond_wait(&cond[3],&lock);
			printf("C");
			c[3] = 1;
			c[4] = 0;
		}
		pthread_mutex_unlock(&lock);
		pthread_cond_signal(&cond[4]);
	}
}

void *
thread4(void *arg) {
	while (1) {
		pthread_mutex_lock(&lock);
		while (c[4] == 0) { 
			pthread_cond_wait(&cond[4],&lock);
			printf("D");
			if (++all == 4)
				pthread_exit(NULL);
			c[4] = 1;
			c[1] = 0;
		}
		pthread_mutex_unlock(&lock);
		pthread_cond_signal(&cond[1]);
	}
}

int main(int argc,char *argv[]) {
	// 标准io无缓冲
	setbuf(stdout,NULL);
	pthread_t tid[5];
	Func func[5] = {NULL,thread1,thread2,thread3,thread4};
	for (int i=1; i<=4; i++)
		cond[i] = (pthread_cond_t)PTHREAD_COND_INITIALIZER;	
	for (int i=1; i<=4; i++)
		pthread_create(&tid[i],NULL,func[i],NULL);

	pthread_cond_signal(&cond[1]);

	for (int i=1; i<=4; i++)
		pthread_join(tid[i],NULL);
    exit(0);
}
// gcc test.c -o test -pthread -lapue
```
