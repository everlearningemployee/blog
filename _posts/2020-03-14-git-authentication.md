---
title: Git Authentication
description: "맨날 까먹지..."
layout: post
categories: [git]
---

- [GitHub Error: Authentication Failed from the Command Line](https://medium.com/@ginnyfahs/github-error-authentication-failed-from-command-line-3a545bfd0ca8)
  
  - 사용자 Settings > Developer settings > Personal access tokens 

- [Git pull/push 시 Password 물어보지 않도록 설정하기(credential.helper)](https://www.hahwul.com/2018/08/git-credential-helper.html)
  
  ```bash
  git config credential.helper store
  ```

- 변경 추적
  
  ```
  git config log.follow true
  ```

- 구찮지
  
  ```
  git config --global user.email "everlearningemployee@gmail.com"
  git config --global user.name "빨강달"
  ```
