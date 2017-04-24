# Docker网络简介

默认安装完docker后，会添加一个名为docker0的bridge设备并添加路由，如下:  

```
# ethtool -i docker0
driver: bridge
version: 2.3
firmware-version: N/A
bus-info: N/A
supports-statistics: no
supports-test: no
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: no

# ip address show docker0
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:00:11:67:dc brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:ff:fe11:67dc/64 scope link
       valid_lft forever preferred_lft forever

# ip route
......
172.17.0.0/16 dev docker0  proto kernel  scope link  src 172.17.0.1
``` 

添加的路由表示目的网络地址为172.17.0.0/16的数据包从docker0设备发出去。  


# Docker网络模式
* bridge模式
* host模式
* container模式
* none模式

在一个宿主机上,不同的网络模式可以共存。



# demo
## 查看容器的对端设备
启动一个容器:  

```
# docker run -d nginx
c6fad6d50a57500efd29c45a52dd9b06685d36327d4a6f4b5f00523010fce969
```

查看容器内的进程在根命名空间的pid:  

```
# docker inspect --format '{{.State.Pid}}' c6fad6
18155
```

进入容器内进程所在的网络命名空间，并查看容器内eth0设备的信息:  

```
# nsenter -t 18155 -n -- ethtool -S eth0
NIC statistics:
     peer_ifindex: 104
```

可以看到对端设备为104，根据对端设备编号，查看找容器内eth0设备(veth类型)在根命名空间的对端设备:  

```
# ip link | grep 104
104: veth46493d3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT
```

可以看到上面启动的容器在根命名空间使用的是veth46493d3和容器内的eth0设备互为对端设备，查看veth46493d3的设备类型如下:  

```
# ethtool -i veth46493d3
driver: veth
version: 1.0
firmware-version:
bus-info:
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: no
```

在根命名空间内，veth46493d3默认会连接到docker0网桥上，如下:  

```
# brctl show
bridge name	bridge id		STP enabled	interfaces
docker0		8000.0242001167dc	no		veth46493d3
```


## docker命名空间为什么ip netns list看不到
在创建一个docker容器后，会发现ip netns list命令没有添加新的命名空间。

这里需要明白网络命名空间不一定是有名字的，通过ip netns add创建的网络命名空间是有名字的网络命名空间；而通过ip netns list列出的网络命名空间都是有名字的网络命名空间。

### 创建一个没有名字的命名空间
创建一个没有名字的命名空间，比如:  

```
# unshare --net /bin/bash

# readlink /proc/self/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026532772]
pid:[4026531836]
uts:[4026531838]

# readlink /proc/1/ns/*
ipc:[4026531839]
mnt:[4026531840]
net:[4026531956]
pid:[4026531836]
uts:[4026531838]

# ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```    

可以看到创建了一个编号为4026532772的网络命名空间。

### ip netns创建有名字的网络命名空间

我们使用strace观察创建一个有名字的网络命名空间的过程，如下:  

```
# strace ip netns add ns_test
execve("/sbin/ip", ["ip", "netns", "add", "ns_test"], [/* 17 vars */]) = 0
......
mkdir("/var/run/netns", 0755)           = -1 EEXIST (File exists)
mount("", "/var/run/netns", "none", MS_REC|MS_SHARED, NULL) = 0
open("/var/run/netns/ns_test", O_RDONLY|O_CREAT|O_EXCL, 0) = 4
close(4)                                = 0
unshare(CLONE_NEWNET)                   = 0
mount("/proc/self/ns/net", "/var/run/netns/ns_test", 0x43838d, MS_BIND, NULL) = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

可以看到首先在/var/run/netns目录下创建了一个和网络命名空间同名的文件ns_test。  


ip netns list命令也是从/var/run/netns目录下读取的，如下:  

```
# strace ip netns list
execve("/sbin/ip", ["ip", "netns", "list"], [/* 17 vars */]) = 0
......
openat(AT_FDCWD, "/var/run/netns", O_RDONLY|O_NONBLOCK|O_DIRECTORY|O_CLOEXEC) = 4
......
```


### 让容器的命名空间显示在ip netns list中

```
# container_id=c6fad6d5
# pid=`docker inspect -f '{{.State.Pid}}' $container_id`
# ln -s /proc/$pid/ns/net /var/run/netns/$container_id
# ip netns | grep $container_id
c6fad6d5
```




# 参考
* docker命名空间在ip netns list里面看不到的问题: http://stackoverflow.com/questions/31265993/docker-networking-namespace-not-visible-in-ip-netns-list
* http://blog.daocloud.io/docker-source-code-analysis-part7-first/





