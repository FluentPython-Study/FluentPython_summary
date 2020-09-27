# Chap 7. 함수 데커레이터와 클로저

----------------



메타프로그래밍의 영역에 관한 이야기이다. 먼저 내부 함수를 가지지 않는 간단한 `@register` 데커레이터로 시작해서 두 단계의 내포된 함수를 가진 매개변수화된 `@clock()` 데커레이터까지 살펴본다.

- `등록 데커레이터`는 본질적으로 간단한 메커니즘이지만 고급 파이썬 프레임워크에서 실제 사용되고 있다. 6장에서 구현한 예제를 리팩토링해서 전략 디자인 패턴을 개선하기 위해 등록 개념을 적용했다. 

- `매개변수화된 데커레이터`는 거의 항상 최소 두 단계의 내포된 함수를 가지고 있으며, 더 고급 기법을 지원하는 데커레이터를 구현하기 위해 @functools.wraps를 사용하는 경우 세 간계 이상 내포되기도 한다.

그리고 표준 라이브러리의 functools 모듈에서 제공하는 `@lru_cache()`와 `@singledispatch` 등 두 개의 멋진 함수 데커레이터를 살펴본다.

데커레이터가 실제 작동하는 방식을 이해하려면, **임포트타임**과 **런타임**의 차이를 알아야 하며, 변수 범위, 클로저, 새로 소개된 nonlocal 선언에 대해서도 자세히 알아야 한다. 

- 클로저와 
- nonlocal을 

완전히 이해하면, 데커레이터를 만들 수 있을 뿐만 아니라, GUI 방식의 이벤트 주도 프로그램이나 콜백을 이용한 비동기 입출력을 구현할 때도 큰 도움이 된다.



## 7.1 데커레이터 기본 지식

```python
@decorate
def target():
	print('running target()')
```



## 7.2 파이썬이 데커레이터를 실행하는 시점

```python
registry = []
def register(func):
	print('running register(%s)' % func)
 	registry.append(func)
 	return func
@register
def f1():
 	print('running f1()')
@register
def f2():
 	print('running f2()')
def f3():
    print('running f3()')
def main():
 	print('running main()')
 	print('registry ->', registry)
 	f1()
 	f2()
 	f3()
    
if __name__=='__main__':
 	main() 
```

임포트타임과 런타임의 차이를 극명하게 보여준다. 데커레이터 함수가 데커레이트 되는 함수와 같은 모듈에 정의되어 있다. register() 데커레이터가 인수로 전달된 함수와 동일한 함수를 반환한다. 실제 코드에서 대부분의 데커레이터는 내부함수를 정의해서 반환한다.

## 7.3 데커레이터로 개선한 전략 패턴

```python
promos = []

def promotion(promo_func):
Decorator-enhanced Strategy pattern | 187
 	promos.append(promo_func)
 	return promo_func
@promotion
def fidelity(order):

 	return order.total() * .05 if order.customer.fidelity >= 1000 else 0
@promotion
def bulk_item(order):

 	discount = 0
 	for item in order.cart:
 	if item.quantity >= 20:
 	discount += item.total() * .1
 	return discount
@promotion
def large_order(order):

 	distinct_items = {item.product for item in order.cart}
 	if len(distinct_items) >= 10:
 	return order.total() * .07
 	return 0
def best_promo(order):

 	return max(promo(order) for promo in promos)
```

- promotion 전략 함수명이 특별한 형태로 되어있을 필요 없다
- `@promotion` 데커레이터는 데커레이트 된 함수의 목적을 명확히 알려준다.
- 재사용성이 좋다.



## 7.5 클로저

클로저 : 실제로 클로저는 함수 본체에서 정의하지 않고 참조하는 nonlocal 변수를 포함한 확장 범위를 가진 함수다. 함수가 익명 함수인지 여부는 중요하지 않다.

```python
def make_averager():
 	series = []
    
 	def averager(new_value):
 		series.append(new_value)
 		total = sum(series)
 		return total/len(series)
	return averager
```



## 7.7 간단한 데커레이터 구현하기

- 함수의 실행시간을 출력하는 간단한 데커레이터

```python
import time
def clock(func):
 	def clocked(*args): #
        t0 = time.perf_counter()
        result = func(*args) #
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
 	return clocked
```



- clock 데커레이터 사용

```python
import time
from clockdeco import clock

@clock
def snooze(seconds):
 	time.sleep(seconds)

@clock
def factorial(n):
 	return 1 if n < 2 else n*factorial(n-1)

if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

```



- 개선된 clock 데커레이터

```python
import time
import functools

def clock(func):
 	@functools.wraps(func)
 	def clocked(*args, **kwargs):
     	t0 = time.time()
     	result = func(*args, **kwargs)
     	elapsed = time.time() - t0
     	name = func.__name__
     	arg_lst = []
     	if args:
 			arg_lst.append(', '.join(repr(arg) for arg in args))
 		if kwargs:
 			pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
			arg_lst.append(', '.join(pairs))
 		arg_str = ', '.join(arg_lst)
 		print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
 		return result
 return clocked

```



## 7.8 표준 라이브러리에서 제공하는 데커레이터

- functools.lru_cache()는 메모이제이션을 구현한다. 메모이제이션은 이전에 실행한 값비싼 함수의 결과를 저장함으로써 이전에 사용된 인수에 대해 다시 계산할 필요가 없게 해준다.

```python
from clockdeco import clock
@clock
def fibonacci(n):
 	if n < 2:
 		return n
 	return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
 	print(fibonacci(6))
```



- 여러 함수를 범용 함수로 묶는 커스텀 `htmlize.register()`를 생성하는 `singledispatch`

```python
from functools import singledispatch
from collections import abc
import numbers
import html

@singledispatch
def htmlize(obj):
 	content = html.escape(repr(obj))
 	return '<pre>{}</pre>'.format(content)

@htmlize.register(str)
def _(text):
 	content = html.escape(text).replace('\n', '<br>\n')
 	return '<p>{0}</p>'.format(content)

@htmlize.register(numbers.Integral)
def _(n):
 	return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
 	inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
 	return '<ul>\n<li>' + inner + '</li>\n</ul>'
```



## 7.10 매개변수화된 데커레이터

소스코드에서 데커레이터를 파싱할 때 파이썬은 데커레이트된 함수를 가져와서 데커레이터 함수의 첫 번째 인수로 넘겨준다. 그러면 어떻게 다른 인수를 받는 데커레이터를 만들 수 있을까? 인수를 받아 데터레이터를 반환하는 데커레이터 팩토리를 만들고 나서, 데커레이트될 함수에 데커레이터 팩토리를 적용하면 된다.

- 매개변수화된 clock 데커레이터

```python
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
 	def decorate(func):
 		def clocked(*_args):
 			t0 = time.time()
 			_result = func(*_args)
 			elapsed = time.time() - t0
 			name = func.__name__
 			args = ', '.join(repr(arg) for arg in _args)
 			result = repr(_result)
 			print(fmt.format(**locals()))
 			return _result
 	return clocked
 return decorate

if __name__ == '__main__':
 	@clock()
 	def snooze(seconds):
 		time.sleep(seconds)
 	for i in range(3):
 		snooze(.123)

```

