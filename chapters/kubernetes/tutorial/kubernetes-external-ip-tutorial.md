# external ip tutorial
参考: [https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/)

本文简述了创建一个对外暴露IP地址的service对象。  


```
kubectl run hello-world --replicas=5 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8080


--load-balancer-ip='A.B.C.D'

kubectl expose deployment hello-world --type=LoadBalancer --name=my-service  

kubectl expose deployment hello-node3 --type="LoadBalancer--target-port=8080 --load-balancer-ip='A.B.C.D'

```



```
# kubectl get services my-service
NAME         CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
my-service   10.254.163.151   <pending>     8080:31781/TCP   19s
```

Note: If the external IP address is shown as <pending>, wait for a minute and enter the same command again.


检查/etc/kubernetes/apiserver文件里，KUBE_SERVICE_ADDRESSES中--service-cluster-ip-range选项是否配置为可以被外部访问的网段(一般配置为宿主机所在的网段)。

更改后需要

KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"


KUBE_SERVICE_ADDRESSES="--portal_net=192.168.56.150/28"



curl http://<external-ip>:<port>


