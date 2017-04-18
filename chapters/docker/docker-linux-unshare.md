# unshare
unshare - run program with some namespaces unshared from parent.

**unshare()系统调用**用于将当前进程和所在的namespace分离并且加入到新创建的namespace之中。

unshare也是一个命令，格式如下:  

```
unshare [options] program [arguments]
```

版本信息如下:  

```
# cat /etc/redhat-release
Derived from Red Hat Enterprise Linux 7.1 (Source)
# unshare --version
unshare from util-linux 2.23.2
```

unshare命令可以从父进程的namespace中脱离出来并在新的namespace执行指定的program，可以脱离的命名空间及相关选项如下:  

* -i: 或者--ipc，表示从父进程的IPC namespace中脱离出来
* -m: 或者--mount，表示从父进程的mount namespace中脱离出来
* -n: 或者--net，表示从父进程的network namespace中脱离出来
* -p: 或者--pid，表示从父进程的pid namespace中脱离出来
* -u: 或者--uts，表示从父进程的UTS namespace中脱离出来

这里没有proc和user namespace。  


在使用-i选项脱离父进程的pid namespace的时候，还有两个有用的选项:  

* -f: 或者--fork，在子进程中运行program而不是直接运行program。
* --mount-proc[=mountpoint]: 在运行program前，mount proc文件系统到mountpoint(默认是/proc)。



# uts
在当前进程中查看pid及其对应的namespace编号，如下:  

```
# echo $$
16385
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026531838]
```

使用unshare从父进程的uts namespace中脱离出来，并加入一个新的namespace中去:  

```
# unshare --uts /bin/bash
# echo $$
16419
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026532157]
```

发现除了uts，其他的namespace都是一样的。  


在进程内修改主机名不会影响物理机的主机名:  

```
# hostname container01
# bash
[root@container01 ~]# exit
exit
# exit
exit
#
```


# pid
在当前进程中查看pid及其对应的namespace编号，如下: 

```
# echo $$
2854
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026531838]
```


## 不挂载/proc
```
# unshare --pid -f /bin/bash
```

查看当前进程的pid，发现变为1，说明pid已经隔离了。

```
# echo $$
1
```

查看当前进程的命名空间，其实看到的是root namespace中pid为1的进程的命名空间，ps命令是从/proc目录中读取的信息，所以看到的还是root namespace中的信息。  
因为/proc文件系统没有重新挂载。  

```
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026531838]

# ps
  PID TTY          TIME CMD
 3360 pts/1    00:00:00 sudo
 3361 pts/1    00:00:00 su
 3362 pts/1    00:00:00 bash
 3387 pts/1    00:00:00 unshare
 3388 pts/1    00:00:00 bash
 3420 pts/1    00:00:00 ps
```




## 挂载/proc(--mount-proc)
使用unshare从父进程的uts namespace中脱离出来，并加入一个新的namespace中去:  

```
# echo $$
3645
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026531838]
```

发现加上了--mount-proc选项，除了脱离父进程的pid namespace，还脱离了mnt namespace。

```
# unshare --pid -f --mount-proc /bin/bash
# echo $$
1
# readlink /proc/$$/ns/*
ipc:[4026531839]
mnt:[4026532157]
net:[4026531956]
pid:[4026532158]
uts:[4026531838]

```

进程在加入新的mnt namespace时，会拷贝父进程的mount信息；使用--mount-proc选项，会在新的mnt namespace中将procfs挂载到/proc目录下。所以下面有两个proc类型的文件系统:  

```
# mount -l -t proc
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
```

挂载procfs的时候，是不是会将这个命名空间下的pid信息写入到/proc目录；貌似是这个文件系统一挂载，里面就有信息，比如pid信息(pid信息是从pid namespace获取来的？)

```
# ls /proc
1       buddyinfo  consoles  diskstats    fb           iomem     kcore      kpagecount  mdstat   mounts        partitions   slabinfo  sys            timer_stats  vmallocinfo
17      bus        cpuinfo   dma          filesystems  ioports   keys       kpageflags  meminfo  mtrr          sched_debug  softirqs  sysrq-trigger  tty          vmstat
acpi    cgroups    crypto    driver       fs           irq       key-users  loadavg     misc     net           scsi         stat      sysvipc        uptime       zoneinfo
asound  cmdline    devices   execdomains  interrupts   kallsyms  kmsg       locks       modules  pagetypeinfo  self         swaps     timer_list     version
```

再次使用ps命令，可以看到pid是pid namespace里面的pid信息(因为root namespace里面pid为1的进程不可能是/bin/bash)

```
# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 09:29 pts/0    00:00:00 /bin/bash
root        15     1  0 09:29 pts/0    00:00:00 ps -ef
```

