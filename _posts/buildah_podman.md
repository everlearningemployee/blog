[Buildah | buildah.io](https://buildah.io/)

[Buildah, Dive, Skopeo: 3 Container Tools for building images on Kubernetes Cluster, with Gitlab CI - YouTube](https://www.youtube.com/watch?v=aViKsSEGwOc)

# Ubuntu 18.04에 설치

```
multipass launch -n buildah -d 10G -m 10G 18.04
```

20.10 이상에서는 아무 조치 없이 apt install을 할 수 있다.

20.04에서는 이 방법도 안된다.

[How To Install Podman on Ubuntu - Linux Windows and android Tutorials - Linux (osradar.com)](https://www.osradar.com/how-to-install-podman-on-ubuntu/)

[Podman/Buildah toolchain in Ubuntu - DEV](https://dev.to/jj/podman-buildah-toolchain-in-ubuntu-5d2o)

```sh
apt update
apt install -y software-properties-common
add-apt-repository -y ppa:projectatomic/ppa
apt update
apt install -y buildah runc
```

```
git clone https://github.com/sds-arch-cert/kubeflow-edu.git
```

# Tutorial

[buildah/docs/tutorials at master · containers/buildah (github.com)](https://github.com/containers/buildah/tree/master/docs/tutorials)

| docker                                              | buildah & podman                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------ |
| docker ps                                           | buildah containers                                                 |
| docker images                                       | buildah images                                                     |
| docker build -f ./Dockerfile -t myimg/test:latest . | buildah bud --format=docker -f ./Dockerfile -t myimg/test:latest . |

buildah bud --format=docker -f ./Dockerfile.titanic -t myimg/test:latest .