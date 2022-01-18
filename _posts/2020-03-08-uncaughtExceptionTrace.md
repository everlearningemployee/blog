---
title: "Uncaught Exception Trace"
description: "언젠가 요긴할 것이다"
layout: post
categories: [python, exception]
---

# Uncaught Exception Trace

```python
import sys
import traceback

def exception_hook(type, value, tb):
    logging.error('=' * 80)
    logging.error(f'Type: {type}')
    logging.error(f'Value: {value}')
    t = traceback.format_exception(type, value, tb)
    t = [i.rstrip().split('\n') for i in t]
    for i in sum(t, []):
        logging.error(i)
    logging.error('-' * 80)

sys.excepthook = exception_hook

1 / 0
```

[전체 샘플 코드](https://gist.github.com/everlearningemployee/1746cd89615dfebed068345f5505d525)

익셉션 트레이스가 로그에 이렇게 찍힌다

```less
2020-03-08 17:51:52 ERROR ================================================================================
2020-03-08 17:51:52 ERROR Type: <class 'IndexError'>
2020-03-08 17:51:52 ERROR Value: tuple index out of range
2020-03-08 17:51:52 ERROR Traceback (most recent call last):
2020-03-08 17:51:52 ERROR   File "d:/temp/uncaughtExceptionTrace.py", line 59, in <module>
2020-03-08 17:51:52 ERROR     lumberjack()
2020-03-08 17:51:52 ERROR   File "d:/temp/uncaughtExceptionTrace.py", line 52, in lumberjack
2020-03-08 17:51:52 ERROR     bright_side_of_death()
2020-03-08 17:51:52 ERROR   File "d:/temp/uncaughtExceptionTrace.py", line 56, in bright_side_of_death
2020-03-08 17:51:52 ERROR     return tuple()[0]
2020-03-08 17:51:52 ERROR IndexError: tuple index out of range
2020-03-08 17:51:52 ERROR --------------------------------------------------------------------------------
```

- [Catching every single exception with Python](https://dev.to/joshuaschlichting/catching-every-single-exception-with-python-40o3) 
- [파이썬 공식 자습서 - 8. 에러와 예외](https://docs.python.org/ko/3/tutorial/errors.html#errors-and-exceptions)
- [파이썬을 이용한 전문적인 오류 처리](https://code.tutsplus.com/ko/tutorials/professional-error-handling-with-python--cms-25950)
