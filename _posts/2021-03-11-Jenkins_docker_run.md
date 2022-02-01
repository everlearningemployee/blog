---
title: Docker로 Jenkins  실행
description: 해줄 사람이 없을 때도 있다
layout: post
image: https://www.jenkins.io/images/logos/jenkins/jenkins.svg
categories: [jenkins, docker, dind]
toc: false
---

#### 관련 Link

- [Docker (jenkins.io)](https://www.jenkins.io/doc/book/installing/docker/)
- [docker/README.md at master · jenkinsci/docker (github.com)](https://github.com/jenkinsci/docker/blob/master/README.md)
- [Plugin Manager CLI tool for Jenkins](https://github.com/jenkinsci/plugin-installation-manager-tool)

#### docker-compose.yaml

```yaml
version: "3"

services:

  jenkins-docker:
    image: docker:dind
    privileged: true
    ports:
      - "2376:2376"
    networks:
      jenkins-network:
        aliases: 
          - docker
    environment:
      - DOCKER_TLS_CERTDIR=/certs
    volumes:
      - jenkins-data:/var/jenkins_home
      - jenkins-docker-certs:/certs/client

  jenkins-worker:
    # image: myjenkins-blueocean:1.1 
    build: .
    ports:
      - "8080:8080"
      - "50000:50000"
    networks:
      jenkins-network:
    environment:
      - DOCKER_HOST=tcp://docker:2376
      - DOCKER_CERT_PATH=/certs/client
      - DOCKER_TLS_VERIFY=1
    volumes:
      - jenkins-data:/var/jenkins_home
      - jenkins-docker-certs:/certs/client:ro
    depends_on:
      - jenkins-docker

networks:
  jenkins-network:

volumes:
  jenkins-data:
  jenkins-docker-certs:
```

#### Dockerfile

```dockerfile
FROM jenkins/jenkins:2.263.4-lts-jdk11
USER root
RUN apt-get update && \
    apt-get install -y docker.io
USER jenkins
RUN jenkins-plugin-cli --plugins blueocean:1.24.4
```

#### 실행

```bash
docker-compose up -d; docker-compose logs -f
```