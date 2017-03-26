# kubernetes安装

## 参考链接
* [http://www.fangyunlin.com/?p=54](http://www.fangyunlin.com/?p=54)


## 软件版本
这是安装完成后在主机上查询的

```
# master上
$ rpm -qa | grep etcd
etcd-3.1.0-2.el7.x86_64

$ rpm -qa | grep kubernetes
kubernetes-client-1.5.2-0.2.gitc55cf2b.el7.x86_64
kubernetes-master-1.5.2-0.2.gitc55cf2b.el7.x86_64

# node上

$ rpm -qa | grep kubernetes
kubernetes-client-1.5.2-0.2.gitc55cf2b.el7.x86_64
kubernetes-node-1.5.2-0.2.gitc55cf2b.el7.x86_64

$ rpm -qa | grep flannel
flannel-0.7.0-1.el7.x86_64

$ rpm -qa | grep docker
docker-common-1.12.6-11.el7.centos.x86_64
docker-1.12.6-11.el7.centos.x86_64
docker-client-1.12.6-11.el7.centos.x86_64
```


## 主机信息
| role | hostname | ip
|------|----------|---
| master | nl-cloud-dyc-k8s-1 | 10.12.10.209
| node | nl-cloud-dyc-k8s-2 | 10.12.10.200
| node | nl-cloud-dyc-k8s-3 | 10.12.10.210

由于本例中的主机是在OpenStack环境中使用provider网络创建的虚拟机，IP是随机dhcp的，所以看起来不连续，等会配置的时候再来找一下，免得配错了。  

## 准备工作
### etcd
kubernetes的配置信息存储在etcd中，需要有一套etcd的环境(这里假设已经在上面的三台机器上部署了一套etcd集群，etcd_servers=http://10.12.10.209:2379,http://10.12.10.200:2379,http://10.12.10.210:2379)。


### DNS
主机间可以通过域名相互访问，如果主机没有在DNS服务器上注册，需要配置各个主机的/etc/hosts文件


## master安装与配置
**在nl-cloud-dyc-k8s-1主机上执行下面的操作.**

### 安装
> $ sudo yum install -y kubernetes-master


### 配置
修改前先备份配置文件便于回滚:

> $ sudo cp -r /etc/kubernetes/ /etc/kubernetes.bak


kubernetes master的配置文件存放的位置是/etc/kubernetes，master上主要有4个文件:

* apiserver: kube-apiserver的配置文件
* config: kubernetes system config，保存的是k8s系统的配置
* controller-manager:
* scheduler:


#### apiserver
| name | required | explain | default
|-----------|--------|----------|-------
| KUBE_API_ADDRESS | yes | The address on the local server to listen to. |  "--insecure-bind-address=127.0.0.1"
| KUBE_API_PORT | no | The port on the local server to listen on. |  "--port=8080"
| KUBELET_PORT | no | Port minions listen on |  "--kubelet-port=10250"
| KUBE_ETCD_SERVERS | yes | Comma separated list of nodes in the etcd cluster |  "--etcd-servers=http://127.0.0.1:2379"
| KUBE_SERVICE_ADDRESSES | yes | Address range to use for services |  "--service-cluster-ip-range=10.254.0.0/16"
| KUBE_ADMISSION_CONTROL | yes | default admission control policies |  "--admission-control=NamespaceLifecycle,<br>NamespaceExists,LimitRanger,SecurityContextDeny,<br>ServiceAccount,ResourceQuota"
| KUBE_API_ARGS | no | 命令行参数 |  没有默认值，自定义



需要修改的配置项

1. KUBE_API_ADDRESS: 修改为"--address=0.0.0.0"
2. KUBE_ETCD_SERVERS: 修改为"--etcd_servers=http://10.12.10.209:2379,http://10.12.10.200:2379,http://10.12.10.210:2379"

修改后配置文件如下:

```
$ grep -v '^#\|^$' /etc/kubernetes/apiserver
KUBE_API_ADDRESS="--address=0.0.0.0"
KUBE_ETCD_SERVERS="--etcd_servers=http://10.12.10.209:2379,http://10.12.10.200:2379,http://10.12.10.210:2379"
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"
KUBE_API_ARGS=""
```


#### config
该文件是kubernetes system config，保存的是k8s系统的配置。 这个文件里的配置会影响到所有的k8s服务，包括:

* kube-apiserver.service
* kube-controller-manager.service
* kube-scheduler.service
* kubelet.service
* kube-proxy.service


需要修改的地方

* KUBE_MASTER: 由于master是10.12.10.209，所以这里修改为"--master=http://10.12.10.209:8080"

修改后配置文件内容如下:

```
$ grep -v '^#\|^$' /etc/kubernetes/config
KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=false"
KUBE_MASTER="--master=http://10.12.10.209:8080"
```







TODO: 配置项说明

```
KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow_privileged=false"
KUBE_MASTER="--master=http://192.168.1.247:8080"
```



```

###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://127.0.0.1:8080"
```


#### controller-manager


```
$ grep -v '^#\|^$' /etc/kubernetes/controller-manager
KUBE_CONTROLLER_MANAGER_ARGS="--node-monitor-grace-period=10s --pod-eviction-timeout=10s"
```


#### TODO
scheduler配置文件解析及config和controller-manager配置配置项详细说明。



### 启动master服务
```
$ sudo systemctl enable kube-apiserver kube-scheduler kube-controller-manager
$ sudo systemctl start kube-apiserver kube-scheduler kube-controller-manager
```




## node安装与配置
**在nl-cloud-dyc-k8s-2和nl-cloud-dyc-k8s-3上执行下面的操作.**

### 安装

> $ sudo yum install -y kubernetes-node flannel docker


### 配置
修改前先备份配置文件便于回滚:

> $ sudo cp -r /etc/kubernetes/ /etc/kubernetes.bak



kubernetes node的配置文件存放的位置是/etc/kubernetes，node上主要有3个文件:

* config: kubernetes system config，保存的是k8s系统的配置
* kubelet: kubernetes kubelet (minion) config，这个文件主要是对工作节点(minion)的配置
* proxy:


#### config文件
配置项说明参考master，主要是把KUBE_MASTER修改为指向master


* KUBE_MASTER: 由于master是10.12.10.209，所以这里修改为"--master=http://10.12.10.209:8080"

修改后配置文件内容如下:

```
$ grep -v '^#\|^$' /etc/kubernetes/config
KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=false"
KUBE_MASTER="--master=http://10.12.10.209:8080"
```

#### kubelet文件
kubernetes kubelet (minion) config，这个文件主要是对工作节点(minion)的配置。

需要修改的地方:

* KUBELET_HOSTNAME: ip地址替换为本机IP，比如nl-cloud-dyc-k8s-2的ip是10.12.10.200，就修改为"--hostname-override=10.12.10.200"
* KUBELET_API_SERVER: 将ip修改为master的ip，比如这个测试集群中master的地址是10.12.10.209，就修改为"--api-servers=http://10.12.10.209:8080"


修改后配置文件内容如下（这里是在nl-cloud-dyc-k8s-2看到的结果，在nl-cloud-dyc-k8s-3上KUBELET_HOSTNAME中的IP地址为nl-cloud-dyc-k8s-3上的IP地址）:

```
$ grep -v '^#\|^$' /etc/kubernetes/kubelet
KUBELET_ADDRESS="--address=127.0.0.1"
KUBELET_HOSTNAME="--hostname-override=10.12.10.200"
KUBELET_API_SERVER="--api-servers=http://10.12.10.209:8080"
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"
KUBELET_ARGS=""
```

#### proxy
TODO


### 启动服务

```
$ sudo systemctl enable kubelet kube-proxy
$ sudo systemctl start kubelet kube-proxy
```


## flannel
flannel网络配置

初始化flannel的etcd配置(在etcd节点的任何一台机器上执行下面的命令):

> etcdctl set /coreos.com/network/config '{ "Network": "10.1.0.0/16" }'


flannel配置文件的路径是**/etc/sysconfig/flanneld**，需要修改两个配置项:

* FLANNEL_ETCD: etcd url location. Point this to the server where etcd runs。修改为运行etcd服务器的地址，可以配置为etcd集群，比如，本例中修改为"http://10.12.10.209:2379,http://10.12.10.200:2379,http://10.12.10.210:2379"
* FLANNEL_ETCD_PREFIX: etcd config key.  This is the configuration key that flannel queries for address range assignment.这是flannel查询etcd中保存的网络信息使用的key，本例中值设置为上面创建的/coreos.com/network


修改后配置文件如下（注意，所有的node结点都需要修改）:
```
$ grep -v '^#\|^$' /etc/sysconfig/flanneld
FLANNEL_ETCD_ENDPOINTS="http://10.12.10.209:2379,http://10.12.10.200:2379,http://10.12.10.210:2379"
FLANNEL_ETCD_PREFIX="/coreos.com/network"
```


启动flannel和docker（注意，所有的node结点都需要执行下面的命令）:

```
$ sudo systemctl enable flanneld docker
$ sudo systemctl start flanneld docker
```



## 验证

TODO
