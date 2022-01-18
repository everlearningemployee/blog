---
title: Ubuntu에 Docker 설치
description: "CentOS보다 쉽다"
layout: post
categories: [docker, ubuntu]
---

출처: [How To Install Docker On Ubuntu 18.04 Bionic Beaver](https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04)

```bash
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $(whoami)
```
