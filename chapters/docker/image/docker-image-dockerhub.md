# DockerHub
DockerHub的功能类似于Github,不同的是DockerHub托管的是Docker image。

我们可以在DockerHub上创建、分享、搜索image。

docker hub地址: [https://hub.docker.com](https://hub.docker.com)




# Tutorial


在DockerHub上创建一个repository(对应一个镜像),需要以下信息:

* namespace: 一般就是我们在DockerHub上的账户名,比如frank6866
* 镜像名称: 自定义的名称,比如"performance-tool"
* Short Description: 简短的描述,比如"performance tools for docker testing"
* Full Description: 详细描述,比如"This image based on CentOS7, contains the following tools: iproute, iperf, nmon..."




下面演示了如何在本地打包一个镜像并上传到DockerHub上去,并在其他地方使用。








daocloud.io/library/centos:7.1.1503


docker pull frank6866/performance-tool


docker build -t frank6866/performance-tool:v1.0 .
docker login


找到image的id,并创建一个latest的tag,方便使用(不用显示输入tag):

docker tag 61e8db203f02 frank6866/performance-tool:latest


docker push frank6866/performance-tool:v1.0
docker push frank6866/performance-tool:latest



官网的DockerHub虽然可以免费创建镜像仓库,但是国内访问网络有问题;DaoCloud的镜像仓库功能虽然网络没问题，不过是付费的,每个月至少200.



# 碰到的问题
## TLS handshake timeout

docker pull centos:7.1.1503
Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: TLS handshake timeout

解决方法: 使用代理

