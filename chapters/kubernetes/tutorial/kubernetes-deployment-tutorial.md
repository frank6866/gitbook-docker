# deployment tutorial

参考: [https://kubernetes.io/docs/tutorials/stateless-application/run-stateless-application-deployment/](https://kubernetes.io/docs/tutorials/stateless-application/run-stateless-application-deployment/)

## 创建deployment
### 创建一个deployment
Create a Deployment based on the YAML file:

vi ngnix-deployment.yml

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2 # tells deployment to run 2 pods matching the template
  template: # create pods using pod definition in this template
    metadata:
      # unlike pod-nginx.yaml, the name is not included in the meta data as a unique name is
      # generated from the deployment name
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

```
# kubectl create -f ngnix-deployment.yml
deployment "nginx-deployment" created
```

### 列出所有的deployment

```
# kubectl get deployment
NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2         0         0            0           1m
```

### 查看deployment
Display information about the Deployment:

```
# kubectl describe deployment nginx-deployment
Name:			nginx-deployment
Namespace:		default
CreationTimestamp:	Mon, 24 Apr 2017 04:27:04 +0000
Labels:			app=nginx
Selector:		app=nginx
Replicas:		0 updated | 2 total | 0 available | 2 unavailable
StrategyType:		RollingUpdate
MinReadySeconds:	0
RollingUpdateStrategy:	1 max unavailable, 1 max surge
Conditions:
  Type			Status	Reason
  ----			------	------
  Available 		False	MinimumReplicasUnavailable
  ReplicaFailure 	True	FailedCreate
OldReplicaSets:		<none>
NewReplicaSet:		nginx-deployment-4087004473 (0/2 replicas created)
Events:
  FirstSeen	LastSeen	Count	From				SubObjectPath	Type		Reason			Message
  ---------	--------	-----	----				-------------	--------	------			-------
  3m		3m		1	{deployment-controller }			Normal		ScalingReplicaSet	Scaled up replica set nginx-deployment-4087004473 to 2
```

看到ReplicaFailure为True，说明有异常:

查看日志/var/log/message

```
kube-controller-manager: E0424 05:41:33.832108   22494 replica_set.go:448] Sync "default/nginx-deployment-4087004473" failed with unable to create pods: No API token found for service account "default", retry after the token is automatically created and added to the service account
```

解决:
去掉/etc/kubernetes/apiserver文件中KUBE_ADMISSION_CONTROL的ServiceAccount，然后重启kube-apiserver服务(systemctl restart kube-apiserver)

List the pods created by the deployment:

```
# kubectl get pods -l app=nginx
NAME                                READY     STATUS              RESTARTS   AGE
nginx-deployment-4087004473-14lc1   0/1       ContainerCreating   0          1m
nginx-deployment-4087004473-xdfk2   0/1       ContainerCreating   0          1m
```

ContainerCreating表示正在创建容器，第一次在某个node上创建容器的时候，要下载镜像，会慢一点。


### 查看某个pod的详细信息

```
# kubectl describe pod nginx-deployment-4087004473-14lc1
```

## 变更创建的deployment的镜像
比如上面使用的是nginx的1.7.9版本，现在想把nginx的版本升级到1.8

首先修改ngnix-deployment.yml，将image修改为nginx:1.8。

```
# kubectl apply -f ngnix-deployment.yml
deployment "nginx-deployment" configured
```

观察pods会发现，会创建新的pod，然后将1.7.9版本nginx的pod删掉。

```
# watch kubectl get pods -l app=nginx
```

## 变更创建的deployment中pod副本数
比如上面使用的副本数是2(replicas: 2)，现在想调大副本数到4.

首先修改ngnix-deployment.yml，将replicas修改为4。

```
# kubectl apply -f ngnix-deployment.yml
deployment "nginx-deployment" configured
```

观察pods会发现，会创建四个pods

```
# watch kubectl get pods -l app=nginx
```

## 删除一个deployment
```
# kubectl delete deployment nginx-deployment
deployment "nginx-deployment" deleted
```

删除一个deployment后，下面的pods会自动被删除。


# 异常
## couldn't find type: v1beta1.Deployment
执行kubectl create -f ngnix-deployment.yml时，报错

```
error: error validating "ngnix-deployment.yml": error validating data: couldn't find type: v1beta1.Deployment; if you choose to ignore these errors, turn validation off with --validate=false
```

解决:
将yml文件中的**apiVersion: apps/v1beta1**修改为**apiVersion: extensions/v1beta1**。
eployments.extensions "nginx-deployment" already exists


