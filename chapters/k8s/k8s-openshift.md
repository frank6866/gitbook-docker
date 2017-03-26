# openshift


# openshift安装
## node节点安装

sudo yum -y install http://10.12.10.10/rpm/openshift/x86_64/openshift-v1.4.1-20170317T114622Z.el7.centos.x86_64.rpm

curl http://10.12.10.10/rpm/os-config -o os-config
chmod a+x os-config

sudo ./os-config --master-url="https://10.12.10.18:8443" --nodename="nl-cloud-dyc-k8s-1"
该命令返回<nil>表示正常输出，没有错误.



sudo yum -y install http://10.12.10.10/rpm/docker/docker-engine-selinux-1.12.5.101-1.el7.centos.noarch.rpm
sudo yum -y install http://10.12.10.10/rpm/docker/docker-engine-1.12.5.101-1.el7.centos.x86_64.rpm



vi /etc/docker/daemon.json

```

```

vi /etc/docker/env

```
_OVERLAY_HOST_MODE=1
```

vi /lib/systemd/system/docker.service

```
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
EnvironmentFile=-/etc/docker/env
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process

[Install]
WantedBy=multi-user.target
```


systemctl daemon-reload
systemctl enable docker openshift-slave
systemctl start docker
systemctl start openshift-slave
