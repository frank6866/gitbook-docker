# 数据卷
数据卷是一个可以给一个或者多个容器使用的特殊目录，它可以绕过unionfs，数据卷的特点如下:  

* 数据卷可以在容器之间共享和重用
* 对数据卷的需改会立马生效
* 对数据卷的更新，在执行docker commit命令时，不会反映到镜像中来
* 数据卷不会因为容器被删除而被删除
* 如果挂载的是容器中已有的目录，容器中原来的文件会被隐藏，看到的是数据卷中的文件


# tutorial
## 只指定容器里面的挂载点
只指定容器里面的挂载点，如下(给容器里面的/data目录挂载数据卷):  

```
# docker run -d -v /data nginx
569addd3dda6d866e98f78425d1aa067eec94c84c08c3a496f8387d0fc723e3e
```

查看挂载的卷:  

```
# docker inspect -f "{{json .Mounts}}" 569add | python -mjson.tool
[
    {
        "Destination": "/data",
        "Driver": "local",
        "Mode": "",
        "Name": "ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52",
        "Propagation": "",
        "RW": true,
        "Source": "/var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52/_data"
    }
]
```

往宿主机上对应的目录上写一个文件，看是否同步到容器中了。  

```
# echo "data changed in host" > /var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52/_data/msg.txt
# docker exec -it 569add cat /data/msg.txt
data changed in host
```

## 指定宿主机的目录和容器的挂载点
格式

```
-v 宿主机目录:容器目录
```

注意:  

* 宿主机目录名不能包含下划线
* 容器里的目录如果不存在会被创建

将本地的hostDir目录挂载到容器的container_dir目录下

```
# mkdir hostDir
# echo "data in host" > hostDir/data.txt
# docker run -d -v /root/hostDir/:/container_dir nginx
c495650e6b4ea73ac00d8a636daa34339f5d3ee8c5d47d5a279c468904656117
```

在容器中修改文件也会修改宿主机上对应目录下的文件(比如修改容器中的/container_dir/data.txt，主机上的hostDir/data.txt也会通过修改；反之也是一样的。)

```
# docker exec -it c4956 /bin/bash
root@c495650e6b4e:/# cat /container_dir/data.txt
data in host
root@c495650e6b4e:/# echo "data changed in container" > /container_dir/data.txt
root@c495650e6b4e:/# exit

# cat hostDir/data.txt
data changed in container
#
```

## Dockefile
Dockerfile中VOLUME指令也可以指定容器中数据卷的挂载点，不同的是-v选项可以指定宿主机指定位置的目录挂载到容器中，而VOLUME指令办不到。  

Dockerfile

```
FROM centos
MAINTAINER frank6866
VOLUME /data
CMD ["sleep", "100"]
```

构建并运行:  

```
docker build -t volume-tutorial:v1.0 .

# docker run -d volume-tutorial:v1.0
8598455ba994280e9654060467972d19b500892dd23fd86b8380095fc17b546e

# docker inspect -f "{{json .Mounts}}" 859845 | python -mjson.tool
[
    {
        "Destination": "/data",
        "Driver": "local",
        "Mode": "",
        "Name": "9d15217f6f43131d6d70a0f2c7331318f1ebbe0521e05957de6efca48054ff6b",
        "Propagation": "",
        "RW": true,
        "Source": "/var/lib/docker/volumes/9d15217f6f43131d6d70a0f2c7331318f1ebbe0521e05957de6efca48054ff6b/_data"
    }
]
```

可以看到自动在宿主机上创建了目录。

## 删除数据卷
数据卷是被设计用来持久化数据的，它的生命周期独立于容器，Docker不会在容器被删除后自动删除数据卷，并且也不存在垃圾回收这样的机制来处理没有任何容器引用的数据卷。如果需要在删除容器的同时移除数据卷。可以在删除容器的时候使用 docker rm -v 这个命令。  

查看数据卷在本地的路径:  

```
# docker inspect -f "{{json .Mounts}}" 569addd3dda6 | python -mjson.tool

[
    {
        "Destination": "/data",
        "Driver": "local",
        "Mode": "",
        "Name": "ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52",
        "Propagation": "",
        "RW": true,
        "Source": "/var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52/_data"
    }
]
```

docker rm时使用-v选项，会删除对应的数据卷目录(**经测试，如果在docker run时将宿主机指定的目录挂载到容器中，docker rm -v并不会删除这个宿主机上的目录。**)

```
# file /var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52
/var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52: directory

# docker rm -f -v 569addd3dda6
569addd3dda6

# file /var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52
/var/lib/docker/volumes/ba05ab6acd049454db18ae73a3f9ab6cc70ea1210dae9b37a84e6100d4f19a52: cannot open (No such file or directory)
```

## 挂载网络文件系统
先尝试把nfs、glusterfs、cephfs挂载到本地，将本地的路径挂载到容器。

再尝试直接挂载docker容器到nfs、glusterfs、cephfs。


https://frank6866.gitbooks.io/linux/content/chapters/io/linux-io-nfs.html




# 参考
* https://yeasy.gitbooks.io/docker_practice/content/data_management/volume.html
* http://container-solutions.com/understanding-volumes-docker/
* https://docs.docker.com/engine/extend/legacy_plugins/#volume-plugins



