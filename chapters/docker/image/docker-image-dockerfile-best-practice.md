# Dockerfile最佳实践

## 使用缓存
Dockerfile的每条指令都会讲结果提交为镜像，下一个指令在上一个指令提交的镜像的基础上构建；如果一个镜像存在相同的父镜像和指令，Docker会使用已有的镜像而不是执行该指令。

注意，下面两个指令不会用到缓存

* MAINTAINER
* ADD





# 参考
* https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/
* http://dockone.io/article/131

