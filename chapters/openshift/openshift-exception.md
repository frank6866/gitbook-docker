# 异常

## User xxx cannot get replicationcontrollers in project yyy

创建一个app时报错:


Use the public Docker Hub MySQL image to create an app. Generated artifacts will be labeled with db=mysql

```
# oc new-app mysql MYSQL_USER=user MYSQL_PASSWORD=pass MYSQL_DATABASE=testdb -l db=mysql
--> Found Docker image 5faba1a (6 days old) from Docker Hub for "mysql"

    * An image stream will be created as "mysql:latest" that will track this image
    * This image will be deployed in deployment config "mysql"
    * Port 3306/tcp will be load balanced by service "mysql"
      * Other containers can access this service through the hostname "mysql"
    * This image declares volumes and will default to use non-persistent, host-local storage.
      You can add persistent volumes later by running 'volume dc/mysql --add ...'
    * WARNING: Image "mysql" runs as the 'root' user which may not be permitted by your cluster administrator

--> Creating resources with label db=mysql ...
    imagestream "mysql" created
    deploymentconfig "mysql" created
    service "mysql" created
--> Success
    WARNING: No Docker registry has been configured with the server. Automatic builds and deployments may not function.
    Run 'oc status' to view your app.
```

排障思路:

1. 先用 **oc status -v** 查看状态
2. 如果发现failed,使用 **oc logs xxx** 查看错误日志

如下:

```
# oc status -v
In project spark-cluster on server https://10.12.10.18:8443

svc/mysql - 172.30.12.118:3306
  dc/mysql deploys istag/mysql:latest
    deployment #1 failed about a minute ago: image change

...
```

```
# oc logs dc/mysql
error: couldn't get deployment mysql-1: User "system:serviceaccount:spark-cluster:deployer"
cannot get replicationcontrollers in project "spark-cluster"
```


看日志觉得是权限问题,从下面几点排查:

1. 创建app的时候用户是不是指定错了
2. 对应的用户是不是没有权限进行该操作








































