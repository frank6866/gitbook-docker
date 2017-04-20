# /var/lib/docker目录


```
# tree /var/lib/docker/ -L 1
/var/lib/docker/
├── containers
├── devicemapper
├── image
├── network
├── swarm
├── tmp
├── trust
└── volumes
```


* volumes: 当使用-v只指定了容器里面的挂载点时，会在宿主机下这个目录下面给容器创建一个目录，并挂载到容器里面











