# 설치

## Microk8s Kubeflow: 포기

1. Install MicroK8s with [Snap](https://snapcraft.io/) by running the following command:
   
   ```bash
   sudo snap install microk8s --classic
   # sudo snap install microk8s --classic --channel=1.18
   sudo iptables -P FORWARD ACCEPT
   ```
   
   ```bash
   sudo usermod -a -G microk8s $USER
   sudo chown -f -R $USER ~/.kube
   ```

```
sudo vi /etc/environment 
AUTHSERVICE_URL_PREFIX=/authservice/

sudo vi /etc/bash.bashrc
set -o vi
alias k='microk8s kubectl'
alias kubectl='microk8s kubectl'
```

```
sudo passwd $USER

su - $USER
```

2. Verify that MicroK8s is running:
   
   ```bash
   microk8s status --wait-ready
   ```

3. Having installed MicroK8s, you can now enable common services on your MicroK8s deployment. To do that, run the following command:
   
   ```bash
   microk8s enable dns dashboard storage
   ```
   
   **Optional:** To enable NVIDIA GPU hardware support, also run `microk8s enable gpu`.

4. Deploy Kubeflow by running this command:
   
   ```bash
   microk8s enable kubeflow
   ```

# Minikube Kubeflow

## Prerequisites

- Ubuntu 18 machine with min 8 cores, 16GB RAM, 250GB storage
- Root privileges on a Ubuntu machine

## Installation of Docker CE, kubectl, and Minikube

Minikube provides a no-driver mode based on Docker without requiring a hypervisor.

### Install Docker CE

Run the following commands to install Docker CE:

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```

```bash
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

sudo usermod -aG docker $USER && newgrp docker
```

### Install kubectl

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

```SHELL
sudo snap install kubectl --classic
```

### Install minikube

Run the command lines below to install the latest version of minikube. If you are looking for a specific version, refer to the [Kubernetes: minikube releases](https://github.com/kubernetes/minikube/releases) page.

```SHELL
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Start minikube

일반 계정으로 실행

```SHELL
sudo usermod -aG docker $USER && newgrp docker

minikube start \
  --driver=docker \
  --cpus 6 --memory 12288 --disk-size=120g \
  --extra-config=apiserver.service-account-issuer=api \
  --extra-config=apiserver.service-account-signing-key-file=/var/lib/minikube/certs/apiserver.key \
  --extra-config=apiserver.service-account-api-audiences=api 
```

## Installation of Kubeflow[ ](https://www.kubeflow.org/docs/started/workstation/minikube-linux/#installation-of-kubeflow)

1. Download the kfctl v1.1.0 release from the [Kubeflow releases page](https://github.com/kubeflow/kfctl/releases/).

2. Extract the zipped TAR file:
   
   ```SHELL
   # https://github.com/kubeflow/kfctl/releases/download/v1.1.0/kfctl_v1.1.0-0-g9a3621e_linux.tar.gz
   curl -LO {KFCTL_TAR_GZ_FILE_DOWNLOAD_LINK}
   tar -xvf {KFCTL_TAR_GZ_FILE}
   ```
   
   where `{KFCTL_TAR_GZ_FILE}` should be replaced with the name of the kfctl release file you have just downloaded.

3. Run the commands below to set up and deploy Kubeflow. One of them includes an optional command to add the binary kfctl to your path. If you don’t add the binary to your path, you must use the full path to the kfctl binary each time you run it.
   
   - **${KF_NAME}** - The name of your Kubeflow deployment. If you want a custom deployment name, specify that name here. For example, `my-kubeflow` or `kf-test`. The value of KF_NAME must consist of lower case alphanumeric characters or ‘-', and must start and end with an alphanumeric character. The value of this variable cannot be greater than 25 characters. It must contain just a name, not a directory path. This value also becomes the name of the directory where your Kubeflow configurations are stored, that is, the Kubeflow application directory.
   - **${KF_DIR}** - The full path to your Kubeflow application directory.

The following example installs Kubeflow v1.0.0 under the `/root/kubeflow/v1.0` directory:

```bash
export KFCTL_PATH=/home/red_suh/kubeflow
export BASE_DIR=$KFCTL_PATH
export KF_NAME=my-kubeflow

rm -rf $KFCTL_PATH
mkdir -p $KFCTL_PATH
export PATH=$PATH:$KFCTL_PATH

cd $KFCTL_PATH
wget https://github.com/kubeflow/kfctl/releases/download/v1.0/kfctl_v1.0-0-g94c35cf_linux.tar.gz
tar -xvf kfctl_v1.0-0-g94c35cf_linux.tar.gz        

export KF_DIR=${BASE_DIR}/${KF_NAME}
mkdir -p ${KF_DIR}
cd ${KF_DIR}

export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.1-branch/kfdef/kfctl_k8s_istio.v1.1.0.yaml" 
kfctl apply -V -f ${CONFIG_URI}
```

After the installation, run the following command to check whether all the pods are in running status:

```SHELL
kubectl get pod -n kubeflow
```

It may take a few minutes to reach full running status.

Expected output:

```
NAME                                                           READY   STATUS      RESTARTS   AGE
admission-webhook-bootstrap-stateful-set-0                     1/1     Running     0          10m
admission-webhook-deployment-64cb96ddbf-w7ptd                  1/1     Running     0        9m33s
application-controller-stateful-set-0                          1/1     Running     0          13m
argo-ui-778676df64-kjw6s                                       1/1     Running     0          10m
centraldashboard-7dd7dd685d-hvll8                              1/1     Running     0          10m
jupyter-web-app-deployment-89789fd5-cjkwf                      1/1     Running     0          10m
katib-controller-6b789b6cb5-kgzv8                              1/1     Running     1          10m
katib-db-manager-64f548b47c-sszv9                              1/1     Running     3        9m59s
katib-mysql-57884cb488-d4qt2                                   1/1     Running     0        9m59s
katib-ui-5c5cc6bd77-2kqvc                                      1/1     Running     0        9m59s
kfserving-controller-manager-0                                 2/2     Running     1          10m
metacontroller-0                                               1/1     Running     0          10m
metadata-db-76c9f78f77-7r8vb                                   0/1     Running     1          10m
metadata-deployment-674fdd976b-hzmzx                           0/1     Running     0          10m
metadata-envoy-deployment-5688989bd6-rqtrk                     1/1     Running     0          10m
metadata-grpc-deployment-5579bdc87b-xx9fk                      1/1     Running     6          10m
metadata-ui-9b8cd699d-scs9d                                    1/1     Running     0          10m
minio-755ff748b-lxsb6                                          1/1     Running     0        9m55s
ml-pipeline-79b4f85cbc-8tjff                                   1/1     Running     0        9m55s
ml-pipeline-ml-pipeline-visualizationserver-5fdffdc5bf-zsngc   1/1     Running     0        9m42s
ml-pipeline-persistenceagent-645cb66874-b465h                  1/1     Running     0        9m54s
ml-pipeline-scheduledworkflow-6c978b6b85-cffng                 1/1     Running     0        9m42s
ml-pipeline-ui-6995b7bccf-s642q                                1/1     Running     0        9m45s
ml-pipeline-viewer-controller-deployment-8554dc7b9f-vgw9r      1/1     Running     0        9m44s
mysql-598bc897dc-lsmqc                                         1/1     Running     0        9m54s
notebook-controller-deployment-7db57b9ccf-vw9vw                1/1     Running     0          10m
profiles-deployment-5d87dd4f87-7gfrj                           2/2     Running     0        9m41s
pytorch-operator-5fd5f94bdd-kfgvp                              1/1     Running     2          10m
seldon-controller-manager-679fc777cd-4n229                     1/1     Running     0        9m39s
spark-operatorcrd-cleanup-kxr7g                                0/2     Completed   0          10m
spark-operatorsparkoperator-c7b64b87f-cfptj                    1/1     Running     0          10m
spartakus-volunteer-6b767c8d6-4v6hc                            1/1     Running     0          10m
tensorboard-6544748d94-8ctk8                                   1/1     Running     0          10m
tf-job-operator-7d7c8fb8bb-xz5pw                               1/1     Running     1          10m
workflow-controller-945c84565-57c72                            1/1     Running     0          10m
```

## Launch of Kubeflow central dashboard

You can access the Kubeflow dashboard using the `istio-ingressgateway` service. To check your settings for `istio-ingressgateway`, execute the following commands:

```SHELL
export INGRESS_HOST=$(minikube ip)
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
```

Then you can access the Kubeflow dashboard in a web browser:

```SHELL
http://$INGRESS_HOST:$INGRESS_PORT
```

```
kubectl port-forward --address 0.0.0.0 -n kubernetes-dashboard service/kubernetes-dashboard 8181:80
```

```
watch 'microk8s kubectl get pod -A | grep -v Running'


microk8s kubectl get pod -A | grep -v Running
microk8s.kubectl logs -n kubeflow oidc-gatekeeper-697988b89f-bwgkk
```

```yaml
cat > /etc/netplan/50-cloud-init.yaml << EOF
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        eth0:
            dhcp4: no
            addresses:
                - 172.21.37.119/20
            gateway4: 172.21.32.1
            match:
                macaddress: 00:15:5d:a0:01:0d
            set-name: eth0
            nameservers:
                addresses:
                    - 8.8.8.8
                    - 8.8.4.4
    version: 2
EOF
netplan apply
```

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCdBLMXD3vy57pJ/hcDazM+hGMRwZfEKpSdrGSoB4CwXpu91S57LQuOOXtjc02il7gIuFWcOpNpii/HAhSd8or/edrBTCHibN5RquuGM8yhIVk6pbuL9VMCFTmVgqBCBqBdi/xZ95oIP5kkjZoC6KZYDCFc8i6LTCQ3JBag3+haHe73065T/aj1oJ2UyABsxj9AVwS08SHTnomcwu1RcEWYMIUVcdK5JqiXQ8LEkS027hy8mzFniL3zhHEAtFJ0ugS0pJQ/k9vs7bA/By535h7KnUUiitwTiD4rnBml12nQiyMjGmnQB4R6zI6GulUsDzrRULa/D5Fwn0VwTmlbi4IQzwIGerDF+jxdBNzud6g0NPKJDY7pH0UsuC/zfHeO7W0OzvS/j6Hoc6eHNQCSzG8G7Uu4dvvEZ00GiNB9SrKZ9DmcFcn58cvUfndr42AimbTvIqlR3B2FiI7QWghLUQgun0PwxRIzVLBVShf2e/1zdVHTKYy7GMgiRzg81ppPuDc= RedMoon@newbook
```
