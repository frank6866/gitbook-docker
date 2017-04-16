# cgroup

参考地址:  

* [https://access.redhat.com/documentation/zh-CN/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/ch01.html](https://access.redhat.com/documentation/zh-CN/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/ch01.html)
* [http://www.infoq.com/cn/articles/docker-kernel-knowledge-cgroups-resource-isolation](http://www.infoq.com/cn/articles/docker-kernel-knowledge-cgroups-resource-isolation)


## 简介
cgroup(全称是control group)，是Linux Kernel(2.6.24中加入)提供的一种限制、记录和隔离进程所使用资源的机制。  

cgroup可以限制的资源包括：  

* CPU时间
* 系统内存
* 网络带宽
* 存储

或者这些资源的组合，我们还可以在系统运行过程中动态地设置cgroup。  

cgroup并不是从头开始研发的一种机制，而是将进程管理从cpuset中剥离出来。  

cgroup本身提供的功能主要有两个:  

* 将进程分组化管理
* 提供接口的基础结构


# 概念
cgroup的一些概念:  

* task(任务): 表示一个系统进程
* control group: 表示按照某种标准划分的一组进程
* subsystem: 表示资源控制器
* hierarchy: 层级，指control group可以组成hierarchy的形式。

CGroup中的资源控制是以Control Group为单位实现的。  

subsystem必须attach到一个hierarchy上才能起作用

## control group
控制组，里面包含了进程。


## hierarchy(层级)
cgroup是分层管理的，类似进程；子cgroup会继承上级cgroup的一些属性。层级好像一棵树，每个结点都是一个control group。

hierarchy由一系列cgroup以一个树状结构排列而成，每个hierarchy通过绑定对应的subsystem进行资源调度。hierarchy中的cgroup节点可以包含零或多个子节点，子节点继承父节点的属性。整个系统可以有多个hierarchy。  

Linux系统中所有进程都是通用父进程init(CentOS6，CentOS7中使用systemd)的子进程，该进程在引导是由内核执行并启动其他进程。因此所有进程都归结到一个父进程，所以Linux进程模式是一个单一层级结构，或者树结构。另外init之外的每个进程都会继承其父进程的环境(比如PATH变量)和某些属性(比如打开的文件描述符)。  

cgroup与进程在以下两点上相似:  

* cgroup是分级的
* 子cgroup会继承其父cgroup的某些属性

有区别的地方在于cgroup中可以有多个层级(如果把进程理解为一棵树的话，cgroup可以看成一个森林)


## hierarchy实践
上面说的有点抽象，直接看看hierarchy在Linux中的体现:  

在Linux中mount一个cgroup类型的文件系统时，就创建了一个hierarchy，可以使用mount查看系统中的hierarchy:  

### 查看hierarchy
```
# mount | grep cgroup
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,seclabel,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpuacct,cpu)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cgroup on /sys/fs/cgroup/net_cls type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
```

除了第一个tmpfs，其它的都是hierarchy。以挂载点/sys/fs/cgroup/memory为例，这个层级挂载在/sys/fs/cgroup/memory目录下，/sys/fs/cgroup/memory目录下的每个目录都是一个cgroup。

```
# tree -d /sys/fs/cgroup/memory/
/sys/fs/cgroup/memory/
├── bar
│   └── in_bar
├── foo
├── system.slice
│   ├── auditd.service
│   ├── _cgroup.mount
│   ├── cgroup-my_mem.mount
│   ├── chronyd.service
│   ├── cloud-config.service
│   ├── cloud-final.service
│   ├── cloud-init-local.service
│   ├── cloud-init.service
│   ├── crond.service
│   ├── dbus.service
│   ├── dev-hugepages.mount
│   ├── dev-mqueue.mount
│   ├── docker-efe5a358924ea97dce9d0e0718851964b337d6acbe7ea35c827393bf224b351b.scope
│   ├── docker.service
......
│   └── zookeeper-server.service
└── user.slice
```

比如/sys/fs/cgroup/memory/bar是层级中的一个cgroup；/sys/fs/cgroup/memory/bar/in_bar也是一个cgroup，它是/sys/fs/cgroup/memory/bar的子cgroup。


### 创建hierarchy






##ERROR
下面的理解有误

当mount一个类型为tmpfs的文件系统时(还有一点是在这个文件系统的目录下挂载类型为cgroup类型的文件系统)，就创建了一个层级。  
### 查看层级
查看系统中已有的层级:  

```
# mount | grep tmpfs
devtmpfs on /dev type devtmpfs (rw,nosuid,seclabel,size=2006596k,nr_inodes=501649,mode=755)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev,seclabel)
tmpfs on /run type tmpfs (rw,nosuid,nodev,seclabel,mode=755)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,seclabel,mode=755)
tmpfs on /run/user/985 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=404764k,mode=700,uid=985,gid=982)
tmpfs on /run/user/995 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=404764k,mode=700,uid=995,gid=993)
tmpfs on /run/user/987 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=404764k,mode=700,uid=987,gid=984)
tmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=404764k,mode=700,uid=1000,gid=1000)

# mount | grep cgroup
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,seclabel,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpuacct,cpu)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cgroup on /sys/fs/cgroup/net_cls type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
```

1. 每一个层级都是tmpfs类型的文件系统(但是tmpfs类型的文件系统不一定是一个层级)，所以先用mount | grep tmpfs看看有哪些可能的层级。
2. 然后使用mount | grep cgroup看看有哪些cgroup类型的文件系统，如果cgroup类型文件系统的挂载点路径包含tmpfs的路径，那对应的tmpfs就是一个层级；
3. 比如/sys/fs/cgroup/systemd目录挂载的文件系统类型为cgroup，并且/sys/fs/cgroup/systemd包含挂载点为/sys/fs/cgroup的tmpfs类型的文件系统；所以/sys/fs/cgroup是一个层级结构(好比一棵树，可能有多个树)



### 创建层级
创建一个层级的方法是创建一个目录，并在上面挂载tmpfs类型的文件系统。  

```
# mkdir /cgroup
# mount -t tmpfs my_cgroups /cgroup
```

上面的命令创建了一个名为my_cgroups的层级，在层级中创建cgroup就是在层级对应的目录下创建目录，然后在这个目录上挂载cgroup类型的文件系统。比如，在my_cgroups层级下创建一个名为cpu_and_mem的cgroup:  

```
# mkdir /cgroup/cpu_and_mem
# mount -t cgroup -o cpu,cpuset,memory cpu_and_mem /cgroup/cpu_and_mem

```



mkdir /cgroup/my_mem
mount -t cgroup -o memory my_mem /cgroup/my_mem

为什么/cgroup/my_mem目录的内容和/sys/fs/cgroup/memory的目录内容一样

卸载后重新挂载失败
```
# umount /cgroup/my_mem
# mount -t cgroup -o memory my_mem /cgroup/my_mem


```


## subsystem(子系统)简介

cgroup本省并没有提供资源隔离的功能，而是通过子系统(也叫控制器)来实现资源隔离的。可以通过如下的方式查看内核使用了哪些子系统:  

```
$ cat /proc/cgroups
#subsys_name	hierarchy	num_cgroups	enabled
cpuset			2			4				1
cpu				3			57				1
cpuacct		3			57				1
memory			4			57				1
devices		5			57				1
freezer		6			4				1
net_cls		7			4				1
blkio			8			57				1
perf_event	9			4				1
hugetlb		10			4				1
```

字段意思:  

* subsys_name: 子系统名称
* hierarchy: hierarchy ID
* num_cgroups: 在这个子系统中cgroup的数据
* enabled: 是否启用(1表示启用，0表示禁用)


TODO: 各个子系统的作用




# libcgroup
在CentOS6中可以使用**libcgroup**工具来维护cgroup，在CentOS7中已经不推荐使用libcgroup了。为了更好地理解cgroup，我们使用这个工具熟悉cgroup，不建议在CentOS7的生产环境中使用。  

安装libcgroup

```
# yum install libcgroup
```

安装libcgroup会自动安装cgconfig服务。  

## lssubsys
lssubsys - list hierarchies containing given subsystem.  

选项:  

* -m: 显示mount point
* -a: 显示所有的subsystem(包括mount和unmount的)

比如:  

```
# lssubsys -am
cpuset /sys/fs/cgroup/cpuset
cpu,cpuacct /sys/fs/cgroup/cpu,cpuacct
memory /sys/fs/cgroup/memory
devices /sys/fs/cgroup/devices
freezer /sys/fs/cgroup/freezer
net_cls /sys/fs/cgroup/net_cls
blkio /sys/fs/cgroup/blkio
perf_event /sys/fs/cgroup/perf_event
hugetlb /sys/fs/cgroup/hugetlb
```

## lscgroup
lscgroup的功能是列出cgroup。  

命令格式:  

```
# lscgroup [[-g] <controllers>:<path>]
```

如果不加选项，会列出系统上所有的cgroup。

如果想查看/system.slice控制组下面，附加了memory子系统的控制组，可以使用如下的命令:  

```
# lscgroup -g memory:/system.slice
memory:/system.slice/
memory:/system.slice/run-user-1000.mount
memory:/system.slice/docker-080f7a0764706130216fc4a7a7e68474e5212f352a78cc2b5efdefa467d15c0c.scope
memory:/system.slice/docker-88d48f2b9bfd4a7ee428ba9fc16b233d2538a0d11f56b94160d215191b6b3e6e.scope
memory:/system.slice/zookeeper-server.service
```












cgcreate


cgdelete











# /sys/fs/cgroup






创建控制组

```
# mkdir /sys/fs/cgroup/memory/bar
```

创建之后，会在/sys/fs/cgroup/memory/bar目录下生成一系列的文件:  

```
# ls -l /sys/fs/cgroup/memory/bar
total 0
-rw-r--r--. 1 root root 0 Apr 13 11:40 cgroup.clone_children
--w--w--w-. 1 root root 0 Apr 13 11:40 cgroup.event_control
-rw-r--r--. 1 root root 0 Apr 13 11:40 cgroup.procs
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.failcnt
--w-------. 1 root root 0 Apr 13 11:40 memory.force_empty
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.failcnt
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.limit_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.max_usage_in_bytes
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.slabinfo
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.tcp.failcnt
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.tcp.limit_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.tcp.max_usage_in_bytes
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.tcp.usage_in_bytes
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.kmem.usage_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.limit_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.max_usage_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.memsw.failcnt
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.memsw.limit_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.memsw.max_usage_in_bytes
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.memsw.usage_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.move_charge_at_immigrate
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.numa_stat
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.oom_control
----------. 1 root root 0 Apr 13 11:40 memory.pressure_level
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.soft_limit_in_bytes
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.stat
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.swappiness
-r--r--r--. 1 root root 0 Apr 13 11:40 memory.usage_in_bytes
-rw-r--r--. 1 root root 0 Apr 13 11:40 memory.use_hierarchy
-rw-r--r--. 1 root root 0 Apr 13 11:40 notify_on_release
-rw-r--r--. 1 root root 0 Apr 13 11:40 tasks
```


其中/sys/fs/cgroup/memory/bar/tasks里面存放的是这个组里面进程的pid(进程退出后，响应的pid就不在这个文件里了)。


以root用户删除为什么报Permission Denied



# 规则
### 规则1
**任何单一子系统(比如cpu)最多可以附加到一个层级中。**

比如： cpu子系统永远无法附加到两个不同的层级。  


### 规则2
**单一层级可附加一个或者多个子系统。**

比如： cpu和memory子系统都可附加到单一层级中，只要每个子系统不再附加到另一个层级即可。  


### 规则3
每次在系统中创建新层级(层级理解为树，cgroup理解为树上的结点)时，该系统中的所有任务都是那个层级的默认cgroup(我们称之为root cgroup)的初始成员。  


创建一个新的层级时，会创建一个默认的cgroup，也就是root cgroup，系统中所有的任务都会自动加入这个root cgroup。











# cgroup在docker中的使用
比如,启动了一个容器,其id为efe5a358924e,如下:

```
# docker ps
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                         NAMES
efe5a358924e        docker.io/nginx:latest   "nginx -g 'daemon off"   14 minutes ago      Up 14 minutes       0.0.0.0:8081->80/tcp, 0.0.0.0:8082->443/tcp   tender_mcnulty
```

这里以memory子系统为例,在/sys/fs/cgroup/memory/system.slice/目录下找到容器对应的cgroup

```
# ls -l /sys/fs/cgroup/memory/system.slice/ | grep efe5a358924e
drwxr-xr-x. 2 root root 0 Apr 13 15:33 docker-efe5a358924ea97dce9d0e0718851964b337d6acbe7ea35c827393bf224b351b.scope
```

查看cgroup中的tasks文件

```
# cat /sys/fs/cgroup/memory/system.slice/docker-efe5a358924ea97dce9d0e0718851964b337d6acbe7ea35c827393bf224b351b.scope/tasks
15599
15622
```

根据pid查看cgroup是应用在哪几个进程上的,可以发现,docker容器本质上是宿主机里面的进程,容器里面的进程是在宿主机里运行的。

```
# ps -f -p 15599 15622
UID        PID  PPID  C STIME TTY      STAT   TIME CMD
root     15599 15583  0 15:33 ?        Ss     0:00 nginx: master process nginx -g daemon off;
104      15622 15599  0 15:33 ?        S      0:00 nginx: worker process
```





