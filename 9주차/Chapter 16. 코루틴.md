# Chapter 16. 코루틴

-------

## 16.2 코루틴으로 사용되는 제너레이터의 기본 동작

```python
>>> def simple_coroutine(): #
... print('-> coroutine started')
... x = yield #
... print('-> coroutine received:', x)
...
>>> my_coro = simple_coroutine()
>>> my_coro #
<generator object simple_coroutine at 0x100c2be10>
>>> next(my_coro) #
-> coroutine started
>>> my_coro.send(42) #
-> coroutine received: 42
Traceback (most recent call last): #
 ...
StopIteration
```

코루틴은 자신의 본체 안에 yield 문을 가진 일종의 제너레이터 함수로 정의된다. 단지 호출자에서 데이터를 받도록 설계하면 yield는 값을 생성하지 않는다. yield 키워드 뒤에 아무런 표현식이 없을 때 값을 생성하지 않으려는 의도를 암묵적으로 표현한다. yield문을 한 번 이상 호출하는 코드를 보면, 코루틴의 동작을 좀 더 명확히 이해 가능하다.

```python
>>> def simple_coro2(a):
... print('-> Started: a =', a)
... b = yield a
... print('-> Received: b =', b)
... c = yield a + b
... print('-> Received: c =', c)
...
>>> my_coro2 = simple_coro2(14)
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(my_coro2)
'GEN_CREATED'
>>> next(my_coro2)
-> Started: a = 14
14
>>> getgeneratorstate(my_coro2)
'GEN_SUSPENDED'
>>> my_coro2.send(28)
-> Received: b = 28
42
>>> my_coro2.send(99)
-> Received: c = 99
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
StopIteration
>>> getgeneratorstate(my_coro2)
'GEN_CLOSED'
```

코루틴 실행은 yield 키워드에서 중단됨에 주목해야한다. 앞에서 설명한 것처럼 할당문에서는 실제 값을 할당하기 전에 = 오른쪽 코드를 실행한다. 



## 16.3 예제 : 이동 평균을 계산하는 코루틴

```python
def averager():
     total = 0.0
     count = 0
     average = None
     while True:
         term = yield average
         total += term
         count += 1
         average = total/count

```

코르틴을 사용하면 total 과 count를 지역 변수로 사용할 수 있다는 장점이 있다. 객체 속성이나 별도의 클로저 없이 평균을 구하는 데 필요한 값들을 유지할 수 있다. 



## 16.4 코루틴을 기동하기 위한 데커레이터

```python
from functools import wraps

def coroutine(func):
 """Decorator: primes `func` by advancing to first `yield`"""
     @wraps(func)
     def primer(*args,**kwargs):
         gen = func(*args,**kwargs)
         next(gen)
         return gen
     return primer

```

```python
"""
이동 평균을 계산하기 위한 코루틴
 >>> coro_avg = averager()
 >>> from inspect import getgeneratorstate
 >>> getgeneratorstate(coro_avg)
 'GEN_SUSPENDED'
 >>> coro_avg.send(10)
 10.0
 >>> coro_avg.send(30)
 20.0
 >>> coro_avg.send(5)
 15.0
"""
from coroutil import coroutine 

@coroutine
def averager():
     total = 0.0
     count = 0
     average = None
     while True:
         term = yield average
         total += term
         count += 1
         average = total/count

```

코루틴과 함께 사용하도록 설계된 특별 데커레이터를 제공하는 프레임워크가 많이 있지만, 이 프레임워크들이 모두 코루틴을 기동시키는 것은 아니다. 코루틴을 이벤트 루프에 연결하는 등 다른 서비스를 제공하는 프레임워크도 있다.



## 16.5 코루틴 종료와 예외 처리

```python
>>> from coroaverager1 import averager
>>> coro_avg = averager()
>>> coro_avg.send(40) #
40.0
>>> coro_avg.send(50)
45.0
>>> coro_avg.send('spam') #
Traceback (most recent call last):
 ...
TypeError: unsupported operand type(s) for +=: 'float' and 'str'
>>> coro_avg.send(60) #
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
StopIteration
```

코루틴의 total 변수에 더할 수 없는 'spam'이라는 문자열을 전송했으므로 에러가 발생했다.



## 16.7 yield from 사용하기

```python
from collections import namedtuple
Result = namedtuple('Result', 'count average')
# the subgenerator
def averager():
     total = 0.0
     count = 0
     average = None
     while True:
         term = yield
         if term is None:
             break
         total += term
         count += 1
         average = total/count
     return Result(count, average)

# the delegating generator
def grouper(results, key):
     while True:
         results[key] = yield from averager()
        
# the client code, a.k.a. the caller
def main(data):
     results = {}
     for key, values in data.items():
         group = grouper(results, key)
         next(group)
         for value in values:
             group.send(value)
         group.send(None) # important!
        
     # print(results) # uncomment to debug
     report(results)
    # output report
```

group.send(None)의 중요함을 강조한다. None을 전송해야 현재의 averager()객체가 종료되고 다음번 객체를 생성하게 된다.



## 16.8 yield from의 의미

유사코드

```python
_i = iter(EXPR)
try:
 _y = next(_i)
except StopIteration as _e:
 _r = _e.value
else:
 while 1:
 try:
 _s = yield _y
 except GeneratorExit as _e:
 try:
 _m = _i.close
 except AttributeError:
 pass
 else:
 _m()
 raise _e
 except BaseException as _e:
 _x = sys.exc_info()
 try:
 _m = _i.throw
 except AttributeError:
 raise _e
 else:
 try:
 _y = _m(*_x)
 except StopIteration as _e:
 _r = _e.value
 break
 else:
 try:
 if _s is None:
 _y = next(_i)
 else:
 _y = _i.send(_s)
 except StopIteration as _e:
 _r = _e.v
```

