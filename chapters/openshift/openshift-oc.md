# oc
oc是OpenShift Client的简称，oc可以帮助我们在OpenShift或者Kubernetes兼容的平台上develop、build、deploy或者run我们的application。oc的子命令**adm**包含了管理集群的命令。  

命令帮助

```
# oc --help
OpenShift Client

This client helps you develop, build, deploy, and run your applications on any OpenShift or Kubernetes compatible
platform. It also includes the administrative commands for managing a cluster under the 'adm' subcommand.

Basic Commands:
  types           An introduction to concepts and types
  login           Log in to a server
  new-project     Request a new project
  new-app         Create a new application
  status          Show an overview of the current project
  project         Switch to another project
  projects        Display existing projects
  explain         Documentation of resources
  cluster         Start and stop OpenShift cluster
  idle            Idle scalable resources

Build and Deploy Commands:
  rollout         Manage a Kubernetes deployment or OpenShift deployment config
  deploy          View, start, cancel, or retry a deployment
  rollback        Revert part of an application back to a previous deployment
  new-build       Create a new build configuration
  start-build     Start a new build
  cancel-build    Cancel running, pending, or new builds
  import-image    Imports images from a Docker registry
  tag             Tag existing images into image streams

Application Management Commands:
  get             Display one or many resources
  describe        Show details of a specific resource or group of resources
  edit            Edit a resource on the server
  set             Commands that help set specific features on objects
  label           Update the labels on a resource
  annotate        Update the annotations on a resource
  expose          Expose a replicated application as a service or route
  delete          Delete one or more resources
  scale           Change the number of pods in a deployment
  autoscale       Autoscale a deployment config, deployment, replication controller, or replica set
  secrets         Manage secrets
  serviceaccounts Manage service accounts in your project

Troubleshooting and Debugging Commands:
  logs            Print the logs for a resource
  rsh             Start a shell session in a pod
  rsync           Copy files between local filesystem and a pod
  port-forward    Forward one or more local ports to a pod
  debug           Launch a new instance of a pod for debugging
  exec            Execute a command in a container
  proxy           Run a proxy to the Kubernetes API server
  attach          Attach to a running container
  run             Run a particular image on the cluster

Advanced Commands:
  adm             Tools for managing a cluster
  create          Create a resource by filename or stdin
  replace         Replace a resource by filename or stdin
  apply           Apply a configuration to a resource by filename or stdin
  patch           Update field(s) of a resource using strategic merge patch
  process         Process a template into list of resources
  export          Export resources so they can be used elsewhere
  extract         Extract secrets or config maps to disk
  observe         Observe changes to resources and react to them (experimental)
  policy          Manage authorization policy
  convert         Convert config files between different API versions
  import          Commands that import applications

Settings Commands:
  logout          End the current server session
  config          Change configuration files for the client
  whoami          Return information about the current session
  completion      Output shell completion code for the given shell (bash or zsh)

Other Commands:
  help            Help about any command
  version         Display client and server versions

Use "oc <command> --help" for more information about a given command.
Use "oc options" for a list of global command-line options (applies to all commands).
```




# Basic Commands
## types           
An introduction to concepts and types

### usage
```
# oc help types
Concepts and Types

Kubernetes and OpenShift help developers and operators build, test, and deploy applications in a containerized cloud
environment. Applications may be composed of all of the components below, although most developers will be concerned
with Services, Deployments, and Builds for delivering changes.

Concepts:

* Containers:
    A definition of how to run one or more processes inside of a portable Linux
    environment. Containers are started from an Image and are usually isolated
    from other containers on the same machine.

* Image:
    A layered Linux filesystem that contains application code, dependencies,
    and any supporting operating system libraries. An image is identified by
    a name that can be local to the current cluster or point to a remote Docker
    registry (a storage server for images).

* Pods [pod]:
    A set of one or more containers that are deployed onto a Node together and
    share a unique IP and Volumes (persistent storage). Pods also define the
    security and runtime policy for each container.

* Labels:
    Labels are key value pairs that can be assigned to any resource in the
    system for grouping and selection. Many resources use labels to identify
    sets of other resources.

* Volumes:
    Containers are not persistent by default - on restart their contents are
    cleared. Volumes are mounted filesystems available to Pods and their
    containers which may be backed by a number of host-local or network
    attached storage endpoints. The simplest volume type is EmptyDir, which
    is a temporary directory on a single machine. Administrators may also
    allow you to request a Persistent Volume that is automatically attached
    to your pods.

* Nodes [node]:
    Machines set up in the cluster to run containers. Usually managed
    by administrators and not by end users.

* Services [svc]:
    A name representing a set of pods (or external servers) that are
    accessed by other pods. The service gets an IP and a DNS name, and can be
    exposed externally to the cluster via a port or a Route. It's also easy
    to consume services from pods because an environment variable with the
    name <SERVICE>_HOST is automatically injected into other pods.

* Routes [route]:
    A route is an external DNS entry (either a top level domain or a
    dynamically allocated name) that is created to point to a service so that
    it can be accessed outside the cluster. The administrator may configure
    one or more Routers to handle those routes, typically through an Apache
    or HAProxy load balancer / proxy.

* Replication Controllers [rc]:
    A replication controller maintains a specific number of pods based on a
    template that match a set of labels. If pods are deleted (because the
    node they run on is taken out of service) the controller creates a new
    copy of that pod. A replication controller is most commonly used to
    represent a single deployment of part of an application based on a
    built image.

* Deployment Configuration [dc]:
    Defines the template for a pod and manages deploying new images or
    configuration changes whenever those change. A single deployment
    configuration is usually analogous to a single micro-service. Can support
    many different deployment patterns, including full restart, customizable
    rolling updates, and fully custom behaviors, as well as pre- and post-
    hooks. Each deployment is represented as a replication controller.

* Build Configuration [bc]:
    Contains a description of how to build source code and a base image into a
    new image - the primary method for delivering changes to your application.
    Builds can be source based and use builder images for common languages like
    Java, PHP, Ruby, or Python, or be Docker based and create builds from a
    Dockerfile. Each build configuration has web-hooks and can be triggered
    automatically by changes to their base images.

* Builds [build]:
    Builds create a new image from source code, other images, Dockerfiles, or
    binary input. A build is run inside of a container and has the same
    restrictions normal pods have. A build usually results in an image pushed
    to a Docker registry, but you can also choose to run a post-build test that
    does not push an image.

* Image Streams and Image Stream Tags [is,istag]:
    An image stream groups sets of related images under tags - analogous to a
    branch in a source code repository. Each image stream may have one or
    more tags (the default tag is called "latest") and those tags may point
    at external Docker registries, at other tags in the same stream, or be
    controlled to directly point at known images. In addition, images can be
    pushed to an image stream tag directly via the integrated Docker
    registry.

* Secrets [secret]:
    The secret resource can hold text or binary secrets for delivery into
    your pods. By default, every container is given a single secret which
    contains a token for accessing the API (with limited privileges) at
    /var/run/secrets/kubernetes.io/serviceaccount. You can create new
    secrets and mount them in your own pods, as well as reference secrets
    from builds (for connecting to remote servers) or use them to import
    remote images into an image stream.

* Projects [project]:
    All of the above resources (except Nodes) exist inside of a project.
    Projects have a list of members and their roles, like viewer, editor,
    or admin, as well as a set of security controls on the running pods, and
    limits on how many resources the project can use. The names of each
    resource are unique within a project. Developers may request projects
    be created, but administrators control the resources allocated to
    projects.

For more, see https://docs.openshift.com

Usage:
  oc types [options]

Examples:
  # View all projects you have access to
  oc get projects

  # See a list of all services in the current project
  oc get svc

  # Describe a deployment configuration in detail
  oc describe dc mydeploymentconfig

  # Show the images tagged into an image stream
  oc describe is ruby-centos7

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo



## login           
Log in to a server，登录到OpenShift上去，也可以用来切换用户

### usage
```
# oc help login
Log in to your server and save login for subsequent use

First-time users of the client should run this command to connect to a server, establish an authenticated session, and
save connection to the configuration file. The default configuration will be saved to your home directory under
".kube/config".

The information required to login -- like username and password, a session token, or the server details -- can be
provided through flags. If not provided, the command will prompt for user input as needed.

Usage:
  oc login [URL] [options]

Examples:
  # Log in interactively
  oc login

  # Log in to the given server with the given certificate authority file
  oc login localhost:8443 --certificate-authority=/path/to/cert.crt

  # Log in to the given server with the given credentials (will not prompt interactively)
  oc login localhost:8443 --username=myuser --password=mypass

Options:
  -p, --password='': Password, will prompt if not provided
  -u, --username='': Username, will prompt if not provided      --certificate-authority='': Path to a cert. file for the
certificate authority
      --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity. This will
make your HTTPS connections insecure
      --token='': Bearer token for authentication to the API server

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
切换用户

```



```




## new-project     
Request a new project

### usage
```
# oc help new-project
Create a new project for yourself

If your administrator allows self-service, this command will create a new project for you and assign you as the project
admin.

After your project is created it will become the default project in your config.

Usage:
  oc new-project NAME [--display-name=DISPLAYNAME] [--description=DESCRIPTION] [options]

Examples:
  # Create a new project with minimal information
  oc new-project web-team-dev

  # Create a new project with a display name and description
  oc new-project web-team-dev --display-name="Web Team Development" --description="Development project for the web
team."

Options:
      --description='': Project description
      --display-name='': Project display name
      --skip-config-write=false: If true, the project will not be set as a cluster entry in kubeconfig after being
created

Use "oc options" for a list of global command-line options (applies to all commands).
```


### demo
oc new-project tutorial --display-name="openshift tutorial" --description="This is a tutorial project in openshift"


## new-app         
Create a new application，根据source code、template或者image创建应用。

TODO: project和app是什么关系

### usage
```
# oc help new-app
Create a new application by specifying source code, templates, and/or images

This command will try to build up the components of an application using images, templates, or code that has a public
repository. It will lookup the images on the local Docker installation (if available), a Docker registry, an integrated
image stream, or stored templates.

If you specify a source code URL, it will set up a build that takes your source code and converts it into an image that
can run inside of a pod. Local source must be in a git repository that has a remote repository that the server can see.
The images will be deployed via a deployment configuration, and a service will be connected to the first public port of
the app. You may either specify components using the various existing flags or let new-app autodetect what kind of
components you have provided.

If you provide source code, a new build will be automatically triggered. You can use 'oc status' to check the progress.

Usage:
  oc new-app (IMAGE | IMAGESTREAM | TEMPLATE | PATH | URL ...) [options]

Examples:
  # List all local templates and image streams that can be used to create an app
  oc new-app --list

  # Create an application based on the source code in the current git repository (with a public remote)
  # and a Docker image
  oc new-app . --docker-image=repo/langimage

  # Create a Ruby application based on the provided [image]~[source code] combination
  oc new-app centos/ruby-22-centos7~https://github.com/openshift/ruby-ex.git

  # Use the public Docker Hub MySQL image to create an app. Generated artifacts will be labeled with db=mysql
  oc new-app mysql MYSQL_USER=user MYSQL_PASSWORD=pass MYSQL_DATABASE=testdb -l db=mysql

  # Use a MySQL image in a private registry to create an app and override application artifacts' names
  oc new-app --docker-image=myregistry.com/mycompany/mysql --name=private

  # Create an application from a remote repository using its beta4 branch
  oc new-app https://github.com/openshift/ruby-hello-world#beta4

  # Create an application based on a stored template, explicitly setting a parameter value
  oc new-app --template=ruby-helloworld-sample --param=MYSQL_USER=admin

  # Create an application from a remote repository and specify a context directory
  oc new-app https://github.com/youruser/yourgitrepo --context-dir=src/build

  # Create an application based on a template file, explicitly setting a parameter value
  oc new-app --file=./example/myapp/template.json --param=MYSQL_USER=admin

  # Search all templates, image streams, and Docker images for the ones that match "ruby"
  oc new-app --search ruby

  # Search for "ruby", but only in stored templates (--template, --image-stream and --docker-image
  # can be used to filter search results)
  oc new-app --search --template=ruby

  # Search for "ruby" in stored templates and print the output as an YAML
  oc new-app --search --template=ruby --output=yaml

Options:
      --allow-missing-images=false: If true, indicates that referenced Docker images that cannot be found locally or in
a registry should still be used.
      --allow-missing-imagestream-tags=false: If true, indicates that image stream tags that don't exist should still be
used.
      --as-test=false: If true create this application as a test deployment, which validates that the deployment
succeeds and then scales down.
      --code=[]: Source code to use to build this application.
      --context-dir='': Context directory to be used for the build.
      --docker-image=[]: Name of a Docker image to include in the app.
      --dry-run=false: If true, show the result of the operation without performing it.
  -e, --env=[]: Specify a key-value pair for an environment variable to set into each container. This doesn't apply to
objects created from a template, use parameters instead.
  -f, --file=[]: Path to a template file to use for the app.
      --grant-install-rights=false: If true, a component that requires access to your account may use your token to
install software into your project. Only grant images you trust the right to run with your token.
      --group=[]: Indicate components that should be grouped together as <comp1>+<comp2>.
      --image=[]: Name of an image stream to use in the app. (deprecated)
  -i, --image-stream=[]: Name of an image stream to use in the app.
      --insecure-registry=false: If true, indicates that the referenced Docker images are on insecure registries and
should bypass certificate checking
  -l, --labels='': Label to set in all resources for this application.
  -L, --list=false: List all local templates and image streams that can be used to create.
      --name='': Set name to use for generated application artifacts
      --no-install=false: Do not attempt to run images that describe themselves as being installable
  -o, --output='': Output results as yaml or json instead of executing, or use name for succint output (resource/name).
      --output-version='': The preferred API versions of the output objects
  -p, --param=[]: Specify a key-value pair (e.g., -p FOO=BAR) to set/override a parameter value in the template.
  -S, --search=false: Search all templates, image streams, and Docker images that match the arguments provided.
      --strategy='': Specify the build strategy to use if you don't want to detect (docker|source).
      --template=[]: Name of a stored template to use in the app.

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
List all local templates and image streams that can be used to create an app，列出所有可以用来创建app的template和image streams.


oc new-app --list

```
# oc new-app --list
Templates (oc new-app --template=<template>)
-----
build-git
  Project: openshift
  Template for deploying Builder Source from Git.
build-github
  Project: openshift
  Template for deploying Builder Source from Github.
config-pet
  Project: openshift
  Template for deploying simple App.
image-stream
  Project: openshift
  Self define image stream
mysql-ephemeral
  Project: openshift
  MySQL database service, without persistent storage. WARNING: Any data stored will be lost upon pod destruction. Only use this template for testing
noc-web
  Project: openshift
  Template for deploying noc-platform. Requires cluster-admin.
nodejs-gitlab
  Project: openshift
  Template for deploying Builder Source from Git.
standard-app
  Project: openshift
  Template for deploying simple App.
standard-config
  Project: openshift
  Template for deploying simple App.
standard-image
  Project: openshift
  Template for deploying simple App.
whoami
  Project: openshift
  Template for deploying registry web console. Requires cluster-admin.
```




Use the public Docker Hub MySQL image to create an app. Generated artifacts will be labeled with db=mysql_test_frank

```
# oc new-app mysql MYSQL_USER=user MYSQL_PASSWORD=pass MYSQL_DATABASE=testdb -l db=mysql_test_frank
--> Found Docker image 5faba1a (6 days old) from Docker Hub for "mysql"

    * An image stream will be created as "mysql:latest" that will track this image
    * This image will be deployed in deployment config "mysql"
    * Port 3306/tcp will be load balanced by service "mysql"
      * Other containers can access this service through the hostname "mysql"
    * This image declares volumes and will default to use non-persistent, host-local storage.
      You can add persistent volumes later by running 'volume dc/mysql --add ...'
    * WARNING: Image "mysql" runs as the 'root' user which may not be permitted by your cluster administrator

--> Creating resources with label db=mysql_test_frank ...
    imagestream "mysql" created
    deploymentconfig "mysql" created
    service "mysql" created
--> Success
    WARNING: No Docker registry has been configured with the server. Automatic builds and deployments may not function.
    Run 'oc status' to view your app.
```    

**oc new-app mysql**中的mysql是镜像的名称。



## status          
Show an overview of the current project，从一个高的层次展示当前项目的状态。



### usage
```
# oc help status
Show a high level overview of the current project

This command will show services, deployment configs, build configurations, and active deployments. If you have any
misconfigured components information about them will be shown. For more information about individual items, use the
describe command (e.g. oc describe buildConfig, oc describe deploymentConfig, oc describe service).

You can specify an output format of "-o dot" to have this command output the generated status graph in DOT format that
is suitable for use by the "dot" command.

Usage:
  oc status [-o dot | -v ] [options]

Examples:
  # See an overview of the current project.
  oc status

  # Export the overview of the current project in an svg file.
  oc status -o dot | dot -T svg -o project.svg

  # See an overview of the current project including details for any identified issues.
  oc status -v

Options:
      --all-namespaces=false: Display status for all namespaces (must have cluster admin)
  -o, --output='': Output format. One of: dot.
  -v, --verbose=false: See details for resolving issues.

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
查看当前项目的状态

```
# oc status
In project spark-cluster on server https://xxx.xxx.xxx.xxx:xxxx

svc/spark-master - 172.30.45.71:7077
  rc/spark-master-controller runs gcr.io/google_containers/spark:1.5.2_v1
    rc/spark-master-controller created 7 days ago - 1 pod

http://spark.router.pso.elenet.me (svc/spark-webui)
  rc/spark-master-controller runs gcr.io/google_containers/spark:1.5.2_v1
    rc/spark-master-controller created 7 days ago - 1 pod

http://zeppelin.router.pso.elenet.me (svc/zeppelin)
  rc/zeppelin-controller runs gcr.io/google_containers/zeppelin:v0.5.6_v1
    rc/zeppelin-controller created 7 days ago

rc/spark-worker-controller runs gcr.io/google_containers/spark:1.5.2_v1
  rc/spark-worker-controller created 7 days ago - 4 pods

Errors:
  * pod/spark-worker-controller-7g8mw is crash-looping

1 error and 4 warnings identified, use 'oc status -v' to see details.
```





## project         
Switch to another project

### usage
```
# oc help project
Switch to another project and make it the default in your configuration

If no project was specified on the command line, display information about the current active project. Since you can use
this command to connect to projects on different servers, you will occasionally encounter projects of the same name on
different servers. When switching to that project, a new local context will be created that will have a unique name -
for instance, 'myapp-2'. If you have previously created a context with a different name than the project name, this
command will accept that context name instead.

For advanced configuration, or to manage the contents of your config file, use the 'config' command.

Usage:
  oc project [NAME] [options]

Examples:
  # Switch to 'myapp' project
  oc project myapp

  # Display the project currently in use
  oc project

Options:
  -q, --short=false: If true, display only the project name

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
查看当前项目  

```
# oc project
Using project "ops" on server "https://xxx.xxx.xxx.xxx:xxxx".
```

切换到名为spark-cluster的项目:  

```
# oc project spark-cluster
Now using project "spark-cluster" on server "https://xxx.xxx.xxx.xxx:xxxx".
```



## projects        
Display existing projects，查看所有的project名称

### usage
```
# oc help projects
Display information about the current active project and existing projects on the server.

For advanced configuration, or to manage the contents of your config file, use the 'config' command.

Usage:
  oc projects [options]

Options:
  -q, --short=false: If true, display only the project names

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
查看所有的project

```
# oc projects
You have access to the following projects and can switch between them with 'oc project <projectname>':

	 ...
    ops
  * spark-cluster
  	 ...

Using project "spark-cluster" on server "https://xxx.xxx.xxx.xxx:xxxx".
```

前面有*号的表示是当前项目.

## explain         
Documentation of resources

### usage
```

```

### demo



## cluster         
Start and stop OpenShift cluster

### usage
```

```

### demo



## idle            
Idle scalable resources

### usage
```

```

### demo




# Build and Deploy Commands
## rollout         
Manage a Kubernetes deployment or OpenShift deployment config

### usage
```

```

### demo



## deploy          
View, start, cancel, or retry a deployment

### usage
```

```

### demo



## rollback        
Revert part of an application back to a previous deployment

### usage
```

```

### demo



## new-build       
Create a new build configuration

### usage
```

```

### demo



## start-build     
Start a new build

### usage
```

```

### demo



## cancel-build    
Cancel running, pending, or new builds

### usage
```

```

### demo



## import-image    
Imports images from a Docker registry

### usage
```

```

### demo



## tag             
Tag existing images into image streams

### usage
```

```

### demo




# Application Management Commands
应用管理命令

## get             
Display one or many resources，展示一个或者多个资源。  

### usage
```
# oc help get
Display one or many resources

Possible resources include builds, buildConfigs, services, pods, etc. To see a list of common resources, use 'oc get'.
Some resources may omit advanced details that you can see with '-o wide'.  If you want an even more detailed view, use
'oc describe'.

Usage:
  oc get
[(-o|--output=)json|yaml|wide|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...]
(TYPE [NAME | -l label] | TYPE/NAME ...) [flags] [options]

Examples:
  # List all pods in ps output format.
  oc get pods

  # List a single replication controller with specified ID in ps output format.
  oc get rc redis

  # List all pods and show more details about them.
  oc get -o wide pods

  # List a single pod in JSON output format.
  oc get -o json pod redis-pod

  # Return only the status value of the specified pod.
  oc get -o template pod redis-pod --template={{.currentState.status}}

Options:
      --all-namespaces=false: If present, list the requested object(s) across all namespaces. Namespace in current
context is ignored even if specified with --namespace.
      --export=false: If true, use 'export' for the resources.  Exported resources are stripped of cluster-specific
information.
  -f, --filename=[]: Filename, directory, or URL to a file identifying the resource to get from a server.
      --include-extended-apis=true: If true, include definitions of new APIs via calls to the API server. [default true]
  -L, --label-columns=[]: Accepts a comma separated list of labels that are going to be presented as columns. Names are
case-sensitive. You can also use multiple flag options like -L label1 -L label2...
      --no-headers=false: When using the default or custom-column output format, don't print headers.
  -o, --output='': Output format. One of:
json|yaml|wide|name|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...
See custom columns [http://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns], golang template
[http://golang.org/pkg/text/template/#pkg-overview] and jsonpath template
[http://kubernetes.io/docs/user-guide/jsonpath].
      --output-version='': Output the formatted object with the given group version (for ex: 'extensions/v1beta1').
      --raw='': Raw URI to request from the server.  Uses the transport specified by the kubeconfig file.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
  -l, --selector='': Selector (label query) to filter on
  -a, --show-all=true: When printing, show all resources (false means hide terminated pods.)
      --show-kind=false: If present, list the resource type for the requested object(s).
      --show-labels=false: When printing, show all labels as the last column (default hide labels column)
      --sort-by='': If non-empty, sort list types using this field specification.  The field specification is expressed
as a JSONPath expression (e.g. '{.metadata.name}'). The field in the API resource specified by this JSONPath expression
must be an integer or a string.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
  -w, --watch=false: After listing/getting the requested object, watch for changes.
      --watch-only=false: Watch for changes to the requested object(s), without listing/getting first.

Use "oc options" for a list of global command-line options (applies to all commands).
```

### 可以get的资源类型
```
# oc get
You must specify the type of resource to get. Valid resource types include:
   * buildconfigs (aka 'bc')
   * builds
   * clusters (valid only for federation apiservers)
   * componentstatuses (aka 'cs')
   * configmaps (aka 'cm')
   * daemonsets (aka 'ds')
   * deployments (aka 'deploy')
   * deploymentconfigs (aka 'dc')
   * events (aka 'ev')
   * endpoints (aka 'ep')
   * horizontalpodautoscalers (aka 'hpa')
   * imagestreamimages (aka 'isimage')
   * imagestreams (aka 'is')
   * imagestreamtags (aka 'istag')
   * ingress (aka 'ing')
   * groups
   * jobs
   * limitranges (aka 'limits')
   * nodes (aka 'no')
   * namespaces (aka 'ns')
   * petsets (alpha feature, may be unstable)
   * pods (aka 'po')
   * persistentvolumes (aka 'pv')
   * persistentvolumeclaims (aka 'pvc')
   * policies
   * projects
   * quota
   * resourcequotas (aka 'quota')
   * replicasets (aka 'rs')
   * replicationcontrollers (aka 'rc')
   * rolebindings
   * routes
   * secrets
   * serviceaccounts (aka 'sa')
   * services (aka 'svc')
   * users
error: Required resource not specified.
Use "oc explain <resource>" for a detailed description of that resource (e.g. oc explain pods).
See 'oc get -h' for help and examples.
```

### demo
#### projects
显示所有的projects(比oc projects命令更加详细，还可以显示project的状态；但是没有显示出当前的project是哪个)

```
# oc get projects
NAME              DISPLAY NAME    STATUS
...
spark-cluster                     Active
...
test              test            Active
```

#### users
显示所有的users

```
# oc get users
NAME            UID                                    FULL NAME   IDENTITIES
...
frank123.deve   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx               myhtp:frank123.deve
...
```


#### pods
列出所有的pods

```
# oc get pods
NAME                            READY     STATUS             RESTARTS   AGE
mysql-1-deploy                  0/1       Error              0          52m
spark-master-controller-vsm2t   1/1       Running            1          4d
```

#### services
列出所有的services

```
# oc get services
NAME           CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
mysql          172.30.12.118    <none>        3306/TCP   55m
spark-master   172.30.45.71     <none>        7077/TCP   7d
```

#### serviceaccounts
列出所有的serviceaccounts  

```
# oc get serviceaccounts
NAME       SECRETS   AGE
builder    2         7d
default    2         7d
deployer   2         7d
```




## describe        
Show details of a specific resource or group of resources

### usage
```

```

### demo
查看名为deployer的serviceaccounts  

```
# oc describe serviceaccounts deployer
Name:		deployer
Namespace:	spark-cluster
Labels:		<none>

Image pull secrets:	deployer-dockercfg-xxxxx

Mountable secrets: 	deployer-dockercfg-xxxxx
                   	deployer-token-xxxxx

Tokens:            	deployer-token-xxxxx
                   	deployer-token-xxxxx
```                   	




## edit            
Edit a resource on the server

### usage
```

```

### demo



## set             
Commands that help set specific features on objects

### usage
```

```

### demo



## label           
Update the labels on a resource

### usage
```

```

### demo



## annotate        
Update the annotations on a resource

### usage
```

```

### demo



## expose          
Expose a replicated application as a service or route

### usage
```

```

### demo



## delete          
Delete one or more resources，删除资源

### usage
```
# oc help delete
Delete a resource

JSON and YAML formats are accepted.

If both a filename and command line arguments are passed, the command line arguments are used and the filename is
ignored.

Note that the delete command does NOT do resource version checks, so if someone submits an update to a resource right
when you submit a delete, their update will be lost along with the rest of the resource.

Usage:
  oc delete ([-f FILENAME] | TYPE [(NAME | -l label | --all)]) [options]

Examples:
  # Delete a pod using the type and ID specified in pod.json.
  oc delete -f pod.json

  # Delete a pod based on the type and ID in the JSON passed into stdin.
  cat pod.json | oc delete -f -

  # Delete pods and services with label name=myLabel.
  oc delete pods,services -l name=myLabel

  # Delete a pod with name node-1-vsjnm.
  oc delete pod node-1-vsjnm

  # Delete all resources associated with a running app, includes
  # buildconfig,deploymentconfig,service,imagestream,route and pod,
  # where 'appName' is listed in 'Labels' of 'oc describe [resource] [resource name]' output.
  oc delete all -l app=appName

  # Delete all pods
  oc delete pods --all

Options:
      --all=false: [-all] to select all the specified resources.
      --cascade=true: If true, cascade the deletion of the resources managed by this resource (e.g. Pods created by a
ReplicationController).  Default true.
  -f, --filename=[]: Filename, directory, or URL to a file containing the resource to delete.
      --grace-period=-1: Period of time in seconds given to the resource to terminate gracefully. Ignored if negative.
      --ignore-not-found=false: Treat "resource not found" as a successful delete. Defaults to "true" when --all is
specified.
      --include-extended-apis=true: If true, include definitions of new APIs via calls to the API server. [default true]
      --now=false: If true, resources are force terminated without graceful deletion (same as --grace-period=0).
  -o, --output='': Output mode. Use "-o name" for shorter output (resource/name).
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
  -l, --selector='': Selector (label query) to filter on.
      --timeout=0s: The length of time to wait before giving up on a delete, zero means determine a timeout from the
size of the object

Use "oc options" for a list of global command-line options (applies to all commands).
```

### resource类型
```
# oc delete
error: You must provide one or more resources by argument or filename.
Example resource specifications include:
   '-f rsrc.yaml'
   '--filename=rsrc.json'
   'pods my-pod'
   'services'
```   

### demo
删除名为'mysql-1-deploy'的pod

```
# oc delete pod mysql-1-deploy
pod "mysql-1-deploy" deleted
```


删除名为mysql的service(在OpenShift的Overview页面中，可以看到的就是service)

```
# oc delete service mysql
service "mysql" deleted
```


删除label中db=mysql的所有资源，包括buildconfig,deploymentconfig,service,imagestream,route and pod,

```
# oc delete all -l db=mysql
imagestream "mysql" deleted
deploymentconfig "mysql" deleted
```




## scale           
Change the number of pods in a deployment

### usage
```

```

### demo



## autoscale       
Autoscale a deployment config, deployment, replication controller, or replica set

### usage
```

```

### demo



## secrets         
Manage secrets

### usage
```

```

### demo



## serviceaccounts 
Manage service accounts in your project

### usage
```
# oc help serviceaccounts
Manage service accounts in your project

Service accounts allow system components to access the API.

Aliases:
serviceaccounts, sa

Usage:
  oc serviceaccounts [options]

Available Commands:
  get-token   Get a token assigned to a service account.
  new-token   Generate a new token for a service account.

Use "oc <command> --help" for more information about a given command.
Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo




# Troubleshooting and Debugging Commands
## logs            
Print the logs for a resource

### usage
```

```

### demo



## rsh             
Start a shell session in a pod

### usage
```

```

### demo



## rsync           
Copy files between local filesystem and a pod

### usage
```

```

### demo



## port-forward    
Forward one or more local ports to a pod

### usage
```

```

### demo



## debug           
Launch a new instance of a pod for debugging

### usage
```

```

### demo



## exec            
Execute a command in a container

### usage
```

```

### demo



## proxy           
Run a proxy to the Kubernetes API server

### usage
```

```

### demo



## attach          
Attach to a running container

### usage
```

```

### demo



## run             
Run a particular image on the cluster

### usage
```

```

### demo




# Advanced Commands
## adm             
Tools for managing a cluster

### usage
```

```

### demo



## create          
Create a resource by filename or stdin

### usage
```

```

### demo



## replace         
Replace a resource by filename or stdin

### usage
```

```

### demo



## apply           
Apply a configuration to a resource by filename or stdin

### usage
```

```

### demo



## patch           
Update field(s) of a resource using strategic merge patch

### usage
```

```

### demo



## process         
Process a template into list of resources

### usage
```

```

### demo



## export          
Export resources so they can be used elsewhere

### usage
```

```

### demo



## extract         
Extract secrets or config maps to disk

### usage
```

```

### demo



## observe         
Observe changes to resources and react to them (experimental)

### usage
```

```

### demo



## policy          
Manage authorization policy，管理认证策略。

### usage
```
# oc help policy
Manage authorization policy

Usage:
  oc policy [options]

Available Commands:
  add-role-to-group      Add a role to groups for the current project
  add-role-to-user       Add a role to users or serviceaccounts for the current project
  can-i                  Check whether an action is allowed
  remove-group           Remove group from the current project
  remove-role-from-group Remove a role from groups for the current project
  remove-role-from-user  Remove a role from users for the current project
  remove-user            Remove user from the current project
  who-can                List who can perform the specified action on a resource

Use "oc <command> --help" for more information about a given command.
Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo



## convert         
Convert config files between different API versions

### usage
```

```

### demo



## import          
Commands that import applications

### usage
```

```

### demo




# Settings Commands
## logout          
End the current server session

### usage
```
# oc help logout
Log out of the active session out by clearing saved tokens

An authentication token is stored in the config file after login - this command will delete that token on the server,
and then remove the token from the configuration file.

If you are using an alternative authentication method like Kerberos or client certificates, your ticket or client
certificate will not be removed from the current system since these are typically managed by other programs. Instead,
you can delete your config file to remove the local copy of that certificate or the record of your server login.

After logging out, if you want to log back into the server use 'oc login'.

Usage:
  oc logout [options]

Examples:
  # Logout
  oc logout

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
```
# oc whoami -c
spark-cluster/xxx-xxx-xxx-xxx:xxxx/frank.green
# oc logout
Logged "yuancong.deng" out on "https://xxx-xxx-xxx-xxx:xxxx"
# oc whoami -c
spark-cluster/xxx-xxx-xxx-xxx:xxxx/frank.green
# oc get nodes
No resources found.
Error from server: User "system:anonymous" cannot list all nodes in the cluster
```

经测试发现： 使用logout退出登录后，没有权限进行集群的相关操作了；但是使用 **oc whoami -c** 命令还是可以看到当前的用户。


## config          
Change configuration files for the client

### usage
```

```

### demo



## whoami          
Return information about the current session，显示当前会话的信息。

### usage
```
# oc help whoami
Show information about the current session

The default options for this command will return the currently authenticated user name or an empty string.  Other flags
support returning the currently used token or the user context.

Usage:
  oc whoami [options]

Options:
  -c, --show-context=false: Print the current user context name
      --show-server=false: Print the current server's REST API URL
  -t, --show-token=false: Print the token the current session is using. This will return an error if you are using a
different form of authentication.

Use "oc options" for a list of global command-line options (applies to all commands).
```

### demo
显示当前用户名

```
# oc whoami
system:admin
```

显示当前会话的上下文信息

```
# oc whoami -c
spark-cluster/xxx-xxx-xxx-xxx:xxx/system:admin
```








## completion      
Output shell completion code for the given shell (bash or zsh)

### usage
```

```

### demo


























