# 配置



# master
##apiserver

KUBE_API_ARGS表示命令行选项的值, 全部选项参见[官网](https://kubernetes.io/docs/admin/kube-apiserver/),

比如,kubernetes在etcd中默认的路径前缀是/registry,可以通过下面的配置修改为/foo

> KUBE_API_ARGS="--etcd-prefix=/foo"

