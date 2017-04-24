# web ui


# 安装
不同版本的yml文件不一样,这里以1.5为例。(在https://github.com/kubernetes/dashboard/tree/v1.5.1/src/deploy里切换到不同版本,下载对应的文件)

vi kubernetes-dashboard.yaml

```
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Configuration to deploy release version of the Dashboard UI.
#
# Example usage: kubectl create -f <this_file>

kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  labels:
    app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubernetes-dashboard
  template:
    metadata:
      labels:
        app: kubernetes-dashboard
      # Comment the following annotation if Dashboard must not be deployed on master
      annotations:
        scheduler.alpha.kubernetes.io/tolerations: |
          [
            {
              "key": "dedicated",
              "operator": "Equal",
              "value": "master",
              "effect": "NoSchedule"
            }
          ]
    spec:
      containers:
      - name: kubernetes-dashboard
        image: gcr.io/google_containers/kubernetes-dashboard-amd64:v1.5.1
        imagePullPolicy: Always
        ports:
        - containerPort: 9090
          protocol: TCP
        args:
          # Uncomment the following line to manually specify Kubernetes API server Host
          # If not specified, Dashboard will attempt to auto discover the API server and connect
          # to it. Uncomment only if the default does not work.
          # - --apiserver-host=http://my-address:port
          - --apiserver-host=http://10.12.10.209:8080
        livenessProbe:
          httpGet:
            path: /
            port: 9090
          initialDelaySeconds: 30
          timeoutSeconds: 30
---
kind: Service
apiVersion: v1
metadata:
  labels:
    app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 9090
  selector:
    app: kubernetes-dashboard

```


```
# kubectl create -f kubernetes-dashboard.yaml
deployment "kubernetes-dashboard" created
service "kubernetes-dashboard" created
```

查看deployment和service

```
# kubectl get deployments --namespace=kube-system
NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-dashboard   1         1         1            0           2m

# kubectl get service --namespace=kube-system
NAME                   CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes-dashboard   10.254.0.192   <nodes>       80:31297/TCP   17s
```

查看pod信息

```
# kubectl get pods --namespace=kube-system
NAME                                    READY     STATUS             RESTARTS   AGE
kubernetes-dashboard-3203831700-twh16   0/1       CrashLoopBackOff   4          3m
```


发现pod的状态是CrashLoopBackOff，查看pod的日志:  

```
# kubectl logs kubernetes-dashboard-3203831700-twh16 --namespace=kube-system
Error from server: Get https://10.12.10.200:10250/containerLogs/kube-system/kubernetes-dashboard-3203831700-twh16/kubernetes-dashboard: dial tcp 10.12.10.200:10250: getsockopt: connection refused
```

在node节点上vi /etc/kubernetes/kubelet，KUBELET_ADDRESS修改为KUBELET_ADDRESS="--address=0.0.0.0"

然后重启kubelet

systemctl restart kubelet

再查看日志:  

```
# kubectl logs kubernetes-dashboard-3203831700-twh16 --namespace=kube-system
Using HTTP port: 9090
Error while initializing connection to Kubernetes apiserver. This most likely means that the cluster is misconfigured (e.g., it has invalid apiserver certificates or service accounts configuration) or the --apiserver-host param points to a server that does not exist. Reason: invalid configuration: no configuration has been provided
Refer to the troubleshooting guide for more information: https://github.com/kubernetes/dashboard/blob/master/docs/user-guide/troubleshooting.md
```

发现是参数可能没有配置，编辑kubernetes-dashboard.yaml文件，对参数--apiserver-host取消注释，取值和node节点上/etc/kubernetes/kubelet上的KUBELET_API_SERVER是一个值(比如http://a.b.c.d:8080)

然后重新应用配置

```
# kubectl apply -f kubernetes-dashboard.yaml
```

此时Dashboard就起来了:  

```
# kubectl get pods --namespace=kube-system
NAME                                   READY     STATUS    RESTARTS   AGE
kubernetes-dashboard-771859086-ksds4   1/1       Running   0          4m
```











