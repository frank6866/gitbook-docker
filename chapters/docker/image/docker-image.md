# 镜像
## unionfs
Docker的镜像用到unionfs(联合文件系统)。 

unionfs的tutorial,参考这篇文件: [https://frank6866.gitbooks.io/linux/content/chapters/io/linux-io-unionfs.html](https://frank6866.gitbooks.io/linux/content/chapters/io/linux-io-unionfs.html)。

## Docker镜像
Docker镜像代表了某个时间点文件系统的快照，Docker镜像包含了启动Docker容器所需要的文件系统结构及其内容。  

Docker镜像类似于虚拟机的快照，但是Docker镜像更轻量(镜像之间可以共享某些层)；虚拟机的镜像很重，镜像之间无法共享。  

Docker镜像采用**分层**的结构构建：最底层的是bootfs，之上的部分是rootfs。如下图:  

![Docker_Images_Layers](resources/Docker_Images_Layers.png)

* bootfs: 是Docker镜像最底层的引导文件系统，包括bootloader和kernel，类似于Linux中的引导文件系统。容器启动之后，为了节约内存，bootfs会被卸载掉。
* rootfs: rootfs位于bootfs之上，是Docker容器在启动时内部可见的文件系统，也就是Docker容器里面的/目录。rootfs通常包括一个操作系统运行所需要的文件，比如/proc、/dev、/bin、/etc等
* 在rootfs之上用户也可以自定义一些层

Docker通过unionfs将不同层的文件系统union起来,构成了Docker的分层镜像(镜像中的每一层都可以理解为一个文件系统,在用户的视角看到的就是最后union成一个的文件系统,)。

unionfs的实现技术除了aufs,还包括VFS、Btrfs、和DeviceMapper等。


## 镜像命名格式
registry/namespace/image-name:tag

比如:

gcr.io/google-samples/node-hello:1.0

* registry: 比如上面的gcr.io。如果registry部分没有,默认是docker.io
* namespace: 比如上面的google-samples。namespace可以没有
* name: 镜像名称,比如上面的node-hello,必须要有
* tag: 镜像tag,比如上面的1.0,如果没有,默认为latest


## 查看镜像的层级
### docker pull
docker pull的时候，是一层层pull的，比如，pull一个nginx镜像:  

```
# docker pull nginx
Using default tag: latest
Trying to pull repository docker.io/library/nginx ...
latest: Pulling from docker.io/library/nginx

6d827a3ef358: Already exists
f8f2e0556751: Pull complete
5c9972dca3fd: Pull complete
451b9524cb06: Pull complete
Digest: sha256:e6693c20186f837fc393390135d8a598a96a833917917789d63766cab6c59582
```

层级之间是可以共享的，比如上面6d827a3ef358层已经存在了就不会再下载了。  


### docker history
可以使用docker history命令查看镜像的层级，比如，查看nginx镜像的层级:  

```
# docker history nginx
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
5766334bdaa0        12 days ago         /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon    0 B
<missing>           12 days ago         /bin/sh -c #(nop)  EXPOSE 443/tcp 80/tcp        0 B
<missing>           12 days ago         /bin/sh -c ln -sf /dev/stdout /var/log/nginx/   0 B
<missing>           12 days ago         /bin/sh -c echo "deb http://nginx.org/package   59.1 MB
<missing>           12 days ago         /bin/sh -c set -e;  NGINX_GPGKEY=573BFD6B3D8F   4.901 kB
<missing>           12 days ago         /bin/sh -c #(nop)  ENV NGINX_VERSION=1.11.13-   0 B
<missing>           4 weeks ago         /bin/sh -c #(nop)  MAINTAINER NGINX Docker Ma   0 B
<missing>           4 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B
<missing>           4 weeks ago         /bin/sh -c #(nop) ADD file:4eedf861fb567fffb2   123.4 MB
```

其中每一行都代表了一个层级，上一个层级是在下面层级的基础上构建的。  













