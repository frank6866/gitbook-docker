# docker run(运行容器)

## 不加选项
使用nginx镜像启动容器(不加选项):  

```
# docker run nginx
```

启动的这个容器会占用标准输入，可以使用Ctrl+C退出容器。

## -d(后台启动)
在后台运行容器(使用-d选项)，

```
# docker run -d nginx
```

## --name(显示名称)
在启动容器的时候可以给容器指定一个名称(比如frontend):  

```
# docker run -d --name frontend nginx
```

## -h(主机名)

容器默认使用其id作为主机名，如果想自定义主机名，可以使用-h选项(或者--hostname)指定容器的主机名，比如，启动一个容器设置主机名为tutorial-01:  

```
# docker run -d --name backend -h tutorial-01 nginx
0fb09e3746e1e6495f9e7d825ba6ee2b32716e12707fff4a30bb2b70998c0b64

[root@nl-cloud-dyc-k8s-1 my_nginx]# docker exec -it backend /bin/bash
root@tutorial-01:/# hostname
tutorial-01
```

## -p或-P(端口映射)
* -p: 指定端口映射
* -P: 随机端口映射(助记词:大随)

将镜像定好的端口随机映射到宿主机的端口上(使用-P选项):  

```
# docker run -d -P nginx
b4840b0bf8266f6e3cfada38f648dc305c6aed73e4695060823c2bde95b4e95d

# docker ps -f "id=b4840"
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                           NAMES
b4840b0bf826        nginx               "nginx -g 'daemon off"   15 seconds ago      Up 14 seconds       0.0.0.0:32773->80/tcp, 0.0.0.0:32772->443/tcp   nauseous_swirles
```

将容器的80端口映射到宿主机的8001端口，容器的443端口映射到主机的8082端口(使用-p选项):  

```
# docker run -d -p "8081:80" -p "8082:443" nginx
88c0c7856f24854e6f14c2441cc837557b1dde0408ac834f2c75133d4afc3b0c

# docker ps -f "id=88c0c"
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                         NAMES
88c0c7856f24        nginx               "nginx -g 'daemon off"   9 seconds ago       Up 7 seconds        0.0.0.0:8081->80/tcp, 0.0.0.0:8082->443/tcp   mad_wing
```

## -it和--rm(自动删除)
-it和--rm一般在调试的时候组合使用。  

* -i: 以交互方式启动容器
* -t: 分配一个伪tty
* --rm: 当容器处于exited时自动被删掉

```
# docker run -it --rm nginx /bin/bash
root@1334705345be:/# exit
exit

[root@nl-cloud-dyc-k8s-1 my_nginx]# docker ps -f "id=1334705345be"
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

发现容器退出后就被删掉了。  


## -v
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




# usage
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
