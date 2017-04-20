# 命令

查看docker的所有命令

```
# docker --help
Usage: docker [OPTIONS] COMMAND [arg...]
       docker [ --help | -v | --version ]

A self-sufficient runtime for containers.

Options:

  --config=~/.docker              Location of client config files
  -D, --debug                     Enable debug mode
  -H, --host=[]                   Daemon socket(s) to connect to
  -h, --help                      Print usage
  -l, --log-level=info            Set the logging level
  --tls                           Use TLS; implied by --tlsverify
  --tlscacert=~/.docker/ca.pem    Trust certs signed only by this CA
  --tlscert=~/.docker/cert.pem    Path to TLS certificate file
  --tlskey=~/.docker/key.pem      Path to TLS key file
  --tlsverify                     Use TLS and verify the remote
  -v, --version                   Print version information and quit

Commands:
    attach    Attach to a running container
    build     Build an image from a Dockerfile
    commit    Create a new image from a container's changes
    cp        Copy files/folders between a container and the local filesystem
    create    Create a new container
    diff      Inspect changes on a container's filesystem
    events    Get real time events from the server
    exec      Run a command in a running container
    export    Export a container's filesystem as a tar archive
    history   Show the history of an image
    images    List images
    import    Import the contents from a tarball to create a filesystem image
    info      Display system-wide information
    inspect   Return low-level information on a container, image or task
    kill      Kill one or more running containers
    load      Load an image from a tar archive or STDIN
    login     Log in to a Docker registry.
    logout    Log out from a Docker registry.
    logs      Fetch the logs of a container
    network   Manage Docker networks
    node      Manage Docker Swarm nodes
    pause     Pause all processes within one or more containers
    port      List port mappings or a specific mapping for the container
    ps        List containers
    pull      Pull an image or a repository from a registry
    push      Push an image or a repository to a registry
    rename    Rename a container
    restart   Restart a container
    rm        Remove one or more containers
    rmi       Remove one or more images
    run       Run a command in a new container
    save      Save one or more images to a tar archive (streamed to STDOUT by default)
    search    Search the Docker Hub for images
    service   Manage Docker services
    start     Start one or more stopped containers
    stats     Display a live stream of container(s) resource usage statistics
    stop      Stop one or more running containers
    swarm     Manage Docker Swarm
    tag       Tag an image into a repository
    top       Display the running processes of a container
    unpause   Unpause all processes within one or more containers
    update    Update configuration of one or more containers
    version   Show the Docker version information
    volume    Manage Docker volumes
    wait      Block until a container stops, then print its exit code

Run 'docker COMMAND --help' for more information on a command.
```

# docker info(环境信息)
```
# docker info
Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 0
Server Version: 1.12.6
Storage Driver: devicemapper
 Pool Name: docker-253:1-25166849-pool
 Pool Blocksize: 65.54 kB
 Base Device Size: 10.74 GB
 Backing Filesystem: xfs
 Data file: /dev/loop0
 Metadata file: /dev/loop1
 Data Space Used: 11.8 MB
 Data Space Total: 107.4 GB
 Data Space Available: 5.58 GB
 Metadata Space Used: 581.6 kB
 Metadata Space Total: 2.147 GB
 Metadata Space Available: 2.147 GB
 Thin Pool Minimum Free Space: 10.74 GB
 Udev Sync Supported: true
 Deferred Removal Enabled: false
 Deferred Deletion Enabled: false
 Deferred Deleted Device Count: 0
 Data loop file: /var/lib/docker/devicemapper/devicemapper/data
 WARNING: Usage of loopback devices is strongly discouraged for production use. Use `--storage-opt dm.thinpooldev` to specify a custom block storage device.
 Metadata loop file: /var/lib/docker/devicemapper/devicemapper/metadata
 Library Version: 1.02.135-RHEL7 (2016-11-16)
Logging Driver: journald
Cgroup Driver: systemd
Plugins:
 Volume: local
 Network: bridge overlay null host
Swarm: inactive
Runtimes: docker-runc runc
Default Runtime: docker-runc
Security Options: seccomp selinux
Kernel Version: 3.10.0-229.el7.x86_64
Operating System: CentOS Linux 7 (Core)
OSType: linux
Architecture: x86_64
Number of Docker Hooks: 2
CPUs: 2
Total Memory: 3.86 GiB
Name: nl-cloud-dyc-k8s-1
ID: TNN5:OMTU:YIY5:3HWV:TSMJ:IMKH:UKBG:ZIIY:UIUX:L2ES:4MUM:3EOA
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
WARNING: bridge-nf-call-iptables is disabled
WARNING: bridge-nf-call-ip6tables is disabled
Insecure Registries:
 127.0.0.0/8
Registries: docker.io (secure)
```

可以看到的信息包括:  

* Containers: 容器信息概要，Running表示正在运行的容器的个数, Paused表示处于Paused状态的容器个数，Stopped表示处于Stopped状态的容器个数
* Images: 镜像的个数
* Server Version: docker服务的版本，这里为1.12.6
* Storage Driver: 后端使用的存储驱动，这里是devicemapper，还可以是aufs和lvm2




# 镜像管理
## docker search(搜索镜像)
### usage
```
# docker help search

Usage:	docker search [OPTIONS] TERM

Search the Docker Hub for images

Options:
  -f, --filter value   Filter output based on conditions provided (default [])
      --help           Print usage
      --limit int      Max number of search results (default 25)
      --no-index       Don't truncate output
      --no-trunc       Don't truncate output
```

### demo
搜索名为nginx的镜像

```
# docker search nginx
INDEX       NAME                                DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
docker.io   docker.io/nginx                     Official build of Nginx.                        5756      [OK]
docker.io   docker.io/jwilder/nginx-proxy       Automated Nginx reverse proxy for docker c...   997                  [OK]
docker.io   docker.io/richarvey/nginx-php-fpm   Container running Nginx + PHP-FPM capable ...   365                  [OK]
docker.io   docker.io/million12/nginx-php       Nginx + PHP-FPM 5.5, 5.6, 7.0 (NG), CentOS...   77                   [OK]
docker.io   docker.io/webdevops/php-nginx       Nginx with PHP-FPM                              77                   [OK]
......
```      

* INDEX表示Registry
* NAME表示镜像的名称


## docker pull(拉取镜像)
### usage
```
# docker help pull

Usage:	docker pull [OPTIONS] NAME[:TAG|@DIGEST]

Pull an image or a repository from a registry

Options:
  -a, --all-tags                Download all tagged images in the repository
      --disable-content-trust   Skip image verification (default true)
      --help                    Print usage
```      


### demo
pull名为busybox的镜像

```
# docker pull busybox
Using default tag: latest
Trying to pull repository docker.io/library/busybox ...
latest: Pulling from docker.io/library/busybox
7520415ce762: Pull complete
Digest: sha256:32f093055929dbc23dec4d03e09dfe971f5973a9ca5cf059cbfb644c206aa83f
```

* 在运行一个容器的时候，需要指定镜像的名称和tag，如果不指定tag，会使用默认的tag值(即latest)；但如果没有名为latest的tag，会报错，提示找不到容器。  
* 没有查询一个镜像所有的tag的接口或命令(TODO)，可以先去registry中查询一下可用的tag，再使用docker pull拉下来



## docker images(列出镜像) 
### usage
```
# docker images -h
Flag shorthand -h has been deprecated, please use --help

Usage:	docker images [OPTIONS] [REPOSITORY[:TAG]]

List images

Options:
  -a, --all             Show all images (default hides intermediate images)
      --digests         Show digests
  -f, --filter value    Filter output based on conditions provided (default [])
      --format string   Pretty-print images using a Go template
      --help            Print usage
      --no-trunc        Don't truncate output
  -q, --quiet           Only show numeric IDs
```


### demo
```
# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/nginx     latest              5766334bdaa0        5 days ago          182.5 MB
docker.io/busybox   latest              00f017a8c2a6        4 weeks ago         1.11 MB
```



## docker rmi(删除镜像)
### usage
```
# docker rmi -h
Flag shorthand -h has been deprecated, please use --help

Usage:	docker rmi [OPTIONS] IMAGE [IMAGE...]

Remove one or more images

Options:
  -f, --force      Force removal of the image
      --help       Print usage
      --no-prune   Do not delete untagged parents
```      

### demo
删除tag为latest的nginx镜像:  

```
# docker rmi docker.io/nginx:latest
```

删除所有镜像(清空镜像)，**docker images -q** 命令会打印出所有的镜像id

```
# docker rmi $(docker images -q)
```

在清空所有镜像的时候，最好使用-f选项，因为镜像间可能有依赖导致删除失败.

```
# docker rmi -f $(docker images -q)
```


## docker commit(用容器制作镜像)
### usage
```
# docker commit --help

Usage:	docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]

Create a new image from a container's changes

Options:
  -a, --author string    Author (e.g., "John Hannibal Smith <hannibal@a-team.com>")
  -c, --change value     Apply Dockerfile instruction to the created image (default [])
      --help             Print usage
  -m, --message string   Commit message
  -p, --pause            Pause container during commit (default true)
```

### demo
用nginx镜像启动一个容器,容器id为4281fb8cb2aa8e648eaa3a5145b37e74d6397f89df238248a98e1ed4ff8ced63,如下:

```
# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/mysql     latest              d5127813070b        7 days ago          407.1 MB
docker.io/nginx     latest              5766334bdaa0        12 days ago         182.5 MB
docker.io/busybox   latest              00f017a8c2a6        5 weeks ago         1.11 MB

# docker run -d nginx
4281fb8cb2aa8e648eaa3a5145b37e74d6397f89df238248a98e1ed4ff8ced63
```

使用exec进入容器,在容器内部创建一个文件:

```
# docker exec -it 4281fb /bin/bash
root@4281fb8cb2aa:/# echo changed > added_file.txt
root@4281fb8cb2aa:/# exit
exit
```

使用运行中的容器4281fb8cb2aa8e648eaa3a5145b37e74d6397f89df238248a98e1ed4ff8ced63创建一个镜像,镜像id为f48aed293fde

```
# docker commit 4281fb
sha256:f48aed293fde39664d56aab9807c85f9fb5eb31b4f3b2907356cd2d3a914200a

# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              f48aed293fde        7 seconds ago       182.5 MB
docker.io/mysql     latest              d5127813070b        7 days ago          407.1 MB
docker.io/nginx     latest              5766334bdaa0        12 days ago         182.5 MB
docker.io/busybox   latest              00f017a8c2a6        5 weeks ago         1.11 MB
```

以刚创建的镜像启动一个容器,发现添加的文件在容器里面了。

```
# docker run -it f48aed293fde /bin/bash
root@81e1f15275df:/# cat added_file.txt
changed
```


## docker push(推送镜像)
### usage

### demo

## docker build(打包镜像)
### usage
```
# docker build --help

Usage:	docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

Options:
      --build-arg value         Set build-time variables (default [])
      --cgroup-parent string    Optional parent cgroup for the container
      --cpu-period int          Limit the CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int           Limit the CPU CFS (Completely Fair Scheduler) quota
  -c, --cpu-shares int          CPU shares (relative weight)
      --cpuset-cpus string      CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string      MEMs in which to allow execution (0-3, 0,1)
      --disable-content-trust   Skip image verification (default true)
  -f, --file string             Name of the Dockerfile (Default is 'PATH/Dockerfile')
      --force-rm                Always remove intermediate containers
      --help                    Print usage
      --isolation string        Container isolation technology
      --label value             Set metadata for an image (default [])
  -m, --memory string           Memory limit
      --memory-swap string      Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --no-cache                Do not use cache when building the image
      --pull                    Always attempt to pull a newer version of the image
  -q, --quiet                   Suppress the build output and print image ID on success
      --rm                      Remove intermediate containers after a successful build (default true)
      --shm-size string         Size of /dev/shm, default value is 64MB
  -t, --tag value               Name and optionally a tag in the 'name:tag' format (default [])
      --ulimit value            Ulimit options (default [])
  -v, --volume value            Set build-time bind mounts (default [])
```

### demo
```

```

## docker login(登录registry)
### usage
```

```


### demo
```

```

## docker logout(退出registry)
### usage
```

```

### demo
```

```


# 容器管理
## docker create(创建容器)
一般使用docker run(包含create和start)

## docker run(启动容器)
### usage
```
# docker run --help

Usage:	docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Run a command in a new container

Options:
      --add-host value              Add a custom host-to-IP mapping (host:ip) (default [])
  -a, --attach value                Attach to STDIN, STDOUT or STDERR (default [])
      --blkio-weight value          Block IO (relative weight), between 10 and 1000
      --blkio-weight-device value   Block IO weight (relative device weight) (default [])
      --cap-add value               Add Linux capabilities (default [])
      --cap-drop value              Drop Linux capabilities (default [])
      --cgroup-parent string        Optional parent cgroup for the container
      --cidfile string              Write the container ID to the file
      --cpu-percent int             CPU percent (Windows only)
      --cpu-period int              Limit CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int               Limit CPU CFS (Completely Fair Scheduler) quota
  -c, --cpu-shares int              CPU shares (relative weight)
      --cpuset-cpus string          CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string          MEMs in which to allow execution (0-3, 0,1)
  -d, --detach                      Run container in background and print container ID
      --detach-keys string          Override the key sequence for detaching a container
      --device value                Add a host device to the container (default [])
      --device-read-bps value       Limit read rate (bytes per second) from a device (default [])
      --device-read-iops value      Limit read rate (IO per second) from a device (default [])
      --device-write-bps value      Limit write rate (bytes per second) to a device (default [])
      --device-write-iops value     Limit write rate (IO per second) to a device (default [])
      --disable-content-trust       Skip image verification (default true)
      --dns value                   Set custom DNS servers (default [])
      --dns-opt value               Set DNS options (default [])
      --dns-search value            Set custom DNS search domains (default [])
      --entrypoint string           Overwrite the default ENTRYPOINT of the image
  -e, --env value                   Set environment variables (default [])
      --env-file value              Read in a file of environment variables (default [])
      --expose value                Expose a port or a range of ports (default [])
      --group-add value             Add additional groups to join (default [])
      --health-cmd string           Command to run to check health
      --health-interval duration    Time between running the check (default 0s)
      --health-retries int          Consecutive failures needed to report unhealthy
      --health-timeout duration     Maximum time to allow one check to run (default 0s)
      --help                        Print usage
  -h, --hostname string             Container host name
  -i, --interactive                 Keep STDIN open even if not attached
      --io-maxbandwidth string      Maximum IO bandwidth limit for the system drive (Windows only)
      --io-maxiops uint             Maximum IOps limit for the system drive (Windows only)
      --ip string                   Container IPv4 address (e.g. 172.30.100.104)
      --ip6 string                  Container IPv6 address (e.g. 2001:db8::33)
      --ipc string                  IPC namespace to use
      --isolation string            Container isolation technology
      --kernel-memory string        Kernel memory limit
  -l, --label value                 Set meta data on a container (default [])
      --label-file value            Read in a line delimited file of labels (default [])
      --link value                  Add link to another container (default [])
      --link-local-ip value         Container IPv4/IPv6 link-local addresses (default [])
      --log-driver string           Logging driver for the container
      --log-opt value               Log driver options (default [])
      --mac-address string          Container MAC address (e.g. 92:d0:c6:0a:29:33)
  -m, --memory string               Memory limit
      --memory-reservation string   Memory soft limit
      --memory-swap string          Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --memory-swappiness int       Tune container memory swappiness (0 to 100) (default -1)
      --name string                 Assign a name to the container
      --network string              Connect a container to a network (default "default")
      --network-alias value         Add network-scoped alias for the container (default [])
      --no-healthcheck              Disable any container-specified HEALTHCHECK
      --oom-kill-disable            Disable OOM Killer
      --oom-score-adj int           Tune host's OOM preferences (-1000 to 1000)
      --pid string                  PID namespace to use
      --pids-limit int              Tune container pids limit (set -1 for unlimited)
      --privileged                  Give extended privileges to this container
  -p, --publish value               Publish a container's port(s) to the host (default [])
  -P, --publish-all                 Publish all exposed ports to random ports
      --read-only                   Mount the container's root filesystem as read only
      --restart string              Restart policy to apply when a container exits (default "no")
      --rm                          Automatically remove the container when it exits
      --runtime string              Runtime to use for this container
      --security-opt value          Security Options (default [])
      --shm-size string             Size of /dev/shm, default value is 64MB
      --sig-proxy                   Proxy received signals to the process (default true)
      --stop-signal string          Signal to stop a container, SIGTERM by default (default "SIGTERM")
      --storage-opt value           Storage driver options for the container (default [])
      --sysctl value                Sysctl options (default map[])
      --tmpfs value                 Mount a tmpfs directory (default [])
  -t, --tty                         Allocate a pseudo-TTY
      --ulimit value                Ulimit options (default [])
  -u, --user string                 Username or UID (format: <name|uid>[:<group|gid>])
      --userns string               User namespace to use
      --uts string                  UTS namespace to use
  -v, --volume value                Bind mount a volume (default [])
      --volume-driver string        Optional volume driver for the container
      --volumes-from value          Mount volumes from the specified container(s) (default [])
  -w, --workdir string              Working directory inside the container
```

### demo
使用nginx镜像启动容器(不加选项):  

```
# docker run docker.io/nginx:latest
```

启动的这个容器会占用标准输入，可以使用Ctrl+C退出容器。


建议在后台运行容器(使用-d选项)，在启动容器的时候可以给容器指定一个名称(比如frontend):  

```
# docker run -d --name frontend docker.io/nginx:latest
```

容器默认使用其id作为主机名，如果想自定义主机名，可以使用-h选项(或者--hostname)指定容器的主机名，比如，启动一个容器设置主机名为tutorial-01:  

```
# docker run -d --name backend -h tutorial-01 docker.io/nginx:latest
```

将镜像定好的端口随机映射到宿主机的端口上(使用-P选项):  

```
# docker run -d -P docker.io/nginx:latest
```

将容器的80端口映射到宿主机的8001端口，容器的443端口映射到主机的8082端口(使用-p选项):  

```
# docker run -d -p "8081:80" -p "8082:443" docker.io/nginx:latest
```


## docker ps(查看容器列表)
### usage
```
# docker ps --help

Usage:	docker ps [OPTIONS]

List containers

Options:
  -a, --all             Show all containers (default shows just running)
  -f, --filter value    Filter output based on conditions provided (default [])
      --format string   Pretty-print containers using a Go template
      --help            Print usage
  -n, --last int        Show n last created containers (includes all states) (default -1)
  -l, --latest          Show the latest created container (includes all states)
      --no-trunc        Don't truncate output
  -q, --quiet           Only display numeric IDs
  -s, --size            Display total file sizes
```

### demo
docker ps命令默认只会列出状态为running的容器，如果想查看处于exited状态的容器，加上-a选项:  

```
# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED              STATUS                      PORTS                                           NAMES
95d45968eb17        docker.io/nginx:latest   "nginx -g 'daemon off"   3 seconds ago        Up 2 seconds                80/tcp, 443/tcp                                 tender_knuth
4556cf56bf5d        docker.io/nginx:latest   "nginx -g 'daemon off"   About a minute ago   Exited (0) 39 seconds ago                                                   hungry_hoover
029260cd98e3        docker.io/nginx:latest   "nginx -g 'daemon off"   About a minute ago   Up About a minute           0.0.0.0:32769->80/tcp, 0.0.0.0:32768->443/tcp   dreamy_mclean
```

* CONTAINER ID: container的id
* IMAGE: 启动容器使用的镜像
* COMMAND: 启动容器时使用的命令
* CREATED: 容器创建的时间
* STATUS: 容器的状态，UP表示running
* PORTS: 容器对外暴露的端口(如果启动容器的时候没有会用-p或者-P选项，PORTS表示的是镜像EXPOSE的端口；如果启动容器的时候使用了-p或者-P选项，PORTS表示主机端口到容器端口的映射,0.0.0.0:32769->80/tcp表示的是宿主机所有网段的tcp 32769端口映射到容器的80端口)
* NAMES: 容器的名称，如果创建容器的时候不使用--name选项，会随机生成一个容器名称


想查看running状态的容器可以使用docker ps命令，如果想查看所有容器可以使用docker ps -a命令；如果只想查看处于exited状态的容器，可以使用-f选项，如下：  

```
# docker ps -f "status=exited"
```

## doker inspect(查看容器信息)
### usage
```
# docker inspect --help

Usage:	docker inspect [OPTIONS] CONTAINER|IMAGE|TASK [CONTAINER|IMAGE|TASK...]

Return low-level information on a container, image or task

  -f, --format       Format the output using the given go template
  --help             Print usage
  -s, --size         Display total file sizes if the type is container
  --type             Return JSON for specified type, (e.g image, container or task)
```  



## docker stop(停止容器)
### usage
```
# docker stop --help

Usage:	docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop one or more running containers

Options:
      --help       Print usage
  -t, --time int   Seconds to wait for stop before killing it (default 10)
```  

### demo
停止id为080f7a076470的容器

```
# docker stop 080f7a076470
```

停止容器后，容器的状态为exited。  


## docker start(启动容器)
### usage
```
# docker start --help

Usage:	docker start [OPTIONS] CONTAINER [CONTAINER...]

Start one or more stopped containers

Options:
  -a, --attach               Attach STDOUT/STDERR and forward signals
      --detach-keys string   Override the key sequence for detaching a container
      --help                 Print usage
  -i, --interactive          Attach container's STDIN
```

### demo
启动id为080f7a076470的容器

```
# docker start 080f7a076470
```

在运行的容器中对文件做的变更，停止容器后重启容器，变更还存在。

比如在运行的容器中创建一个文件/test.txt，停止容器后重新启动容器，/test.txt文件还在。


## docker rm(删除容器)
### usage
```
# docker rm --help

Usage:	docker rm [OPTIONS] CONTAINER [CONTAINER...]

Remove one or more containers

Options:
  -f, --force     Force the removal of a running container (uses SIGKILL)
      --help      Print usage
  -l, --link      Remove the specified link
  -v, --volumes   Remove the volumes associated with the container
```

### demo  
删除id为d1b07fe77248的容器(注意不能直接删除处于running状态的容器，如果下面的容器处于running状态，删除时会报错):  

```
# docker rm d1b07fe77248
```

报错

```
Error response from daemon: You cannot remove a running container d1b07fe772486652b518a98a5dcbf32fa3b1d5e2f454172b6914ced416e99162. Stop the container before attempting removal or use -f
```

如果想删除处于running状态的容器，可以使用-f选项

```
# docker rm -f d1b07fe77248
```

如果想清空所有运行和非运行状态的容器

```
# docker rm -f $(docker ps -aq)
```

如果想清空所有exited状态的容器

```
# docker rm -f $(docker ps -q -f "status=exited")
```

## docker exec(在容器中执行命令)
### usage
```
# docker exec --help

Usage:	docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

Run a command in a running container

  -d, --detach         Detached mode: run command in the background
  --detach-keys        Override the key sequence for detaching a container
  --help               Print usage
  -i, --interactive    Keep STDIN open even if not attached
  --privileged         Give extended privileges to the command
  -t, --tty            Allocate a pseudo-TTY
  -u, --user           Username or UID (format: <name|uid>[:<group|gid>])
```


### demo

在id为88d48f2b9bfd的容器中执行/bin/bash命令，进入交互模式:  

```
# docker exec -it 88d48f2b9bfd /bin/bash
```


## docker top(查看容器内的进程)
### usage
```
# docker top --help

Usage:	docker top CONTAINER [ps OPTIONS]

Display the running processes of a container

Options:
      --help   Print usage
```      

### demo

```
# docker top 88d48f2b9bfd
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                7735                7718                0                   08:19               ?                   00:00:00            nginx: master process nginx -g daemon off;
104                 7757                7735                0                   08:19               ?                   00:00:00            nginx: worker process
```

## docker port(查看端口映射)
### usage
```
# docker port --help

Usage:	docker port CONTAINER [PRIVATE_PORT[/PROTO]]

List port mappings or a specific mapping for the container

Options:
      --help   Print usage
```

### demo
```

```      



## docker stats(查看容器的资源占用)
### usage
```
# docker stats --help

Usage:	docker stats [OPTIONS] [CONTAINER...]

Display a live stream of container(s) resource usage statistics

Options:
  -a, --all         Show all containers (default shows just running)
      --help        Print usage
      --no-stream   Disable streaming stats and only pull the first result
```

### demo
查看所有容器的资源使用情况:  

```
# docker stats
CONTAINER           CPU %               MEM USAGE / LIMIT      MEM %               NET I/O             BLOCK I/O           PIDS
080f7a076470        0.00%               7.688 MiB / 3.86 GiB   0.19%               578 B / 578 B       6.955 MB / 0 B      0
88d48f2b9bfd        0.00%               9.609 MiB / 3.86 GiB   0.24%               1.136 kB / 648 B    9.106 MB / 0 B      0
```

如果只想查看id为88d48f2b9bfd的容器的资源使用情况:  

```
# docke stats 88d48f2b9bfd
CONTAINER           CPU %               MEM USAGE / LIMIT      MEM %               NET I/O             BLOCK I/O           PIDS
88d48f2b9bfd        0.00%               9.609 MiB / 3.86 GiB   0.24%               1.206 kB / 648 B    9.106 MB / 0 B      0
```




## docker rename(重命名容器)
### usage
```
# docker rename --help

Usage:	docker rename CONTAINER NEW_NAME

Rename a container

Options:
      --help   Print usage
```      

### demo
将id为88d48f2b9bfd的容器重命名为loadbalance-1

```
# docker rename 88d48f2b9bfd loadbalance-1
```


# 网络管理



# 存储相关



### usage


### demo


















