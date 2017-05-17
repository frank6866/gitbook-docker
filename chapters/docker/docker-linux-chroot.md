# chroot
chroot - run command or interactive shell with special root directory。  

chroot可以一个命令或者shell指定一个特定的root目录；chroot是*nix系统的一个操作，可以改变进程及其子进程的根目录。

chroot jail: 由chroot创造出来的那个目录，叫做chroot jail或者chroot prison。  


# 好处
## 安全性
使用chroot后，在新的根目录下访问不了原来根目录的文件，增强了系统的安全性

## 应急
比如进入单用户模式下修复文件系统及修改root密码，参考[https://frank6866.gitbooks.io/tools/content/chapters/linux/linux-single-user-mode.html](https://frank6866.gitbooks.io/tools/content/chapters/linux/linux-single-user-mode.html)



# 使用

## 命令格式
```
chroot [OPTION] NEWROOT [COMMAND [ARG]...]
```

```
If no command is given, run '${SHELL} -i' (default: '/bin/sh -i').
```

如果没有指定命令。比如，在chroot之前，默认的shell如下: 

```
# echo $SHELL
/bin/bash
```

在chroot之后，会执行$SHELL -i命令。  


## demo
测试环境为CentOS7.1。

这里以busybox(busybox的使用参见[https://docker.frank6866.com/chapters/docker/docker-busybox.html](https://docker.frank6866.com/chapters/docker/docker-busybox.html))为例子，


```
# mkdir /root/tutorial
# cd /root/tutorial
# pwd
/root/tutorial
# chroot /root/tutorial/
chroot: failed to run command ‘/bin/bash’: No such file or directory
```

chroot时如果不指定参数，chroot到一个新目录后，会执行$SHELL -i命令；这个例子会在新目录(/root/tutorial)下执行/bin/bash命令，没有找到命令，就报错了。  

将/bin/bash拷贝到/root/tutorial目录下

```
# mkdir /root/tutorial/bin
# cp /bin/bash /root/tutorial/bin
# chroot /root/tutorial/
chroot: failed to run command ‘/bin/bash’: No such file or directory
```

还是报错，用strace看一下，提示信息和上面一下，没有有价值的信息。于是Google一下(参考[这篇博客](https://www.zhukun.net/archives/6831))，发现是/bin/bash的依赖包没有拷贝进来

```
# cd /root/tutorial
# ldd /bin/bash
	linux-vdso.so.1 =>  (0x00007fff8294d000)
	libtinfo.so.5 => /lib64/libtinfo.so.5 (0x00007f89afd38000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f89afb34000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f89af772000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f89aff6a000)
# mkdir lib64
# cp /lib64/libtinfo.so.5 lib64/
# cp /lib64/libdl.so.2 lib64/
# cp /lib64/libc.so.6 lib64/
# cp /lib64/ld-linux-x86-64.so.2 lib64/
# chroot /root/tutorial/ 
# Ctrl+D退出
```

chroot成功，Ctrl+D可以退出.(由于现在没有logout命令，执行logout会提示找不到)



先退出chroot，下载busybox，然后chroot进去

```
# cd /root/tutorial
# wget https://busybox.net/downloads/binaries/1.21.1/busybox-x86_64
# chmod a+x busybox-x86_64
# chroot /root/tutorial/
```

由于新的root下面没有ls命令，所以执行ls会提示找不到命令。可以使用busybox中的ls命令查看文件。

```
# chroot /root/tutorial/
bash-4.2# pwd
/
bash-4.2# ls
bash: ls: command not found
bash-4.2# ./busybox-x86_64 ls
bin             busybox-x86_64  lib64
```


# 参考
* man chroot
* https://zh.wikipedia.org/wiki/Chroot
* https://www.ibm.com/developerworks/cn/linux/l-cn-chroot/
