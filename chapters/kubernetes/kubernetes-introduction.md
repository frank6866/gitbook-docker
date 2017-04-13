# Kubernetes介绍
Kubernetes是一个开源的容器管理平台，可以自动化地进行一些容器操作，比如部署、调度和伸缩。  

k8s编排容器的操作：

* 自动化部署容器，对容器做复制
* 非常快地对容器进行扩缩容操作
* 对容器进行分组，还可以对这个组内的容器做LB
* 非常容易对应用程序的新版本容器做滚动更新
* 提供弹性的功能，如果容器终止了，马上可以被替换。



# 概念
![kubernetes_cluster](resources/kubernetes_cluster.png)


## cluster
cluster是一组物理或者虚拟的node(结点，结点上面运行着操作系统),在Kubernetes中包含两种类型的结点:  

* master
* node

## master
Kubernetes master对集群提供了统一的视图，master主要包含下面的功能：

1. api server：主要提供了和集群交互的rest endpoint
2. replication controller：主要作用是创建和复制pods


## node
node在早期的版本中称为Minion，是Kubernetes里面干活的角色，每个node都会运行下面的服务：

1. kubelet：是一个主要的node agent
2. kube-proxy：被service使用来代理连接（todo：详细过程）
3. docker或者rocket：k8s用来创建容器的技术



## pod
pod(豆荚，很形象的比喻，里面的豆子就是容器)是Kubernetes中最小的部署单元(部署单元是指可以被Kubernetes创建、调度和管理的单元)。

## label
label是附加到pod上的键值对，用来传递用户自定义的属性。

## replication controller
replication controller保证在任何时间，特定数量的的pods副本在运行。如果我们为一个pod创建了一个replication controller并且指定了副本数为3，replication controller会创建3个pods并持续监控这些pods。如果一个pod终止了，那么replication controller会替换这个pod来保证有3个pod。

## service
现在我们已经创建了很多pod的副本，那么如何在他们之间做lb，答案是service。

概念：service
回到上面提到的问题：如果容器是临时的，重启后IP可能发生变化，那么前端容器怎么稳定地访问后端容器呢？

service是一个抽象，service定义了一系列pod和访问他们的策略。service通过label找到pods组。由于service是抽象的，在一般的图表里面看不到，所以很难理解这个概念。



## kubectl
kubectl是一个和Kubernetes API交互的客户端工具。






# todo
事实上，通过k8s只需要一个配置文件和一行命令，我们就可以部署一个包含多层架构的应用（比如前端和后端）。
kubectl create -f app1.yaml






# 参考链接
* [http://omerio.com/2015/12/18/learn-the-kubernetes-key-concepts-in-10-minutes/](http://omerio.com/2015/12/18/learn-the-kubernetes-key-concepts-in-10-minutes/)



























