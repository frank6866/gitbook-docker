# Dockerfile
docker commit命令会碰到无法重复、操作不透明等问题；我们可以使用Dockerfile来解决这些问题。  

Dockerfile是一个文本文件，里面包含了一条条指令，每一个指令都会建立一层。

## tutorial
新建一个目录，在目录里面新建一个名为Dockerfile的文件

```
# mkdir my_nginx
# cd my_nginx/
# touch Dockerfile
```

文件内容如下:  

```
FROM nginx
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```

构建镜像:  

```
# docker build -t nginx:v1.0 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM nginx
 ---> 5766334bdaa0
Step 2 : RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
 ---> Running in 22a0a5e977d5
 ---> fa233ee8a288
Removing intermediate container 22a0a5e977d5
Successfully built fa233ee8a288
```

查看构建的镜像:  

```
# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
nginx               v1.0                fa233ee8a288        About a minute ago   182.5 MB
docker.io/nginx     latest              5766334bdaa0        12 days ago          182.5 MB
```



用构建的镜像启动容器，

```
# docker run -d -P nginx:v1.0
0b52a7943343696f2ebabd94c3f4d94f08bb8b2a01f34477b1703a8ace273c6f
# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                           NAMES
0b52a7943343        nginx:v1.0          "nginx -g 'daemon off"   5 seconds ago       Up 4 seconds        0.0.0.0:32769->80/tcp, 0.0.0.0:32768->443/tcp   modest_mahavira
# curl http://0.0.0.0:32769
<h1>Hello, Docker!</h1>
```


# TODO
从centos镜像，制作一个nginx的镜像，包括所有的指令。



# 语法

一个示例的Dockerfile文件

## FROM
FROM指令表示要制作的镜像金鱼哪个镜像，FROM指令必须是Dockerfile的第一个指令。如果FROM指令设置的镜像在本地不存在，会自动从Docker Hub上下载。

### 格式

```
FROM <image>[:<tag>]
```

### demo
Dockerfile 

```
FROM centos
```

Build:  

```
# docker build -t nginx:v1.1 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
Trying to pull repository docker.io/library/centos ...
latest: Pulling from docker.io/library/centos

93857f76ae30: Pull complete
Digest: sha256:4eda692c08e0a065ae91d74e82fff4af3da307b4341ad61fa61771cc4659af60
 ---> a8493f5f50ff
Successfully built a8493f5f50ff
```

如果FROM中指定的镜像在本地不存在，会下载。



## MAINTAINER
MAINTAINER指令用于给待制作的镜像设置作者信息。  

### 格式

```
MAINTAINER <name>
```

### demo
Dockerfile 

```
FROM centos
MAINTAINER frank6866
```

Build:  

```
# docker build -t nginx:v1.2 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
 ---> a8493f5f50ff
Step 2 : MAINTAINER frank6866
 ---> Running in 200dbc9fe45c
 ---> 76ebd2865f7a
Removing intermediate container 200dbc9fe45c
Successfully built 76ebd2865f7a

# docker history nginx:v1.2
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
76ebd2865f7a        47 seconds ago      /bin/sh -c #(nop)  MAINTAINER frank6866         0 B
a8493f5f50ff        12 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B
<missing>           12 days ago         /bin/sh -c #(nop)  LABEL name=CentOS Base Ima   0 B
<missing>           12 days ago         /bin/sh -c #(nop) ADD file:807143da05d70138e5   192.5 MB
```

可以发现，MAINTAINER给镜像加了一层，镜像ID从a8493f5f50ff变为76ebd2865f7a。


## RUN
RUN指令会在一个新的容器中执行命令，然后把执行后的更改提交到镜像。RUN指令中定义的命令会顺序执行并提交。

RUN指令有两种格式

### 格式1  
```
RUN <command>
```

格式1将会调用/bin/sh -c <command>命令

### 格式2

```
RUN ["executable", "param1", "param2"]
```

格式2将会调用exec执行，以避免有些时候shell方式执行时的传递参数问题；并且有些基础镜像可能不包含/bin/sh。  

> 注意: 格式2数组里面的元素需要使用双引号。  


### demo
Dockerfile 

```
FROM centos
MAINTAINER frank6866
RUN echo 'run instruction' > run_instruction.txt
RUN yum -y install epel-release
RUN yum -y install nginx
```

Build:  

```
# docker build -t nginx:v1.3 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
 ---> a8493f5f50ff
Step 2 : MAINTAINER frank6866
 ---> Using cache
 ---> 76ebd2865f7a
Step 3 : RUN echo 'run instruction' > run_instruction.txt
 ---> Using cache
 ---> 6ffe098adaef
Step 4 : RUN yum -y install epel-release
 ---> Running in e5d8575d6caf
Loaded plugins: fastestmirror, ovl
Determining fastest mirrors
 * base: repo.virtualhosting.hk
 * extras: mirrors.btte.net
 * updates: mirrors.sohu.com
Resolving Dependencies
--> Running transaction check
---> Package epel-release.noarch 0:7-9 will be installed
--> Finished Dependency Resolution
......
......
Complete!
 ---> 9e0b4877ce31
Removing intermediate container 2bdcc9e12f12
Successfully built 9e0b4877ce31
```


### 优化
上面的Dockerfile有两个问题:  

1. 每一个命令都会构建一层镜像，会导致镜像层级过多
2. 构建完镜像后没有进行清理工作，导致镜像的体积过大

如下，是上面的镜像的信息，可以发现镜像相比于base镜像centos，多了4层。  

```
# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               v1.3                9e0b4877ce31        3 minutes ago       380.1 MB
...
docker.io/centos    latest              a8493f5f50ff        12 days ago         192.5 MB

# docker history 9e0b4877ce31
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
9e0b4877ce31        5 minutes ago       /bin/sh -c yum -y install nginx                 101 MB
8b895a37d487        6 minutes ago       /bin/sh -c yum -y install epel-release          86.57 MB
6ffe098adaef        14 minutes ago      /bin/sh -c echo 'run instruction' > run_instr   16 B
76ebd2865f7a        27 minutes ago      /bin/sh -c #(nop)  MAINTAINER frank6866         0 B
a8493f5f50ff        12 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B
<missing>           12 days ago         /bin/sh -c #(nop)  LABEL name=CentOS Base Ima   0 B
<missing>           12 days ago         /bin/sh -c #(nop) ADD file:807143da05d70138e5   192.5 MB

```


使用下面的Dockerfile构建:  

```
FROM centos
MAINTAINER frank6866
RUN echo 'run instruction' > run_instruction.txt \
    && yum -y install epel-release \
    && yum -y install nginx \
    && yum clean all
```

```
# docker build -t nginx:v1.4 .
[root@nl-cloud-dyc-k8s-1 my_nginx]# docker build -t nginx:v1.4 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
 ---> a8493f5f50ff
Step 2 : MAINTAINER frank6866
 ---> Using cache
 ---> 76ebd2865f7a
Step 3 : RUN echo 'run instruction' > run_instruction.txt     && yum -y install epel-release     && yum -y install nginx     && yum clean all
 ---> Running in 7f88240937b4
Loaded plugins: fastestmirror, ovl
Determining fastest mirrors
 * base: ftp.cuhk.edu.hk
 * extras: mirrors.btte.net
 * updates: mirrors.sohu.com
Resolving Dependencies
--> Running transaction check
---> Package epel-release.noarch 0:7-9 will be installed
--> Finished Dependency Resolution
...
 ---> bb54cc35248a
Removing intermediate container 7f88240937b4
Successfully built bb54cc35248a


# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
nginx               v1.4                bb54cc35248a        About a minute ago   261.4 MB
nginx               v1.3                9e0b4877ce31        15 minutes ago       380.1 MB
docker.io/centos    latest              a8493f5f50ff        12 days ago          192.5 MB
......

# docker history bb54cc35248a
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
bb54cc35248a        2 minutes ago       /bin/sh -c echo 'run instruction' > run_instr   68.91 MB
76ebd2865f7a        38 minutes ago      /bin/sh -c #(nop)  MAINTAINER frank6866         0 B
a8493f5f50ff        12 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B
<missing>           12 days ago         /bin/sh -c #(nop)  LABEL name=CentOS Base Ima   0 B
<missing>           12 days ago         /bin/sh -c #(nop) ADD file:807143da05d70138e5   192.5 MB
```

发现经过优化后的镜像nginx:v1.4大小比没有优化的nginx:v1.3小了近120M，层级少了两层。


## CMD
CMD指令会在启动容器时被执行，在Dockerfile中，只有一个CMD有效；如果指定了多个CMD指令，则只有最后一个CMD指令有效。  

### 格式
```
CMD ["executable", "param1", "param2"]    #将会调用exec执行，首选方式
CMD ["param1", "param2"]        #当使用ENTRYPOINT指令时，为该指令传递默认参数
CMD <command> [ <param1>|<param2> ]        #将会调用/bin/sh -c执行
```

### demo
Dockerfile 

```
FROM centos
MAINTAINER frank6866
RUN echo 'run instruction' > run_instruction.txt \
    && yum -y install epel-release \
    && yum -y install nginx \
    && yum clean all
CMD ["nginx", "-g", "daemon off;"]
```

主要nginx的启动命令是**nginx -g "daemon off;"**而不是nginx -g daemon off;

Build:  

```
# docker build -t nginx:v1.5 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
 ---> a8493f5f50ff
Step 2 : MAINTAINER frank6866
 ---> Using cache
 ---> 76ebd2865f7a
Step 3 : RUN echo 'run instruction' > run_instruction.txt     && yum -y install epel-release     && yum -y install nginx     && yum clean all
 ---> Using cache
 ---> bb54cc35248a
Step 4 : CMD nginx -g daemon off;
 ---> Running in cb2156f2ea32
 ---> 21c33e737727
Removing intermediate container cb2156f2ea32
Successfully built 21c33e737727


# docker run -d nginx:v1.5
5a0543e1057c796a437749b8331c4040f73c27d38eb9e5759f0e59c95bacc127


# docker ps -f "id=5a0543e1057c"
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
5a0543e1057c        nginx:v1.5          "nginx -g 'daemon off"   49 seconds ago      Up 48 seconds                           awesome_hoover

#如下，可以看见nginx进程已经启动了

# docker exec -it 5a0543e1057c /bin/bash
[root@5a0543e1057c /]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 17:28 ?        00:00:00 nginx: master process nginx -g daemon off;
nginx        5     1  0 17:28 ?        00:00:00 nginx: worker process
nginx        6     1  0 17:28 ?        00:00:00 nginx: worker process
```

**注意: CMD中指定的命令可以被覆盖，比如，启动容器的时候执行/bin/bash命令，而不执行CMD中的nginx -g "daemon off;"命令:**    

```
# docker run -it --rm nginx:v1.5 /bin/bash
[root@9fc55d8f2ff7 /]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  1 17:39 ?        00:00:00 /bin/bash
root        13     1  0 17:39 ?        00:00:00 ps -ef
[root@9fc55d8f2ff7 /]# exit
#
```




## ENTRYPOINT
ENTRYPOINT指令中指定的命令会在镜像运行时执行，在Dockerfile中最多只有一个有效；如果使用了多个ENTRYPOINT指令，则只有最后一个指令有效。

RUN、CMD和ENTRYPOINT的关系:  

* RUN、CMD和ENTRYPOINT指令都会给镜像添加层级
* RUN指令可以有多个，CMD和ENTRYPOINT最多只有一个有效
* RUN和CMD都是执行命令，他们的差异在于RUN中定义的命令(比如yum -y install nginx)会在执行docker build命令创建镜像时执行；而CMD中定义的命令(比如nginx -g "daemon off;")会在执行docker run命令运行镜像时执行
* 当只用ENTRYPOING时，容器启动时会执行ENTRYPOINT中的命令；当只用CMD时，容器启动时会执行CMD中的命令；当两个同时存在时(CMD如果不在Dockerfile中，在docker run的命令中，也算存在)，容器启动时会执行<ENTRYPOING> "<CMD"命令，CMD此时的作用相当于ENTRYPOINT命令中的选项。  
* 将命令的固定部分写在ENTRYPOINT中，选项和参数放在CMD中。比如想用容器启用Pyhton的SimplHTTPServer，但是端口用户可以指定，比如下面的demo1。
* 如果在启动容器时，指定一个命令，默认会覆盖掉CMD命令，不需要额外的选项；如果想覆盖ENTRYPOINT，需要使用--entrypoint选项，但是一般不用



### 格式

```
ENTRYPOINT ["executable", "param1", "param2"]        #将会调用exec执行，首选方式
ENTRYPOINT command param1 param2             #将会调用/bin/sh -c执行

  解释：ENTRYPOINT指令中指定的命令会在镜像运行时执行，在Dockerfile中只能存在一个，如果使用了多个ENTRYPOINT指令，则只有最后一个指令有效。ENTRYPOINT指令中指定的命令(exec执行的方式)可以通过docker run来传递参数，例如docker run <images> -l启动的容器将会把-l参数传递给ENTRYPOINT指令定义的命令并会覆盖CMD指令中定义的默认参数(如果有的话)，但不会覆盖该指令定义的参数，例如ENTRYPOINT ["ls","-a"]，CMD ["/etc"],当通过docker run <image>启动容器时该容器会运行ls -a /etc命令，当使用docker run <image> -l启动时该容器会运行ls -a -l命令，-l参数会覆盖CMD指令中定义的/etc参数。
  注意：①当使用ENTRYPOINT指令时生成的镜像运行时只会执行该指令指定的命令。
      ②当出现ENTRYPOINT指令时CMD指令只可能(当ENTRYPOINT指令使用exec方式执行时)被当做ENTRYPOINT指令的参数使用，其他情况则会被忽略。
```


### demo1:让镜像变成命令一样使用
Dockerfile 

```
FROM centos
ENTRYPOINT ["python", "-m", "SimpleHTTPServer"]     
```

Build:  

```
# docker build -t python:v1.0 .
```

Run:  

不加CMD启动

```
# docker run -d python:v1.0
2d4261cb9a037576b918a5fc6b90590ab72bdf091454df6640888826c338f858

# docker exec -it 2d4261 /bin/bash
[root@2d4261cb9a03 /]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 02:35 ?        00:00:00 python -m SimpleHTTPServer
root         5     0  1 02:35 ?        00:00:00 /bin/bash
root        16     5  0 02:36 ?        00:00:00 ps -ef
```

在CMD中传入端口启动:  

```
# docker run -d python:v1.0 8081
79f758aba8d07928ca39576d056d1c45f6ebae208d3c3fe7d94ec14e00b2541d

# docker exec -it 79f758 /bin/bash
[root@79f758aba8d0 /]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 02:38 ?        00:00:00 python -m SimpleHTTPServer 8081
root         5     0  1 02:38 ?        00:00:00 /bin/bash
root        16     5  0 02:38 ?        00:00:00 ps -ef
```




## EXPOSE
EXPOSE指令表示基于该镜像运行的容器会监听哪些端口。

EXPOSE指令仅仅是声明容器打算使用什么端口，并不会在容器启动时开启容器里面的端口，更不会将宿主机的端口映射到容器中的端口:  

* 在容器启动时开启容器里面的端口是用户进程(或者说是通过ENTRYPOINT或CMD来实现)的工作
* 将宿主机的端口映射到容器中的端口需要在容器启动时使用-p或者-P选项

使用EXPOSE的好处:  

* 方便镜像的使用者知道容器监听的是哪几个端口
* 在使用docker run -P时，会自动随机映射EXPOSE的端口



### 格式

```
EXPOSE <port> [ ...]
```

EXPOSE 443/tcp 80/tcps

### demo
Dockerfile 

```
FROM centos
MAINTAINER frank6866
RUN echo 'run instruction' > run_instruction.txt \
    && yum -y install epel-release \
    && yum -y install nginx \
    && yum clean all
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80 443
```

Build:  

```
# docker build -t nginx:v1.6 .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos
 ---> a8493f5f50ff
Step 2 : MAINTAINER frank6866
 ---> Using cache
 ---> 76ebd2865f7a
Step 3 : RUN echo 'run instruction' > run_instruction.txt     && yum -y install epel-release     && yum -y install nginx     && yum clean all
 ---> Using cache
 ---> bb54cc35248a
Step 4 : CMD nginx -g daemon off;
 ---> Using cache
 ---> 21c33e737727
Step 5 : EXPOSE 80 443
 ---> Running in 2983ffa3f2f4
 ---> a33fce46db43
Removing intermediate container 2983ffa3f2f4
Successfully built a33fce46db43
```

Run:  

```
# docker run -d nginx:v1.6
a995d5584124e805464f1cea2e4f7178c13fd533dbabaa71f39357452c998e7b

# docker ps -f "id=a995d"
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
a995d5584124        nginx:v1.6          "nginx -g 'daemon off"   30 seconds ago      Up 29 seconds       80/tcp, 443/tcp     compassionate_panini

# docker run -dP nginx:v1.6
e9459e68d9c61672b5ef1d9eddd8d23ff2a015af83c04b50465fa11e31442e36
# docker ps -f "id=e9459"
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                           NAMES
e9459e68d9c6        nginx:v1.6          "nginx -g 'daemon off"   10 seconds ago      Up 9 seconds        0.0.0.0:32771->80/tcp, 0.0.0.0:32770->443/tcp   kickass_morse
# curl 0.0.0.0:32771
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
......
```

发现，在docker ps命令的输出中:  

* 如果启动容器时，没有使用-P或者-p选项，docker ps命令输出中的PORTS字段为Dockerfile中的EXPOSE指定的端口
* 如果启动容器时，使用了-P或者-p选项，docker ps命令输出中的PORTS字段为宿主机端口到容器端口的映射

> 到这里，一个最简单的nginx容器就可以使用了。下面会介绍一些其他可能用到的指令。  


## ENV
ENV指令用于设置环境变量，可以在RUN指令中使用ENV定义的环境变量；如果需要在运行时更改这些环境变量，可以在docker run是通过-e <key>=<value>来修改。

### 格式

```
ENV <key> <value>
```

### demo
Dockerfile 

```

```

docker build


## COPY
将一个文件拷贝到容器中

### 格式

```
COPY <src> <dest>
```

### demo
Dockerfile 

```

```

docker build



## ADD
ADD指令与COPY指令相似，也可以用于拷贝文件，但是ADD指令会使镜像缓存失效，让镜像构建变慢；不过ADD有一些高级的功能，比如支持url和自动加压缩:  

* 如果ADD指令中的<src>是一个url，会自动下载这个url
* 如果ADD指令中的<src>是一个压缩包，会调用tar -x命令解压缩

在Dockerfile的最佳实践中，建议只要涉及到文件拷贝就使用COPY，遇到需要解压缩时，才使用ADD。

### 格式

```
ADD <src> <dest>
```


### demo
Dockerfile 

```

```

docker build



## VOLUME

### 格式

```
  语法：VOLUME ["samepath"]
  解释：VOLUME指令用来设置一个挂载点，可以用来让其他容器挂载以实现数据共享或对容器数据的备份、恢复或迁移，具体用法请参考其他文章。
```

### demo
Dockerfile 

```

```

docker build



## USER
USER指令用于设置用户或uid来运行生成的镜像和执行RUN指令。

### 格式

```
USER [username|uid]
```


### demo
Dockerfile 

```

```

docker build



## WORKDIR
### 格式

```
  语法：WORKDIR /path/to/workdir
  解释：WORKDIR指令用于设置Dockerfile中的RUN、CMD和ENTRYPOINT指令执行命令的工作目录(默认为/目录)，该指令在Dockerfile文件中可以出现多次，如果使用相对路径则为相对于WORKDIR上一次的值，例如WORKDIR /data，WORKDIR logs，RUN pwd最终输出的当前目录是/data/logs
```

### demo
Dockerfile 

```

```

docker build


## ONBUILD
### 格式

```

```

### demo
Dockerfile 

```

```

docker build



## 
### 格式

```

```

### demo
Dockerfile 

```

```

docker build


# 参考
* https://docs.docker.com/engine/reference/builder
* https://yeasy.gitbooks.io/docker_practice/content/image/build.html
* https://hujb2000.gitbooks.io/docker-flow-evolution/content/cn/basis/dockerfiledetail.html
* https://hujb2000.gitbooks.io/docker-flow-evolution/content/cn/basis/dockerfiledetail.html





