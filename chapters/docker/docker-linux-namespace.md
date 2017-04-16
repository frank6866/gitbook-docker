# namespace
namespace是linux kernel提供的一种为一系列进程提供隔离的资源(比如pid, hostname, user id, network, ipc和filesystem等)的特性。  

和某个namespace关联的进程只能看见和这个namespace关联的资源。

namespace一个常见的用途是实现容器化技术，比如Docker。  



## 查看是否支持namespace
查看kernel是否支持namespace

```
# cat /boot/config-$(uname -a | awk '{print $3}') | grep "CONFIG_USER_NS=y"
```

如果输出"CONFIG_USER_NS=y"就表示支持namespace。  


## 分类
查看内核支持哪些namespace，找到clone 命令的online manual([http://man7.org/linux/man-pages/man2/clone.2.html](http://man7.org/linux/man-pages/man2/clone.2.html))，搜索CLONE_NEW字符，可以找到所有支持的namespace。如下:  

| namespace | clone_flag | 开始支持的kernel版本 | 隔离内容
| --------- | ---------- | ------------------ | -------
| Cgroup | CLONE_NEWCGROUP | 4.6 | Cgroup root directory
| IPC | CLONE_NEWIPC | 2.6.19 | System V IPC, POSIX message queues
| Network | CLONE_NEWNET | 2.6.24 | Network devices, stacks, ports, etc.
| Mount | CLONE_NEWNS | 2.4.19 | Mount points
| PID | CLONE_NEWPID | 2.6.24 | Process IDs  
| User | CLONE_NEWUSER | 2.6.23 |  User and group IDs
| UTS | CLONE_NEWUTS | 2.6.19 | Hostname and NIS domain name



# namespace API
namespace API包括[clone](http://man7.org/linux/man-pages/man2/clone.2.html), [setns](http://man7.org/linux/man-pages/man2/setns.2.html), [unshare](http://man7.org/linux/man-pages/man2/unshare.2.html)

## clone
clone()实际上是Linux系统调用fork()的一种更通用的实现方式，可以通过使用flags来控制使用多少功能。

**在Docker中就是使用的clone()系统调用来使用namespace的。**

### /proc/[pid]/ns目录
从3.8的kernel开始，用户就可以在/proc/[pid]/ns文件下看到指向不同namespace号的文件，如下查看telegraf进程的ns信息:  

```
# ps -ef | grep telegraf
root      1265  1115  0 18:45 pts/1    00:00:00 grep --color=auto telegraf
telegraf 19651     1  1 Mar21 ?        07:10:17 /usr/bin/telegraf -config /etc/telegraf/telegraf.conf -config-directory /etc/telegraf/telegraf.d
# ls -l /proc/19651/ns
total 0
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 cgroup -> cgroup:[4026531835]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 mnt -> mnt:[4026531840]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 net -> net:[4026531969]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 pid -> pid:[4026531836]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 user -> user:[4026531837]
lrwxrwxrwx 1 telegraf telegraf 0 Apr 16 18:45 uts -> uts:[4026531838]
```

比如net -> net:[4026531969]中4026531969就是namespace号。  

如果两个进程指向的namespace号相同，就说明它们在同一个namespace下面。  

在/proc/[pid]/ns文件里面设置link的作用是，如果该namespace下的进程结束了(进程结束了/proc/[pid]/目录就不存在了)，这个namespace还存在，后序的进程还可以加入进来。  

保留namespace的目的是为以后的进程加入做准备。  

也可以通过mount --bind的方式在进程结束的前提下，将namespace保留下来。

## setns
setns()系统调用的作用是将一个进程和一个namespace关联起来。  

在Docker中使用docker exec命令在已经运行的容器中执行一个新的命令，就需要用到该方法。

## unshare
unshare()系统调用使某进程脱离某个namespace。  



# demo
## UTS namespace
Unix Time-sharing System。







## PID namespace
PID namespace隔离非常使用，它对进程PID重新编号，即两个不同的namespace下的进程可以有相同的PID。  

![namespace-pid](resources/namespace-pid.png)

每个PID namespace都有自己的计数程序。内核为所有的PID namespace维护了一个树状结构，最顶层的是系统初始化时创建的(比如图中的init进程所在的namespace)，被称为root namespace。之后创建的新PID namespace被称为child namespace(比如图中pid为4的进程创建的child namespace)。

child namespace中的进程有两个PID，一个是全局的，比如pid为6的进程，6就是全局的pid；1是pid为6的进程在child namespace中的pid。

parent namespace中的进程可以看到chilid namespace中的进程，并可以通过信号等方式对子节点中的进程产生影响；但是child namespace中的进程却不能看到parent namespace中的进程。  

有如下规律：  

* 每个PID namespace中的第一个进程的PID为1，像Linux中的init或systemd进程一样拥有特权
* child namespace中的进程，不能看到parent namespace中的进程；更不能使用kill影响parent namespace中这些进程了
* 如果在新的PID namespace中重新挂载了proc文件系统到/proc目录，会发现/proc目录下只显示同属于一个PID namespace中的其他进程
* 在root namespace中可以看到所有的进程(包括child namespace中的进程，因为child namespace中的进程也在root namespace中有一个全局的PID)


### 测试代码
引用于[http://dockone.io/article/81](http://dockone.io/article/81)

vi get_pid_namespace.c

```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>
#define STACK_SIZE (1024 * 1024)
// sync primitive
int checkpoint[2];
static char child_stack[STACK_SIZE];
char* const child_args[] = {
"/bin/bash",
NULL
};


int child_main(void* arg) {
char c;
// init sync primitive
close(checkpoint[1]);
// wait...
read(checkpoint[0], &c, 1);
printf(" - [%5d] World !\n", getpid());
sethostname("In Namespace", 12);
execv(child_args[0], child_args);
printf("Ooops\n");
return 1;
}


int main() {
    // init sync primitive
    pipe(checkpoint);
    printf(" - [%5d] Hello ?\n", getpid());
    int child_pid = clone(child_main, child_stack+STACK_SIZE, CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWPID | SIGCHLD, NULL);
    close(checkpoint[1]);
    waitpid(child_pid, NULL, 0);
    return 0;
}

```

### 运行代码

编译链接

```
# gcc get_pid_namespace.c -o get_pid_namespace.bin
```


运行

```
# ./get_pid_namespace.bin
 - [24608] Hello ?
 - [    1] World !
[root@In Namespace tutorial]# echo $$
1
[root@In Namespace tutorial]# kill -9 24608
bash: kill: (24608) - No such process
```

可以看出打印当前进程编号返回的是1，并且在子进程中看不到父进程了。  


但是在子进程中执行ps命令时，看到的还是全局的进程号

```
[root@In Namespace tutorial]# ps
  PID TTY          TIME CMD
24419 pts/0    00:00:00 sudo
24420 pts/0    00:00:00 su
24421 pts/0    00:00:00 bash
24608 pts/0    00:00:00 get_pid_namespa
24609 pts/0    00:00:00 bash
24622 pts/0    00:00:00 ps
```










# TODO
一个进程可以在多个namespace中吗？可以有两个以上pid吗？
可以有多个层级的namespace吗？比如孙子








# 参考
* http://man7.org/linux/man-pages/man2/clone.2.html
* http://man7.org/linux/man-pages/man7/namespaces.7.html
* man setns













