# 后端存储基准测试


内核基于**4.9.14-1**.el7.centos.x86_64 #1 SMP Sun Mar 12 14:42:37 EDT 2017 x86_64 x86_64 x86_64 GNU/Linux



# 内核升级
> vi /etc/yum.repos.d/eleme.repo

```
[eleme]
name=Eleme All-in-one RPM Repo
baseurl=http://os.elenet.me/repo/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
```

> yum clean;yum makecache

查看现有内核版本

> uname -a

输出:  

> Linux nl-cloud-openstack-5 3.10.0-327.36.3.el7.x86_64 #1 SMP Mon Oct 24 16:09:20 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux


> rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm


> vi elrepo.repo

修改[elrepo-kernel]的enable为1，启用这个仓库

yum --enablerepo=elrepo-kernel install kernel-ml


grub2-set-default 0



重启机器




yum -y install kernel-lt-aufs kernel-lt-aufs-tools


cat /proc/filesystems  | grep aufs


dockerd --storage-driver=aufs&


dockerd --storage-driver=devicemapper&


dockerd --storage-driver=overlay2&





ln -s /usr/libexec/docker/docker-runc /usr/local/sbin/docker-runc
ln -s /usr/bin/docker-runc /usr/libexec/docker/docker-runc

My workaround is to create symbolic link /usr/local/sbin/docker-runc -> /usr/libexec/docker/docker-runc

devicemapper


# aufs 
## 安装







# script

参数：创建虚拟机的个数(默认10个)，镜像的名称


创建后删掉












# ref

2017-02-13

目前再测的4.9内核，使用了Spaceduck上的预编译版本，该版本有包括小米在内的多家国内公司在用，稳定性经过测试有一定的口碑。

办公室测试环境的安装源配置，

[eleme]
name=Eleme All-in-one RPM Repo
baseurl=http://os.elenet.me/repo/centos/$releasever/$basearch/
gpgcheck=0
enabled=1

生产环境的安装源配置，

[eleme]
name= Custom package for eleme
baseurl=http://mirrors.elenet.me/eleme/centos/$releasever/os/x86_64
gpgcheck=0
enabled=1
对应新Kernel的软件包名为 kernel-lt-aufs，安装完 kernel-lt-aufs 后，需要设置系统使用新内核重启，具体方法 参考CentOS官方的Grub2介绍 。

文件



# docker基准测试

# 启动容器时间
## 环境信息
### 内核版本
内核版本为4.9.14，如下

> $ uname -a

输出

> Linux nl-cloud-openstack-5 4.9.14-1.el7.centos.x86_64 #1 SMP Sun Mar 12 14:42:37 EDT 2017 x86_64 x86_64 x86_64 GNU/Linux

### aufs版本
aufs版本版本为kernel-lt-aufs-4.9.14，如下

> $ rpm -qa | grep aufs

输出

> kernel-lt-aufs-4.9.14-1.el7.centos.x86_64

## 测试脚本
测试启动nginx容器所花的时间，运行100次，计算平均时间，脚本如下：  

> $ vi docker_benchmark.py

脚本内容如下：  

```
import subprocess
import time

if __name__ == '__main__':
    subprocess.check_output(['docker pull nginx'], shell=True)
    execute_count = 100
    run_command = "docker run -d nginx"
    kill_command = "docker rm -f $(docker ps -a -q)"
    total_time = 0

    for i in xrange(execute_count):
        start = time.time()
        subprocess.check_output([run_command], shell=True)
        end = time.time()
        one_time = end-start
        total_time += one_time
        time.sleep(3)
        subprocess.check_output([kill_command], shell=True)

    print "creating time per container is: %s" % str(total_time/execute_count)
```

## 运行结果
### aufs
启动命令

> dockerd --storage-driver=aufs&

> python docker_benchmark.py

运行结果

> creating time per container is: 0.602060251236

使用aufs，启动一个nginx容器的平均时间是**0.6**秒


### device mapper
启动命令

> dockerd --storage-driver=devicemapper&

> python docker_benchmark.py

> creating time per container is: 1.15359771729

使用device mapper，启动一个nginx容器的平均时间是**1.15**秒




# ref 内核升级
https://www.ostechnix.com/install-linux-kernel-4-10-centos-ubuntu/
https://havee.me/linux/2017-01/upgrade-kernel-4-9-for-centos.html
