# kubectl
kubectl是Kubernetes集群的管理工具.


查看命令选项

```
$ kubectl
kubectl controls the Kubernetes cluster manager.

Find more information at https://github.com/kubernetes/kubernetes.

Basic Commands (Beginner):
  create         Create a resource by filename or stdin
  expose         Take a replication controller, service, deployment or pod and expose it as a new Kubernetes Service
  run            Run a particular image on the cluster
  set            Set specific features on objects

Basic Commands (Intermediate):
  get            Display one or many resources
  explain        Documentation of resources
  edit           Edit a resource on the server
  delete         Delete resources by filenames, stdin, resources and names, or by resources and label selector

Deploy Commands:
  rollout        Manage a deployment rollout
  rolling-update Perform a rolling update of the given ReplicationController
  scale          Set a new size for a Deployment, ReplicaSet, Replication Controller, or Job
  autoscale      Auto-scale a Deployment, ReplicaSet, or ReplicationController

Cluster Management Commands:
  certificate    Modify certificate resources.
  cluster-info   Display cluster info
  top            Display Resource (CPU/Memory/Storage) usage
  cordon         Mark node as unschedulable
  uncordon       Mark node as schedulable
  drain          Drain node in preparation for maintenance
  taint          Update the taints on one or more nodes

Troubleshooting and Debugging Commands:
  describe       Show details of a specific resource or group of resources
  logs           Print the logs for a container in a pod
  attach         Attach to a running container
  exec           Execute a command in a container
  port-forward   Forward one or more local ports to a pod
  proxy          Run a proxy to the Kubernetes API server
  cp             Copy files and directories to and from containers.

Advanced Commands:
  apply          Apply a configuration to a resource by filename or stdin
  patch          Update field(s) of a resource using strategic merge patch
  replace        Replace a resource by filename or stdin
  convert        Convert config files between different API versions

Settings Commands:
  label          Update the labels on a resource
  annotate       Update the annotations on a resource
  completion     Output shell completion code for the given shell (bash or zsh)

Other Commands:
  api-versions   Print the supported API versions on the server, in the form of "group/version"
  config         Modify kubeconfig files
  help           Help about any command
  version        Print the client and server version information

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
```





# Basic Commands (Beginner):
## create         
Create a resource by filename or stdin
### usage


### demo



## expose         
Take a replication controller, service, deployment or pod and expose it as a new Kubernetes Service
### usage


### demo



## run            
Run a particular image on the cluster
### usage


### demo



## set            
Set specific features on objects
### usage


### demo



# Basic Commands (Intermediate):
## get            
Display one or many resources
### usage


### demo



## explain        
Documentation of resources
### usage


### demo



## edit           
Edit a resource on the server
### usage


### demo



## delete         
Delete resources by filenames, stdin, resources and names, or by resources and label selector
### usage


### demo



# Deploy Commands:
## rollout        
Manage a deployment rollout
### usage


### demo



## rolling-update 
Perform a rolling update of the given ReplicationController
### usage


### demo



## scale          
Set a new size for a Deployment, ReplicaSet, Replication Controller, or Job
### usage


### demo



## autoscale      
Auto-scale a Deployment, ReplicaSet, or ReplicationController
### usage


### demo



# Cluster Management Commands:
## certificate    
Modify certificate resources.
### usage


### demo



## cluster-info   
Display cluster info.

### usage
```
$ kubectl help cluster-info
Display addresses of the master and services with label kubernetes.io/cluster-service=true To further debug and diagnose
cluster problems, use 'kubectl cluster-info dump'.

Aliases:
cluster-info, clusterinfo

Available Commands:
  dump        Dump lots of relevant info for debugging and diagnosis

Options:
      --include-extended-apis=true: If true, include definitions of new APIs via calls to the API server. [default true]

Usage:
  kubectl cluster-info [options]
```  



### demo



## top            
Display Resource (CPU/Memory/Storage) usage
### usage


### demo



## cordon         
Mark node as unschedulable
### usage


### demo



## uncordon       
Mark node as schedulable
### usage


### demo



## drain          
Drain node in preparation for maintenance
### usage


### demo



## taint          
Update the taints on one or more nodes
### usage


### demo



# Troubleshooting and Debugging Commands:
## describe       
Show details of a specific resource or group of resources
### usage


### demo



## logs           
Print the logs for a container in a pod
### usage


### demo



## attach         
Attach to a running container
### usage


### demo



## exec           
Execute a command in a container
### usage


### demo



## port-forward   
Forward one or more local ports to a pod
### usage


### demo



## proxy          
Run a proxy to the Kubernetes API server
### usage


### demo



## cp             
Copy files and directories to and from containers.
### usage


### demo



# Advanced Commands:
## apply          
Apply a configuration to a resource by filename or stdin
### usage


### demo



## patch          
Update field(s) of a resource using strategic merge patch
### usage


### demo



## replace        
Replace a resource by filename or stdin
### usage


### demo



## convert        
Convert config files between different API versions
### usage


### demo



# Settings Commands:
## label          
Update the labels on a resource
### usage


### demo



## annotate       
Update the annotations on a resource
### usage


### demo



## completion     
Output shell completion code for the given shell (bash or zsh)
### usage


### demo



# Other Commands:
## api-versions   
Print the supported API versions on the server, in the form of "group/version"

## config         
Modify kubeconfig files
### usage


### demo



## help           
Help about any command

查看子命令帮助，比如查看create命令的帮助:  

```
$ kubectl create --help
Create a resource by filename or stdin.

JSON and YAML formats are accepted.

Examples:
  # Create a pod using the data in pod.json.
  kubectl create -f ./pod.json

  # Create a pod based on the JSON passed into stdin.
  cat pod.json | kubectl create -f -

  # Edit the data in docker-registry.yaml in JSON using the v1 API format then create the resource using the edited
data.
  kubectl create -f docker-registry.yaml --edit --output-version=v1 -o json

Available Commands:
  configmap      Create a configmap from a local file, directory or literal value
  deployment     Create a deployment with the specified name.
  namespace      Create a namespace with the specified name
  quota          Create a quota with the specified name.
  secret         Create a secret using specified subcommand
  service        Create a service using specified subcommand.
  serviceaccount Create a service account with the specified name

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --edit=false: Edit the API resource before creating
  -f, --filename=[]: Filename, directory, or URL to files to use to create the resource
      --include-extended-apis=true: If true, include definitions of new APIs via calls to the API server. [default true]
      --no-headers=false: When using the default or custom-column output format, don't print headers.
  -o, --output='': Output format. One of:
json|yaml|wide|name|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...
See custom columns [http://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns], golang template
[http://golang.org/pkg/text/template/#pkg-overview] and jsonpath template
[http://kubernetes.io/docs/user-guide/jsonpath].
      --output-version='': Output the formatted object with the given group version (for ex: 'extensions/v1beta1').
      --record=false: Record current kubectl command in the resource annotation. If set to false, do not record the
command. If set to true, record the command. If not set, default to updating the existing annotation value only if one
already exists.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
      --save-config=false: If true, the configuration of current object will be saved in its annotation. This is useful
when you want to perform kubectl apply on this object in the future.
      --schema-cache-dir='~/.kube/schema': If non-empty, load/store cached API schemas in this directory, default is
'$HOME/.kube/schema'
  -a, --show-all=false: When printing, show all resources (default hide terminated pods.)
      --show-labels=false: When printing, show all labels as the last column (default hide labels column)
      --sort-by='': If non-empty, sort list types using this field specification.  The field specification is expressed
as a JSONPath expression (e.g. '{.metadata.name}'). The field in the API resource specified by this JSONPath expression
must be an integer or a string.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --validate=true: If true, use a schema to validate the input before sending it
      --windows-line-endings=false: Only relevant if --edit=true. Use Windows line-endings (default Unix line-endings)

Usage:
  kubectl create -f FILENAME [options]
```


## version        
Print the client and server version information.


查看工具版本

```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"5", GitVersion:"v1.5.2", GitCommit:"c55cf2b7d8bfeb947f77453415d775d7f71c89c2", GitTreeState:"clean", BuildDate:"2017-03-07T00:03:00Z", GoVersion:"go1.7.4", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"5", GitVersion:"v1.5.2", GitCommit:"c55cf2b7d8bfeb947f77453415d775d7f71c89c2", GitTreeState:"clean", BuildDate:"2017-03-07T00:03:00Z", GoVersion:"go1.7.4", Compiler:"gc", Platform:"linux/amd64"}
```


# global cli options

```
$ kubectl options
The following options can be passed to any command:

      --allow-verification-with-non-compliant-keys=false: Allow a SignatureVerifier to use keys which are technically
non-compliant with RFC6962.
      --alsologtostderr=false: log to standard error as well as files
      --api-version='': DEPRECATED: The API version to use when talking to the server
      --application-metrics-count-limit=100: Max number of application metrics to store (per container)
      --as='': Username to impersonate for the operation
      --azure-container-registry-config='': Path to the file container Azure container registry configuration
information.
      --boot-id-file='/proc/sys/kernel/random/boot_id': Comma-separated list of files to check for boot-id. Use the
first one that exists.
      --certificate-authority='': Path to a cert. file for the certificate authority
      --client-certificate='': Path to a client certificate file for TLS
      --client-key='': Path to a client key file for TLS
      --cluster='': The name of the kubeconfig cluster to use
      --container-hints='/etc/cadvisor/container_hints.json': location of the container hints file
      --context='': The name of the kubeconfig context to use
      --docker='unix:///var/run/docker.sock': docker endpoint
      --docker-env-metadata-whitelist='': a comma-separated list of environment variable keys that needs to be collected
for docker containers
      --docker-only=false: Only report docker containers in addition to root stats
      --docker-root='/var/lib/docker': DEPRECATED: docker root is read from docker info (this is a fallback, default:
/var/lib/docker)
      --enable-load-reader=false: Whether to enable cpu load reader
      --event-storage-age-limit='default=0': Max length of time for which to store events (per type). Value is a comma
separated list of key values, where the keys are event types (e.g.: creation, oom) or "default" and the value is a
duration. Default is applied to all non-specified event types
      --event-storage-event-limit='default=0': Max number of events to store (per type). Value is a comma separated list
of key values, where the keys are event types (e.g.: creation, oom) or "default" and the value is an integer. Default is
applied to all non-specified event types
      --global-housekeeping-interval=1m0s: Interval between global housekeepings
      --google-json-key='': The Google Cloud Platform Service Account JSON Key to use for authentication.
      --housekeeping-interval=10s: Interval between container housekeepings
      --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity. This will
make your HTTPS connections insecure
      --ir-data-source='influxdb': Data source used by InitialResources. Supported options: influxdb, gcm.
      --ir-dbname='k8s': InfluxDB database name which contains metrics required by InitialResources
      --ir-hawkular='': Hawkular configuration URL
      --ir-influxdb-host='localhost:8080/api/v1/proxy/namespaces/kube-system/services/monitoring-influxdb:api': Address
of InfluxDB which contains metrics required by InitialResources
      --ir-namespace-only=false: Whether the estimation should be made only based on data from the same namespace.
      --ir-password='root': Password used for connecting to InfluxDB
      --ir-percentile=90: Which percentile of samples should InitialResources use when estimating resources. For
experiment purposes.
      --ir-user='root': User used for connecting to InfluxDB
      --kubeconfig='': Path to the kubeconfig file to use for CLI requests.
      --log-backtrace-at=:0: when logging hits line file:N, emit a stack trace
      --log-cadvisor-usage=false: Whether to log the usage of the cAdvisor container
      --log-dir='': If non-empty, write log files in this directory
      --log-flush-frequency=5s: Maximum number of seconds between log flushes
      --logtostderr=true: log to standard error instead of files
      --machine-id-file='/etc/machine-id,/var/lib/dbus/machine-id': Comma-separated list of files to check for
machine-id. Use the first one that exists.
      --match-server-version=false: Require server version to match client version
  -n, --namespace='': If present, the namespace scope for this CLI request
      --password='': Password for basic authentication to the API server
      --request-timeout='0': The length of time to wait before giving up on a single server request. Non-zero values
should contain a corresponding time unit (e.g. 1s, 2m, 3h). A value of zero means don't timeout requests.
  -s, --server='': The address and port of the Kubernetes API server
      --stderrthreshold=2: logs at or above this threshold go to stderr
      --storage-driver-buffer-duration=1m0s: Writes in the storage driver will be buffered for this duration, and
committed to the non memory backends as a single transaction
      --storage-driver-db='cadvisor': database name
      --storage-driver-host='localhost:8086': database host:port
      --storage-driver-password='root': database password
      --storage-driver-secure=false: use secure connection with database
      --storage-driver-table='stats': table name
      --storage-driver-user='root': database username
      --token='': Bearer token for authentication to the API server
      --user='': The name of the kubeconfig user to use
      --username='': Username for basic authentication to the API server
  -v, --v=0: log level for V logs
      --version=false: Print version information and quit
      --vmodule=: comma-separated list of pattern=N settings for file-filtered logging
```      















































