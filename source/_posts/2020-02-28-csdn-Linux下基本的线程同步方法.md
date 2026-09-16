---
title: Linux下基本的线程同步方法
date: '2020-02-28 16:30:00'
permalink: 2020/02/28/csdn/Linux下基本的线程同步方法/
categories:
- 系统与底层
- Unix系统编程
---

### 线程同步

#### 问题引入:

> ２个线程同时修改一个变量`x = 1`时,如果不进行**同步**会怎么样?
>
> 假设进行增加操作,增量操作通常分解为３步
>
> > 1. 从内存将变量读入寄存器(cpu)
> > 2. 在寄存器中对变量做增量操作
> > 3. 写回内存
>
> 那么在线程A对`x`进行增量操作时,如果**不加锁**,那么最终结果取决与线程B开始增量操作时获取的值,
>
> - 比如:
>
>   线程A中`cpu`对寄存器中变量做完增量操作还没有写回内存,此时线程B获取到的值还是`1`,最终2线程执行完后值是`2`,

#### 互斥量

1. 函数

> ```c
// 初始化互斥量
pthread_mutex_init(pthread_mutex_t *restrict mutex,
				const pthread_mutexattr_t *restrict attr);
// 若动态分配的互斥量,在内存回收前,先摧毁mutex
pthread_mutex_destroy(pthread_mutex_t *mutex);

// 给互斥量加锁
pthread_mutex_lock(pthread_mutex_t *mutex);

// 解锁
pthread_mutex_unlock(pthread_mutex_t *mutex);

// 尝试加锁,此时mutex未锁住,则锁住(不阻塞)返回0,否则返回EBUSY
pthread_mutex_trylock(pthread_mutex_t *mutex);
```
>
> - 先了解os就比较好理解

- 实例:多线程环境下访问动态分配的对象中,嵌入引用计数,避免对象内存空间不会被释放,

```c
#include "apue.h" 
#include <pthread.h>

struct foo {
	int f_count;
	pthread_mutex_t f_lock;
	int f_id;
	int f_use;
};
 
struct foo *
foo_alloc(int id)
{

	struct foo *fp;

	if ((fp = malloc(sizeof(struct foo))) != NULL) {
		fp->f_count = 1;
		fp->f_id = id;
		if (pthread_mutex_init(&fp->f_lock,NULL) != 0) {
			free(fp);
			return NULL;
		}
	}
	return fp;
}

void 
foo_hold(struct foo *fp)
{
	pthread_mutex_lock(&fp->f_lock);
	fp->f_count++;
	pthread_mutex_unlock(&fp->f_lock);
}

void 
foo_rele(struct foo *fp)
{
	pthread_mutex_lock(&fp->f_lock);
	if (--fp->f_count == 0) {
		pthread_mutex_unlock(&fp->f_lock);
		// 如果互斥量是动态分配的,在回收内存前要destroy(互斥量)
		pthread_mutex_destroy(&fp->f_lock);
		printf("end\n");
		free(fp);
	}

	pthread_mutex_unlock(&fp->f_lock);
}

void *
func(void *arg)
{
   	// 使用对象的话
    return ((void *)0);
}

int main(int argc,char *argv[]) {
	pthread_t tid[maxn]; 
	struct foo *p = foo_alloc(99);
	// 3个线程的线程池
	for (int i=0; i<maxn; i++) 
		pthread_create(&tid[i],NULL,func,(void *)p);

	// ３个元素的数组,元素是void *
	for (int i=0; i<maxn; i++) {
		pthread_join(tid[i],NULL);
	}
	
	free(p);
    exit(0);
}
```
> 类似`c++`类的构造和析构,且要在临界区中更新计数,但此段程序仍有问题: **还剩2个线程时,如果线程A进入`foo_rele`此时引用计数- 1 等于 0 且线程B因为`mutex`被锁住而被阻塞,那么内存被释放是不对的**

#### 死锁

1. 线程对同一`mutex`加锁２次,

```c
#include "apue.h" 
#include <pthread.h>

pthread_mutex_t mutex;
 
// 同一mutex加锁２此死锁
void *
func(void *arg)
{
	// 尝试２次对mutex进行加锁
	pthread_mutex_lock(&mutex);
	
	// 尝试加锁,但是mutex已经被加锁,于是阻塞,但是又是自己加的锁,自己被阻塞不能解开造成死锁
	pthread_mutex_lock(&mutex);
}

int main(int argc,char *argv[]) {
	pthread_t tid;
	void *ret;

	pthread_create(&tid,NULL,func,NULL);
	
	// 主线程等待线程返回,不然可能主线程return了子线程还没开始执行
	pthread_join(tid,&ret);
    exit(0);
}
```

2. 线程A给`mutex_A`加锁后试图给`mutex_B`加锁,但线程B已经给`mutex_B`加锁且想占有`mutex_A`,**２线程都想请求对方的资源,导致死锁**

```c
#include "apue.h" 
#include <pthread.h>

pthread_mutex_t mutex1,mutex2;

void *
func1(void *arg)
{
	pthread_mutex_lock(&mutex1);

	sleep(2);

	pthread_mutex_lock(&mutex2);
}

// sleep的目的是想让另一个线程开始执行

void *
func2(void *arg)
{
	pthread_mutex_lock(&mutex2);
	
	sleep(1.5);
	
	pthread_mutex_lock(&mutex1);
}
 
int main(int argc,char *argv[]) {
	pthread_t tid1,tid2;
	
	//创建线程
	pthread_create(&tid1,NULL,func1,NULL);
	pthread_create(&tid2,NULL,func2,NULL);


	pthread_join(tid1,NULL);
	pthread_join(tid2,NULL);
    exit(0);
}
```

##### 防止死锁规律

- **多线程按照相同的顺序对互斥量进行加锁就不会死锁(可能其他资源导致死锁,不讨论**
- **如果一个线程加锁的顺序和另一个线程加锁的顺序相反那么一定会导致死锁**

> tips:**结构体中的互斥量能够保护整个结构的成员**

##### 实例

```c
#include "apue.h" 
#include <pthread.h>

#define NHASH 29
#define HASH(id) (((unsigned long)id)%NHASH)

struct foo *fh[NHASH];

// 只适合静态分配的mutex进行初始化or init (记住mutex使用之前必须初始化)
pthread_mutex_t hashlock = PTHREAD_MUTEX_INITIALIZER;

struct foo {
	int f_count;
	int f_id;
	pthread_mutex_t f_lock;
	struct foo *f_next;
};

//给struct foo分配内存空间,
struct foo *
foo_alloc(int id)
{
	struct foo *fp;
	int index;
	if ((fp = malloc(sizeof(struct foo))) != NULL) {
		fp->f_count = 1;
		fp->f_id = id;
		// 使用互斥量前一定要初始化
		if (pthread_mutex_init(&fp->f_lock,NULL) != 0) {
			free(fp);
			return NULL;	
		}
		index = HASH(id);
		pthread_mutex_lock(&hashlock);
		fp->f_next = fh[index];
		fh[index] = fp;
		pthread_mutex_lock(&fp->f_lock);
		pthread_mutex_unlock(&hashlock);

		/* 省略初始化,初始化完成之前,阻塞其他线程访问此结构*/

		pthread_mutex_unlock(&fp->f_lock);
	}
	return fp;
}

void 
foo_hold(struct foo *fp)
{
	pthread_mutex_lock(&fp->f_lock);
	fp->f_count++;
	pthread_mutex_unlock(&fp->f_lock);
}

struct foo *
foo_find(int id)
{
	struct foo *fp;
	
	pthread_mutex_lock(&hashlock);
	// 从hash链表头开始查,
	for (fp = fh[HASH(id)]; fp != NULL; fp = fp->f_next) {
		if (fp->f_id == id) {
			// 加锁了又加一层锁,影响性能,
			foo_hold(fp);
			break;
		}
	}
	pthread_mutex_unlock(&hashlock);
	// 增加引用计数,并返回指向该结构的指针
	return fp;
}

void 
foo_rele(struct foo *fp)
{
	struct foo *tfp;
	int index;

	// 首先别的线程在我访问时不能访问,则锁住该结构
	pthread_mutex_lock(&fp->f_lock);
	if (fp->f_count == 1) {
		// 解锁,因为想从散列表中删除
		pthread_mutex_unlock(&fp->f_lock);
		// 锁住hashlock,防止被find找到,但是之前已经找到的线程会从此时会增加引用计数,
		// 对散列表加锁,然后对结构加锁
		pthread_mutex_lock(&hashlock);
		pthread_mutex_lock(&fp->f_lock);

		// f_lock unlock后 其他线程找到了并对其进行hold,此时我们返回就行了
		if (fp->f_count != 1) {
			fp->f_count--;
			pthread_mutex_unlock(&fp->f_lock);
			pthread_mutex_unlock(&hashlock);
			return ;
		}

		index = HASH(fp->f_id);
		// tfp是链表头
		tfp = fh[index];
		if (tfp == fp) 
			fh[index] = fp->f_next;
		else {
			// 找到fp在链条中的上一个,然后移除fp
			while (tfp->f_next != fp)
				tfp = tfp->f_next;
			tfp->f_next = fp->f_next;
		}
		pthread_mutex_unlock(&hashlock);
		pthread_mutex_unlock(&fp->f_lock);
		pthread_mutex_destroy(&fp->f_lock);
		free(fp);
	} else {
		fp->f_count--;
		pthread_mutex_unlock(&fp->f_lock);
	}
}

int main(int argc,char *argv[]) {
    exit(0);
}
```

---

改进

```c
#include <stdlib.h>
#include <pthread.h>

#define NHASH 29
#define HASH(id) (((unsigned long)id)%NHASH)
 
struct foo *fh[NHASH];
pthread_mutex_t hashlock = PTHREAD_MUTEX_INITIALIZER;
// initializer

struct foo {
	int f_count;
	pthread_mutex_t f_lock;
	int f_id;
	struct foo *f_next;
};

struct foo *
foo_alloc(int id)
{
	struct foo *fp;
	int index;

	if ((fp = malloc(sizeof(struct foo))) != NULL) {
		fp->f_count = 1;
		fp->f_id = id;
		// 第二个参数mutex_t attr,返回互斥量的错误码
		if (pthread_mutex_init(&fp->f_lock,NULL) != 0) {
			free(fp);
			// 分配失败
			return NULL;
		}
		// 根据id得到链表索引
		index = HASH(id);
		pthread_mutex_lock(&hashlock);
		fp->f_next = fh[index];
		fh[index] = fp;
		pthread_mutex_lock(&fp->f_lock);
		// 和前面一个,在全局锁解锁前,先把自己加锁
		pthread_mutex_unlock(&hashlock);
		pthread_mutex_unlock(&fp->f_lock);
	}
	return fp;
}

void 
foo_hold(struct foo *fp)
{
	pthread_mutex_lock(&fp->f_lock);
	fp->f_count++;
	pthread_mutex_unlock(&fp->f_lock);
}

struct foo *
foo_find(int id)
{
	struct foo *fp;
	// 操作链表,多个线程可能同时找个一个然后同时操作,所以锁住hashlock
	pthread_mutex_lock(&hashlock);
	for (fp = fh[HASH(id)]; fp != NULL; fp = fp->f_next) {
		if (fp->f_id == id) {
			fp->f_count++;
			break;
		}
	}
	pthread_mutex_unlock(&hashlock);
	return fp;
}

void 
foo_rele(struct foo *fp)
{
	struct foo *tfp;
	int index;
	pthread_mutex_lock(&hashlock);
	//此时可能有hold线程存在,但是hold中的f_lock能锁住结构体
	if (--fp->f_count == 0) {
		index = HASH(fp->f_id);
		tfp = fh[index];
		if (tfp == fp)
			fh[index] = fp->f_next;
		else {
			while (tfp->f_next != fp)
				tfp = tfp->f_next;
			tfp->f_next = fp->f_next;
		}
		pthread_mutex_unlock(&hashlock);
		pthread_mutex_destroy(&fp->f_lock);
		// 多线程及时被抢占也无所谓,已经从列表中移除了
		free(fp);
	} else
		// 不符合资格就不释放
		pthread_mutex_unlock(&hashlock);
}

int main(int argc,char *argv[]) {
    exit(0);
}
```

#### `pthread_mutex_timedlock`

> `int pthread_mutex_timedlock(pthread_mutex_t *restrict mutex,const struct timespec *restrict tsptr);`
>
> 尝试获得一个已经加锁的互斥量,在允许的绝对时间前阻塞,直到该互斥量的锁释放,否则超过时间返回`ETIMEDOUT`

```c
#include "apue.h" 
#include <pthread.h>
 
int 
main(int argc,char *argv[]) {
	int err;
	struct timespec tout;
	struct tm *tmp;
	char buf[64];
	pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

	pthread_mutex_lock(&lock);
	printf("mutex is locked\n");
	clock_gettime(CLOCK_REALTIME,&tout);
	tmp = localtime(&tout.tv_sec);	
	strftime(buf,sizeof(buf),"%r",tmp);
	printf("current time is %s\n",buf);
	tout.tv_sec += 10;

	sleep(5);
	pthread_mutex_unlock(&lock);
	// 2次对自己加锁,就会造成死锁
	// 在绝对时间前,只要锁释放了就锁住,否则error返回
	err = pthread_mutex_timedlock(&lock,&tout);
	clock_gettime(CLOCK_REALTIME,&tout);
	tmp = localtime(&tout.tv_sec);
	strftime(buf,sizeof(buf),"%r",tmp);
	printf("the time is now %s\n",buf);

	if (err == 0)
		printf("mutex locked again!\n");
	else 
		printf("can't lock mvtex again:%s\n",strerror(err));
    exit(0);
}
```

#### 读写锁

1. 原理

> 共享互斥锁(`shared-exclusive-lock`),有３种状态:
>
> > 1. 读模式加锁
> > 2. 写模式加锁
> > 3. 不加锁
> >
> > - 读模式加锁就是共享状态,多个线程可以同时占有锁(os实现可能对线程个数有限制,所以要检查`pthread_rwlock_rdlock()`的返回值)
> > - 写模式加锁就是互斥,只能有一个线程占用锁,
>
> 1. 读写锁是**写模式加锁状态时,在这个锁解锁前,无论是以读还是写的方式试图对这个锁加锁的线程都将阻塞**
> 2. 读写锁是**读模式加锁状态时,以读方式对读写锁加锁的线程可以获得访问权,但是以写的方式对读写锁加锁的线程会被阻塞(直到所有线程释放读锁为止)** —-> 如果此时又有线程以读方式加锁,如果该线程不被阻塞,**岂不是以写方式对读写锁加锁的线程一直处于饥饿状态,所以　读写锁会阻塞随后的读模式锁请求,避免读模式锁长期占用,而写模式锁请求等不到满足**,

2. 适用场景

> 对数据结构**读的次数远大于写的次数**

3. 使用

> 初始化与`pthread_mutex_t`相同,静态分配的读写锁初始化可使用`PTHREAD_RWLOCK_INITIALIZER`,也可使用`pthread_rwlock_init()`初始化,动态分配的读写锁在回收内存前要释放资源`pthread_rwlock_destroy()`,
>
> ---
>
> ```c
>pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);
>pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);
>pthread_rwlock_unlock(pthread_rwlock_t *rwlock);
```

```c
#include "apue.h" 
#include <pthread.h>

struct job {
	struct job *j_next;
	struct job *j_prev;
	pthread_t j_id; // 线程id
};

struct queue {
	struct job *q_head;
	struct job *q_tail;
	pthread_rwlock_t q_lock;
};

int 
queue_init(struct queue *que)
{
	int err;
	que->q_head = NULL;
	que->q_tail = NULL;
	// 初始化任务队列的读写锁
	err = pthread_rwlock_init(&que->q_lock,NULL);
	if (err != 0)
		return err;
	return 0;
}

// job插入到队列头
void
job_insert(struct queue *que,struct job *jp)
{
	// 互斥锁住
	pthread_rwlock_wrlock(&que->q_lock);
	jp->j_next = que->q_head;
	jp->j_prev = NULL;
	if (que->q_head != NULL)
		que->q_head->j_prev = jp;
	else 
		// 队列中只有１个job了
		que->q_tail = jp;
	que->q_head = jp;

	pthread_rwlock_unlock(&que->q_lock);
}

// job插入到列队尾部
void 
job_append(struct queue *que,struct job *jp)
{
	pthread_rwlock_wrlock(&que->q_lock);
	jp->j_next = NULL;
	jp->j_prev = que->q_tail;
	if (que->q_tail != NULL)
		que->q_tail->j_next = jp;
	else
		//队列中只有１个job了
		que->q_head = jp;
	que->q_tail = jp;
	pthread_rwlock_unlock(&que->q_lock);
}

// 从job队列中　移出job
void
job_remove(struct queue *que,struct job *jp)
{
	pthread_rwlock_wrlock(&que->q_lock);

	if (jp == que->q_head) {	
		que->q_head = jp->j_next;
		// 队列只剩一个就是jp
		if (que->q_tail == jp)
			que->q_tail == NULL;
		else
			jp->j_next->j_prev = jp->j_prev;
		// jp是最后一个,且队列长度>1
	} else if (jp == que->q_tail) {
		que->q_tail = jp->j_prev;
		jp->j_prev->j_next = jp->j_next;
	} else {
		jp->j_prev->j_next = jp->j_next;
		jp->j_next->j_prev = jp->j_prev;
	}
	pthread_rwlock_unlock(&que->q_lock);
}

// 从队列中找到某个job
struct job *
job_find(struct queue *que,pthread_t id)
{
	struct job *jp;

	// 系统对读锁被占有的线程个数有限制,所以检查返回值
	if (pthread_rwlock_rdlock(&que->q_lock) != 0)
		return NULL;

	for (jp = que->q_head; jp != NULL; jp = jp->j_next)
		if (pthread_equal(id,jp->j_id))
			break;
	pthread_rwlock_unlock(&que->q_lock);
	return jp;
}

int 
main(int argc,char *argv[]) {
 
    exit(0);
}
```

#### 条件变量

> 线程通过共享全局变量进行同步,条件变量分为条件状态和变量(用来通信)`pthread_cond_t`
>
> - 初始化和其他的一样
>
> 条件由互斥量来保护,,线程在改变条件状态前先锁住互斥量,`pthread_cond_wait(pthread_cond_t *cond,pthread_mutex_t *mutex)`,然后此函数把调用线程放入等待条件的线程列表(进程挂起),**对互斥量解锁,等`pthread_cond_wait`返回后,互斥量再次被锁住**

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdlib.h>
#include <pthread.h>

void
maketimeout(struct timespec *tsp,long minutes)
{
	struct timeval now;
	gettimeofday(&now,NULL);
	tsp->tv_sec = now.tv_sec;
	tsp->tv_nsec = now.tv_usec * 1000;
	tsp->tv_sec += minutes * 60;
}

struct msg {
	struct msg *m_next;
};

struct msg *workq;

pthread_cond_t qready = PTHREAD_COND_INITIALIZER;

pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER;


// 消费者(消费消息) 
void  
process_msg(void)
{
	struct msg *mp;
	for (;;) {
		pthread_mutex_lock(&qlock);
		// 如果工作队列为空,则线程进入等待(循环等待)
		while (workq == NULL) 
			// 线程放入等待条件的线程列表上
			pthread_cond_wait(&qready,&qlock);
		// 处于等待的线程结束等待后,立即进入临界区
		mp = workq;
		workq = mp->m_next;
		printf("proc msg \n");
		pthread_mutex_unlock(&qlock);
	}
}

// 生产者(生产消息)
void 
enqueue_msg(struct msg *mp)
{
	pthread_mutex_lock(&qlock);
	mp->m_next = workq;
	workq = mp;
	printf("create \n");
	pthread_mutex_unlock(&qlock);
	// 给处于条件变量等待队列中的线程发信号,
	pthread_cond_signal(&qready);

}

void *
func1(void *arg)
{
	process_msg();
	return (void *)0;
}

void *
func2(void *mp)
{
	enqueue_msg(mp);
	return (void *)0;
}

const int maxn = 100;

int main(int argc,char *argv[]) {
	pthread_t tid[maxn];
	struct msg* p[maxn];
	for (int i=0; i<maxn; i++)
		p[i] = (struct msg *)malloc(sizeof(struct msg));
		
	pthread_t tid1;
	pthread_create(&tid1,NULL,func1,NULL);
	//我先创造maxn个生产者
	for (int i=0; i<maxn; i++)
		pthread_create(&tid[i],NULL,func2,(void *)p[i]);
	
	for (int i=0; i<maxn; i++)
		pthread_join(tid[i],NULL);
	for (int i=0; i<maxn; i++)
		free(p[i]);
	pthread_join(tid1,NULL);
    exit(0);
}
```

#### 自旋锁(类似互斥量)

1. 非抢占式内核中,由于中断处理程序不能抢占已经有锁的线程,所以中断不会导致死锁
2. 单核/单cpu环境下使用自旋锁没有用,因为线程A获得锁以后,线程B一直占用CPU使得锁不能释放,知道线程B的时间片用完,
3. 获得自旋锁之前一直处于忙等待状态(占用CPU),所以自旋锁被持有的时间短,且线程不希望进行睡眠or唤醒的线程调度
4. 尝试获取互斥量可能会先自旋一会(避免线程调度,看具体实现)

```c
#include "apue.h" 
#include <pthread.h>
 
pthread_spinlock_t lock;

void *
func1(void *arg)
{
	printf("func1 before\n");
	pthread_spin_lock(&lock);
	printf("func1 中间\n");
	sleep(1);

	printf("func1 end\n");
	pthread_spin_unlock(&lock);	
	return (void *)0;
}

void *
func2(void *arg)
{
	printf("func2 before\n");
	pthread_spin_lock(&lock);
	printf("func2 sleep\n");
	sleep(10);
	printf("func2 end\n");
	pthread_spin_unlock(&lock);
	return (void *)0;
}

int main(int argc,char *argv[]) {
	pthread_spin_init(&lock,PTHREAD_PROCESS_SHARED);
	pthread_t tid1,tid2;

	pthread_create(&tid1,NULL,func1,NULL);
	pthread_create(&tid2,NULL,func2,NULL);


	pthread_join(tid1,NULL);
	pthread_join(tid2,NULL);
	pthread_spin_destroy(&lock);
    exit(0);
}
```

#### 屏障

- 多线程并行工作的同步机制,允许每个线程等待,直到所有的合作线程都达到某一点,然后从该点继续执行,(意思是等待一些线程在某点之前必须都执行完毕

> `pthread_join()`就是一种简单的屏障,等待指定的线程执行完毕

- 使用屏障允许任意数量的线程等待,直到所有线程处理完毕

---

> 1. 初始化相比其他几个同步少了**宏定义**,且初始化要**声明任意线程的数量(记得主线程**
>
> ```c
>// 注意第三个参数
>pthread_barrier_init(pthread_barrier_t *barrier,
                   const pthread_barrierattr_t *attr,
                   unsigned int count);
>pthread_barrier_destroy(pthread_barrier_t *barrier);
```
>
> 2. `pthread_barrier_wait()`表明此线程完成工作,等待其他线程赶上来
>
> - 调用此函数的线程在屏蔽计数为满足时,线程进入休眠状态,最后一个调用的线程会唤醒所有此类线程(**注意返回值**)

```c
// gcc a.c -o a -lpthread -lbsd
#include "apue.h" 
#include <pthread.h>
#include <limits.h>
#include <sys/time.h>

#define NTHR 8 
#define NUMNUM 8000000L
#define TNUM (NUMNUM/NTHR)

long nums[NUMNUM];
long snums[NUMNUM];

pthread_barrier_t b;

#ifdef SOLARIS
#define heapsort qsort
#else
extern int heapsort(void *,size_t,size_t,int (*)(const void *,const void *));
#endif 

int 
complong(const void *arg1,const void *arg2)
{
	long l1 = *(long *)arg1;
	long l2 = *(long *)arg2;

	if (l1 == l2)
		return 0;
	else if (l1 < l2)
		return -1;
	else
		return 1;
}

void *
thr_fn(void *arg)
{
	long index = (long)arg;
	heapsort(&nums[index],TNUM,sizeof(long),complong);
	// 线程完成工作,等待其他所有线程赶上来,增加屏障计数
	pthread_barrier_wait(&b);
	return (void *)0;
}

void 
merge()
{
	long index[NTHR];
	long i,minindex,sindex,num;

	// 得到每个线程处理部分的下标
	for (i = 0; i < NTHR; i++)
		index[i] = i * TNUM;
	// 扫描所有数字一遍,每一个数字从8个部分中选取,然后增加其中一部分的下标,８个部分都已经是排好序
	for (sindex = 0; sindex < NUMNUM; sindex++) {
		num = LONG_MAX;
		for (i = 0; i <	NTHR; i++) {
			//
			if ((index[i] < (i+1)*TNUM) && (nums[index[i]] < num)) {
				num = nums[index[i]];
				minindex = i;
			}
		}
		snums[sindex] = nums[index[minindex]];
		index[minindex]++;
	}
}

int main(int argc,char *argv[]) {
	unsigned long i;
	struct timeval start,end;
	long long startusec,endusec;
	double elapsed;
	int err;
	pthread_t tid;
	srandom(1);
	for (i = 0; i < NUMNUM; i++)
		nums[i] = random();
	gettimeofday(&start,NULL);
	// 初始化屏障量
	pthread_barrier_init(&b,NULL,NTHR+1);
	for (i = 0; i < NTHR; i++) {
		err = pthread_create(&tid,NULL,thr_fn,(void *)(i * TNUM));
		if (err != 0)
			err_exit(err,"can't create thread");
	}
	// 自己做完了,等到所有屏障前的线程,满足屏障计数后,所有线程都唤醒,
	pthread_barrier_wait(&b);
	merge();
	gettimeofday(&end,NULL);

	startusec = start.tv_sec * 1000000 + start.tv_usec;
	endusec = end.tv_sec * 1000000 + end.tv_usec;
	elapsed = (double)(endusec - startusec) / 1000000.0;
	printf("sort took %.4f seconds\n",elapsed);
	//for (i = 0; i < NUMNUM; i++)
	//	printf("%ld\n",snums[i]);
	//
    exit(0);
}
```

- 单线程和8线程,性能提高4倍多,
