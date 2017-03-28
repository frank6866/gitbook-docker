# 异常整理


## 两套k8s环境干扰
### 现象
第二套k8s环境的master指向了第一套k8s环境的etcd，在第二套环境中使用**kubectl get nodes**命令可以看到第一套环境的结点

### TODO
k8s是如何使用etcd的？应该不会是一套k8s独占一套etcd



## lock is held by xxx and has not yet expired
### 现象
详细日志  

```
kube-controller-manager: I0328 04:34:09.106220   16430 leaderelection.go:247] lock is held by nl-cloud-dyc-k8s-1 and has not yet expired
```










