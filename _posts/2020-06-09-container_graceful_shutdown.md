---
title: Container Graceful Shutdown
description: "세련되게 살자"
layout: post
categories: [Python, Container, stopsignal, Docker, SIGTERM]
---

## 필요한 이유

- 롱트랜잭션 실행 중일 때 shutdown 한다면?
- 서비스 업데이트 등의 상황으로 k8s가 pod 종료 시도할 때
- pod가 처리 중인 상태에서 강제로 kill 될 가능성 농후

### 1안) SIGTERM에 대한 처리 구현

#### Python Conatiner

- signal trap으로 구현

#### RESTful API Contaner

- Supervisord  설정
  
  ```ini
  stopsignal=HUP
  stopwaitsecs=10
  ```

- uWSGI
  
  - 뭔짓을 해도 python에서 trap을 하지 못한다
  - 그나마 graceful하게 reload은 한다

#### 시나리오1

1. docker stop하면 
2. Supervisord에서 HUP 보내고
3. uWSGI는 graceful reload (이뭐병)
4. (결과적으로 uWSGI랑 상관없이) Supervisord는 10초 기다렸다 kill all
5. 아직 안 죽었으면 docker는 time 기다리고 kill

#### 시나리오2

- 그냥 K8s에서 `terminationGracePeriodSeconds`을 길게 준다

#### Signal(IPC)

- [SIGINT SIGTERM SIGKILL SIGSTOP](https://www.quora.com/What-is-the-difference-between-the-SIGINT-and-SIGTERM-signals-in-Linux-What%E2%80%99s-the-difference-between-the-SIGKILL-and-SIGSTOP-signals)
- [Signal (IPC)](https://en.wikipedia.org/wiki/Signal_(IPC))

| signal    | can be caught or ignored |                    | 내용                                                                                                               |
| --------- |:------------------------:| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `SIGINT`  | O                        | interrupt signal   | **ctrl-c**. to provide a mechanism for an orderly, **graceful shutdown**. "user-initiated **happy** termination" |
| `SIGTERM` | O                        | termination signal | to kill the process, **gracefully** or not, but to first allow it a chance to cleanup.                           |
| `SIGKILL` | X                        | kill signal        | 프로세스 **즉시** 죽임!! 최후의 수단!!                                                                                        |
| `SIGQUIT` | O                        | dump core signal   | **ctrl-\\**. to provide a mechanism for the user to abort the process. "user-initiated **unhappy** termination"  |
| SIGHUP    |                          | Terminate          |                                                                                                                  |
| `SIGSTOP` | X                        | pause signal       | resuming via `SIGCONT`                                                                                           |
| SIGCHLD   |                          |                    | Child process terminated, stopped, or continued                                                                  |
| SIGWINCH  |                          |                    |                                                                                                                  |

#### Python에서 처리

- [Python에서 처리: signal — Set handlers for asynchronous events](https://docs.python.org/3.7/library/signal.html)
- https://codeday.me/ko/qa/20190529/660372.html (Python 2.X)
- https://code-examples.net/ko/docs/python~3.7/library/signal
- http://blog.kichul.co.kr/2018/01/12/python%EC%97%90%EC%84%9C-signal-%EC%B2%98%EB%A6%AC/

#### uWSGI에서 처리

- [Configuring uWSGI for Production Deployment](https://www.techatbloomberg.com/blog/configuring-uwsgi-production-deployment/)
  
  - 아래 설정 절대 안 먹는다. 해도 python에서 signal trap 안된다.
    
    ```ini
    py-call-osafterfork = true
    ```
  
  - 하긴 먹어도 쓸데가 없다

- [Signals for controlling uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/Management.html#signals-for-controlling-uwsgi)
  
  - graceful하게 shutdown하는게 **없다!!** 나머지는 그냥 immediately kill 해버린다
    - SIGHUP이 그나마 graceful 한데 reload를 해버린다
    - 얼씨구 Windows는 SIGHUP이 없다

| Signal  | Description                                                  | Convenience command                                                           |
| ------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| SIGHUP  | **gracefully reload** all the workers and the master process | `--reload`                                                                    |
| SIGTERM | **brutally reload** all the workers and the master process   | (use `--die-on-term` to respect the convention of shutting down the instance) |
| SIGINT  | **immediately** kill the entire uWSGI stack                  | `--stop`                                                                      |
| SIGQUIT | **immediately** kill the entire uWSGI stack                  |                                                                               |

#### Supervisord에서 처리

- https://serverfault.com/questions/386319/is-supervisord-shutting-down-gracefully
  - 야간데...
  - `stopsignal`
    - The signal used to kill the program when a stop is requested.  This can be any of TERM, HUP, INT, QUIT, KILL, USR1, or USR2.
    - *Default*: TERM
    - *Required*:  No.
  - `stopwaitsecs`
    - The number of seconds to wait for the OS to return a SIGCHLD to **supervisord** after the program has been sent a stopsignal. If this number of seconds elapses before **supervisord** receives a SIGCHLD from the process, **supervisord** will attempt to kill it with a final SIGKILL.
    - *Default*: 10
    - *Required*:  No.

#### Docker에서 처리

- [Gracefully Stopping Docker Containers](https://www.ctl.io/developers/blog/post/gracefully-stopping-docker-containers/)
- https://codeday.me/ko/qa/20190529/660372.html

#### K8s에서 처리

- https://pracucci.com/graceful-shutdown-of-kubernetes-pods.html
- [Kubernetes: Termination of pods](http://kubernetes.io/docs/user-guide/pods/#termination-of-pods)
- [Kubernetes: Pods lifecycle hooks and termination notice](http://kubernetes.io/docs/user-guide/production-pods/#lifecycle-hooks-and-termination-notice)
- [Kubernetes: Container lifecycle hooks](http://kubernetes.io/docs/user-guide/container-environment/)
- [kubernetes를 이용한 서비스 무중단 배포](https://tech.kakao.com/2018/12/24/kubernetes-deploy/)
  - terminationGracePeriodSeconds 

### 2안) 재처리

### 3안) 운영 프로세스로 해결

shutdown 필요할 시

1. request 더이상 발생 안되게 조치 하고 
2. 충분한 시간 경과 후 (request 처리 중이던 pod가 처리를 모두 마친 후)
3. shutdown 진행

### python signal trap 예

```python
app = flask.Blueprint('app', __name__)

# Graceful Shutdown (signal 처리) 구현
imBusy = []
def graceful_shutdown_handler(signum = None, frame = None):
    logging.info("I am dying.. [%s]" % signum)
    logging.debug("working [%s]" % imBusy)

    while len(imBusy) > 0:
        time.sleep(0.5)        

    logging.info("Good Bye")
    exit(0)

# signal 처리 등록
try:
    signals = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]
except:    
    # Windows에는 signal.SIGHUP 없음
    signals = [signal.SIGTERM, signal.SIGINT]

for sig in signals:
    signal.signal(sig, graceful_shutdown_handler) 

@app.before_app_request
def imbusy():
    global imBusy
    imBusy.append(threading.currentThread().name)

@app.after_app_request
def solong(res):
    global imBusy
    logging.debug("remove [%s]" % threading.currentThread().name)
    imBusy.remove(threading.currentThread().name)
    return res
```
