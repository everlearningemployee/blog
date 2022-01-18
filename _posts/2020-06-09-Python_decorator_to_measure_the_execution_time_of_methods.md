---
title: Python 함수 실행시간 측정 decorator
description: "롱트랜잭션이 얼마나 걸리는지 맨날 물어보더라"
layout: post
categories: [Python]
toc: true
---

### 함수 실행시간 측정용 decorator 정의

```python
def exec_time(original_fn):
    @wraps(original_fn)
    def wrapper_fn(*args, **kwargs):
        int_ln = 70
        str_start = "== START [%s] ==" % (original_fn.__name__)
        int_s1 = int( (int_ln - len(str_start)) / 2 )
        int_s2 = int_ln - len(str_start) - int_s1
        print("\n" + "=" * int_s1 + str_start + "=" * int_s2)

        start_time = time.time()
        result = original_fn(*args, **kwargs)
        dt = time.time() - start_time

        str_end = "== END [%s]: working %.4f sec ==" % (original_fn.__name__, dt)
        int_e1 = int( (int_ln - len(str_end)) / 2 )
        int_e2 = int_ln - len(str_end) - int_e1
        print("=" * int_e1 + str_end + "=" * int_e2 + "\n")

        return result
    return wrapper_fn
```

### 사용 예

코드

```python
@exec_time
def hahahoho():
    … 생략 …
    logger.debug('long long time')
```

이 때 로그 출력은 다음과 같다

```
========================== START [hahahoho] ==========================
… 생략 …
[2019-07-15 05:05:35,166] DEBUG   long long time
================ END [hahahoho]: working 26.7614 sec =================
```
