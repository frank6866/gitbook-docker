# 认证

# Kubernetes中的用户
Kubernetes集群有两种类型的用户: service accounts和normal users。

* service accounts: service accounts类型的用户由Kubernetes管理
* normal user: normal user是被外部的、独立的服务管理的，比如keystone。

在Kubernetes中，没有对象来表示normal user，normal不能通过Kubernetes API被加入到集群中；而是在外部服务中添加normal user，比如在keystone中添加用户。   

service accounts是被Kubernetes API管理的用户。service accounts和特定的namespace绑定，service accounts可以自动被创建或者手动创建。  

service accounts和一系列的存储为Secrets的credentials联系起来，Secrets被挂载到pods中，允许集群中的进程和Kubernetes API交互。  

API请求可以和service account关联，也可以和normal user关联，也可以被当做匿名请求。这也就意味着，在集群内部或者外部的进程，或者kubectl命令，在调用API的时候，必须经过认证，或者被当做匿名用户。  

# 认证策略
Kubernetes通过authentication plugins使用**client certificate**，**bearer tokens**，**authenticating proxy**或者**HTTP basic auth**来认证。当有请求到达API server时，plugins试图给请求添加下面的一些属性:  

* Username: 用户名(字符串)
* UID: 用户id(字符串)
* Groups: 用来表示用户属于的组(字符串数组)
* Extra fields: 附加的字段 

我们可以一起启用多个认证方式，我们至少需要使用两个方法:  

* 对于service account使用service account
* 对于normal user，至少一种其他的方法

如果使用了多个认证方式，当某个认证通过后就不会进行其他的认证了；API server并不保证认证的执行顺序。  

**system:authenticated**组包含了所有通过认证的用户。  
















