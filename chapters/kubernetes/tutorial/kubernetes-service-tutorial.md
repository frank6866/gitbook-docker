# service tutorial
外部程序可以使用service访问运行在集群中的应用。service对有两个实例的app提供了负载均衡。

参考[https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/)

## 创建deployment
```
# kubectl run hello-world --replicas=2 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8080
deployment "hello-world" created
```

上面的命令会创建一个名为hello-world的deployment，并且副本数为2.

```
# kubectl get deployment
NAME          DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
hello-world   2         2         2            0           2m
```

## 创建service
创建一个service，对外暴露deployment服务:  

```
# kubectl expose deployment hello-world --type=NodePort --name=example-service
service "example-service" exposed
```

Display information about the Service:

```
# kubectl describe services example-service
Name:				example-service
Namespace:			default
Labels:				run=load-balancer-example
Selector:			run=load-balancer-example
Type:				NodePort
IP:					10.254.240.83
Port:				<unset>	8080/TCP
NodePort:			<unset>	31969/TCP
Endpoints:			10.1.36.2:8080,10.1.51.2:8080
Session Affinity:	None
No events.
```

记下NodePort的值，比如上面的31969



## 访问服务
List the pods that are running the Hello World application:

```
# kubectl get pods --selector="run=load-balancer-example" --output=wide
NAME                           READY     STATUS    RESTARTS   AGE       IP          NODE
hello-world-2895499144-8bc0x   1/1       Running   0          8m        10.1.51.2   10.12.10.200
hello-world-2895499144-kr8zf   1/1       Running   0          8m        10.1.36.2   10.12.10.210
```

以hello-world-2895499144-8bc0x这个pod为例，它运行在10.12.10.200这个node上面，使用上面的NodePort就可以访问容器中的服务了。 如下:  

```
# curl 10.12.10.200:31969
Hello Kubernetes!
```

## 删除service
```
# kubectl delete services example-service
service "example-service" deleted
```






