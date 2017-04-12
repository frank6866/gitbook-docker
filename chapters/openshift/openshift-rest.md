# openshift rest

# 使用user/password获取token
> 注意: 账户密码、token等数据已脱敏,直接执行下面的命令可能会失败;请在测试时使用真实的账户密码。

OpenShift使用OAuth进行认证,生成token的API基于WWW-Authenticate进行认证。

假设用户名为: oc_user,密码为: oc_pwd

对字符串 "oc_user:oc_pwd" 进行base64编码:

```
➜  ~ echo -n "oc_user:oc_pwd" | base64
b2NfdXNlcjpvY19wd2Q=
```

```
➜  ~ curl -k -v -XGET  -H "X-Csrf-Token: 1" -H "Authorization: Basic b2NfdXNlcjpvY19wd2Q=" "https://10.12.10.18:8443/oauth/authorize?response_type=token&client_id=openshift-challenging-client"
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 10.12.10.18...
* TCP_NODELAY set
* Connected to 10.12.10.18 (10.12.10.18) port 8443 (#0)
* TLS 1.2 connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate: 10.12.10.18
* Server certificate: openshift-signer@1479806685
> GET /oauth/authorize?response_type=token&client_id=openshift-challenging-client HTTP/1.1
> Host: 10.12.10.18:8443
> User-Agent: curl/7.51.0
> Accept: */*
> X-Csrf-Token: 1
> Authorization: Basic b2NfdXNlcjpvY19wd2Q=
>
< HTTP/1.1 302 Found
< Cache-Control: no-cache, no-store, max-age=0, must-revalidate
< Expires: Fri, 01 Jan 1990 00:00:00 GMT
< Location: https://10.12.10.18:8443/oauth/token/implicit#access_token=abcdefghijklmnopqrstuvwxyz&expires_in=86400&scope=user%3Afull&token_type=Bearer
< Pragma: no-cache
< Set-Cookie: ssn=MTQ5MTkwMjQ4M3xtdVVRVGtkYkVMZ0VpdVRVbWFyRGhJWUU4TG1XRUQ3T2VQQlh0VTMzNWxLaS1zU2NlQkw3ZGxpSUVLUi1YaENZNlZtUFVUbVd5LV9WM2RmUVByczVfTnpVWm55UmtRVXoydFFGSDllWU9vN1dId3k2NGpFRXUwOGx0aVRCUVg2d0Z3PT18ku9V2n7hBmJcSz_kLLpWZmkgQx9rpEXOGutVW1YkxeI=; Path=/; Expires=Tue, 11 Apr 2017 09:26:23 GMT; Max-Age=300; HttpOnly; Secure
< Date: Tue, 11 Apr 2017 09:21:23 GMT
< Content-Length: 0
< Content-Type: text/plain; charset=utf-8
<
* Curl_http_done: called premature == 0
* Connection #0 to host 10.12.10.18 left intact
```

在HTTP响应头里面的Location如下:

```
Location: https://10.12.10.18:8443/oauth/token/implicit#access_token=abcdefghijklmnopqrstuvwxyz&expires_in=86400&scope=user%3Afull&token_type=Bearer
```

其中access_token是生成的token,可以用于后面API的使用。

# 镜像
## 列出所有镜像
```
curl -k -v -XGET -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" https://10.12.10.18:8443/oapi/v1/namespaces/fb/imagestreams | python -mjson.tool
```


## 导入镜像
新建请求体文件:  

```
$ vi import-image.data
{
    "kind": "ImageStreamImport",
    "apiVersion": "v1",
    "metadata": {
        "name": "fe-web",
        "namespace": "fb",
        "creationTimestamp": null
    },
    "spec": {
        "import": true,
        "images": [
            {
                "from": {
                    "kind": "DockerImage",
                    "name": "docker.elenet.me/fe/fe-web:0.0.1"
                },
                "to": {
                    "name": "0.0.1"
                },
                "importPolicy": {}
            }
        ]
    },
    "status": {}
}
```


调用api:  

```
curl -k -v -XPOST  -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" -H "Accept: application/json, */*" -H "Content-Type: application/json" --data @import-image.data https://10.12.10.18:8443/oapi/v1/namespaces/fb/imagestreamimports | python -mjson.tool
```


## 删除镜像

```
curl -k -v -XDELETE  -H "Accept: application/json, */*" -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" https://10.12.10.18:8443/oapi/v1/namespaces/fb/imagestreams/fe-web
```


# app管理
## 列出所有的service

```
curl -k -v -XGET -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" -H "Accept: application/json, */*" https://10.12.10.18:8443/api/v1/namespaces/fb/services  | python -mjson.tool
```

## 创建一个app
新建请求体文件:  

```
# vi create-app.data
{
    "kind": "DeploymentConfig",
    "apiVersion": "v1",
    "metadata": {
        "name": "fe-web",
        "creationTimestamp": null,
        "labels": {
            "app": "fe-web"
        },
        "annotations": {
            "openshift.io/generated-by": "OpenShiftNewApp"
        }
    },
    "spec": {
        "strategy": {
            "resources": {}
        },
        "triggers": [
            {
                "type": "ConfigChange"
            },
            {
                "type": "ImageChange",
                "imageChangeParams": {
                    "automatic": true,
                    "containerNames": [
                        "fe-web"
                    ],
                    "from": {
                        "kind": "ImageStreamTag",
                        "namespace": "fb",
                        "name": "fe-web: 0.0.1"
                    }
                }
            }
        ],
        "replicas": 1,
        "test": false,
        "selector": {
            "app": "fe-web",
            "deploymentconfig": "fe-web"
        },
        "template": {
            "metadata": {
                "creationTimestamp": null,
                "labels": {
                    "app": "fe-web",
                    "deploymentconfig": "fe-web"
                },
                "annotations": {
                    "openshift.io/generated-by": "OpenShiftNewApp"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "fe-web",
                        "image": "docker.elenet.me/fe/fe-web: 0.0.1",
                        "resources": {}
                    }
                ]
            }
        }
    },
    "status": {}
}
```

调用api:  

```
curl -k -v -XPOST  -H "Accept: application/json, */*" -H "Content-Type: application/json" -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" --data @create-app.data https://10.12.10.18:8443/oapi/v1/namespaces/fb/deploymentconfigs
```


## 删除app
```
curl -k -v -XDELETE  -H "Accept: application/json, */*" -H "Authorization: Bearer cyLXuTVAaXj8c7wF3jefkCvElzsPAG0pxD8j7F-fMQU" https://10.12.10.18:8443/oapi/v1/namespaces/fb/deploymentconfigs/fe-web
```



# https证书
例子中为了方便演示功能,在curl命令中使用了-k选项(-k, --insecure, Allow connections to SSL sites without certs (H)),可以不使用证书。

正式使用时建议使用证书,下载地址是[http://10.12.10.10/ca/10.12.10.18-ca.crt](http://10.12.10.10/ca/10.12.10.18-ca.crt),在curl工具中使用--cacert 10.12.10.18-ca.crt选项指定证书。



