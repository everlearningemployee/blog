---
title: 패키지관리자 설정파일 위치
description: 지금 알고 있는 걸 그때도 알았더라면
layout: post
categories: [Package, PyPI, npm, yarn, Dockerfile, Ubuntu, 폐쇠망]
toc: true
---

폐쇠망에서 Dockerizing할 때 요긴하게 참고하시라

\[꿀팁\] $HOME에 PVC 마운트하는 경우는 전체 사용자에게 적용되는 설정파일 위치를 사용하면 된다

## Ubuntu APT Repository

설정파일 위치

- `/etc/apt/sources.list.d/`

설정파일 샘플

```bash
# source.list
deb http://ubuntu.mirror.xxx.net/ubuntu bionic main restricted
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-updates main restricted
deb http://ubuntu.mirror.xxx.net/ubuntu bionic universe
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-updates universe
deb http://ubuntu.mirror.xxx.net/ubuntu bionic multiverse
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-updates multiverse
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-backports main restricted universe multiverse
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-security main restricted
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-security universe
deb http://ubuntu.mirror.xxx.net/ubuntu bionic-security multiverse
```

## PyPI Repository

설정파일 위치

- https://pip.pypa.io/en/stable/user_guide/#config-file
- 전체 사용자: `/etc/pip.conf`
- 개별 사용자:
  - Unix/MacOS: `${HOME}/.pip/pip.conf `
  - Windows: `%HOME%\pip\pip.ini`

설정파일 샘플

```
[global]
index-url = http://nexus.xxx.com/repository/pypi-remote/simple/
trusted-host = nexus.xxx.com
```

## npm Registry

설정파일 위치

- 전체 사용자: `/usr/etc/npmrc`
- 개별 사용자: `~/.npmrc`

설정파일 샘플

```ini
registry=http://nexus.xxx.net/repository/npm/
```

## yarn Registry

설정파일 위치

- 전체 사용자: `/usr/etc/yarnrc`
- 개별 사용자: `~/.yarnrc`

설정파일 샘플

```
registry "http://nexus.xxx.net:8081/artifactory/api/npm/npm"
```

## 기타1) Docker Registry

설정파일 위치

- `${DOCKER_CONFIG}/config.json`
- 일반적으로  `~/config.json`
- 전체 사용자 적용 위치는 없음

설정파일 샘플

```json
{
       "auths": {
                "yyy.xxx.net": {
                        "auth": "THisISASaMplECOnFIgfilEWow=="
                }
        },
        "HttpHeaders": {
                "User-Agent": "Docker-Client/19.03.5 (linux)"
        }
}
```

## 기타2) .bashrc

설정파일 위치

- 전체 사용자:
  - Debian-based Linux: `/etc/bash.bashrc`
  - Redhat, Fedora: `/etc/bashrc`
  - Suse, OpenSuse,: `/etc/bash.bashrc.local`
- 개별 사용자: `~/.bashrc`
