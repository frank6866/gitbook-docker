# 简单玩一下


创建一个deployment  

```
$ kubectl create -f http://k8s.io/docs/tutorials/stateless-application/deployment.yaml
deployment "nginx-deployment" created
```


查看deployment

```
$ kubectl describe deployment nginx-deployment
Name:			nginx-deployment
Namespace:		default
CreationTimestamp:	Mon, 27 Mar 2017 14:20:14 +0000
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
  1m		1m		1	{deployment-controller }			Normal		ScalingReplicaSet	Scaled up replica set nginx-deployment-4087004473 to 2
  ```

列出deployment创建的pods

```

```















