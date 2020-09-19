# Chap 5. 일급(First-class) 함수
이 장의 목적은 파이썬 함수의 일급 특성에 대해 탐구하는 것이었다. 기본 개념은 

- 함수를 변수에 할당하고, 
- 다른 함수에 전달하고, 
- 데이터 구조체에 저장하며,
- 함수 속성에 접근해서

프레임워크나 도구가 이 속성 정보를 사용할 수 있게 해주는 것이다. 지능형 리스트 및 제너레이터 표현식과 sum(). all(), any() 등 내장된 리덕션 함수의 등장으로 map(), filter(), reduce() 함수가 예전보다 사용 빈도가 떨어지기는 했지만, 함수형 프로그래밍의 기본적인 특징인 고위 함수를 파이썬에서 쉽게 볼 수 있다. sorted(), min(), max() 내장 함수와 dunctools.partial()이 자주 사용되는 고위 함수의 예다.

  파이썬에서 콜러블은 람다로 생성한 간단한 함수부터 \_\_call\_\_() 메서드를 구현하는 클래스 객체까지, 7가지 형태로 구현할 수 있다. 모든 콜러블은 callable() 내장 함수가 탐지할 수 있다. 모든 콜러블은 파이썬 3에서 새로 소개된 

- 키워드 전용 매개변수와 
- 애너테이션 등

매개변수를 선언하는 풍부한 구문을 공통적으로 지원한다.

파이썬 함수와 애너테이션에는 inspect 모듈을 이용해서 쉽게 읽을 수 있는 속성이 풍부하게 들어 있다. inspect 모듈에 포함된 Signature.bind() 메서드는 인수를 매개변수에 바인딩하기 위해 파이썬이 사용하는 규칙을 적용한다.

마지막으로 operator 모듈에서 제공하는 함수 몇 개와 functools.partial() 함수에 대해 설명했다. 이 함수들은 기능이 떨어지는 람다 구문을 사용할 필요 없이 쉽게 함수형 프로그래밍을 할 수 있게 해준다.


## 핵심개념1. 일급 함수 (First - class Function) 

프로그래밍 언어가 함수를 first-class citizen으로 취급하는 것을 말한다. 함수를 first-class citizen으로 취급 가능하다고 하는 것은 다음을 뜻한다.

- 함수를 변수나 자료구조(리스트, 튜플, set, 딕셔너리)에 저장할 수 있다.
- 함수의 매개변수(인자)에 다른 함수를 인수로 전달할 수 있다.
- 함수의 반환 값(return 값)으로 함수를 전달할 수 있다.

1960년에 탄생한 일급함수의 개념을 파이썬의 함수에도 적용이 된다. 따라서 파이썬의 함수는 함수를 변수나 자료구조에 저장 가능하며, 매개변수에 인수로 전달 가능하며, 함수의 return값으로 사용할 수 있는 것이다.



```python
## 1. 함수를 변수나 자료구조에 저장

def add(a, b):
    return a+b

var = add
print(var is add)
```

    True



```python
## 2. 함수의 매개변수에 함수를 인자로 사용

def square(x):
    return x*x

def first_class(func, arg_list):
    print("Running Finction : %s" % func.__name__)
    
    return [func(i) for i in arg_list]

num_list = [i for i in range(10)]
result = first_class(square, num_list)
print(result)
```

    Running Finction : square
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]



```python
## 3. 함수의 반환 값(return 값)으로 함수를 전달할 수 있다.
def logger(message):
    
    def log_message():
        print("Log : %s" % message)
        
    return log_message

log_hi = logger("Hi. Nice to meet you")
print(log_hi())
```

    Log : Hi. Nice to meet you
    None



```python
def add2(num1, num2):
    return num1 + num2

def first_class2(func):

    def addition(*args, **kwargs):
        print(f"Running Function : {func.__name__}") ## Running Function : add2
        print(f"Positional arguments : {args}") ## Positional arguments : (3, 5)
        print(f"Keyword argumets : {kwargs}") ## Keyword argumets : {}
        result = func(*args, **kwargs)

        return result

    return addition

decorated_add = first_class2(add2)
print(decorated_add) ## <function first_class2.<locals>.addition at 0x00000273FC3701F0>
print(decorated_add(3, 5)) ## 8
```

    <function first_class2.<locals>.addition at 0x000002738C3CB598>
    Running Function : add2
    Positional arguments : (3, 5)
    Keyword argumets : {}
    8


## 핵심개념2. 고위함수(higher-order function)

- 함구를 인자로 받거나
- 함수를 결과로 반환하는 함수

일급함수의 조건 중 두가지를 만족하는 것


```python
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=len))
print(sorted(fruits, key=lambda word: word[::-1]))
```

    ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']
    ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']


## 5.5 사용자 정의 콜러블형
파이썬 함수가 실제 객체일 뿐만 아니라, 모든 파이썬 객체가 함수처럼 동작하게 만들 수 있다. 단지 **\_\_call\_\_() 인스턴스** 메서드를 구현하면 된다.


```python
import random

class BingoCage:
    
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)
        
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
            
    def __call__(self):
        return self.pick()
    
if __name__ == "__main__":
    bingo = BingoCage(range(4))
    print(bingo.pick())
    print(bingo())
    print(callable(bingo))
```

    3
    2
    True


## 5.7 위치 매개변수, 퀴워드 전용 매개변수


```python
def tag(name, *content, cls=None, **attrs):
    """하나 이상의 HTML 태그를 생성한다"""
    if cls is not None:
        attrs['class'] = cls
    
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for (attr, value) in sorted(attrs.items())) 
    else:
        attr_str = ''
    
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)
    
if __name__=="__main__":
    print(tag('br'), "\n")
    print(tag('p', 'hello', 'world'), "\n")
    print(tag('p', 'hello', 'world', cls='sidebar'))
```

    <br /> 
    
    <p>hello</p>
    <p>world</p> 
    
    <p class="sidebar">hello</p>
    <p class="sidebar">world</p>


## 5.9 함수 애너테이션


```python
def func(arg1: str, arg2: 1+2, arg3: 'this is annotation') -> bool:
    print(f'arg1 = {arg1}') 
    print(f'arg2 = {arg2}') 
    print(f'arg3 = {arg3}') 
    
    return True 

result = func('test1', 3, 'this is test') 
print(f'result = {result}')

```

    arg1 = test1
    arg2 = 3
    arg3 = this is test
    result = True


## 5.10 함수형 프로그래밍을 위한 패키지
### 5.10.1 operator 모듈


```python
## reduce

from functools import reduce

reduce(lambda a,b : a*b, range(1, 10))
```




    362880




```python
## itemgetter

from operator import itemgetter, attrgetter
from collections import namedtuple

metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

# itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
print('\n')
    
# attrgetter
LatLong = namedtuple('LatLong', 'lat long')
Metropolis = namedtuple('Matropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data]
print(metro_areas[0])
print('\n')

name_lat = attrgetter('name', 'coord.lat')
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))
print('\n')
```

    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))


​    
    Matropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))


​    
    ('Sao Paulo', -23.547778)
    ('Mexico City', 19.433333)
    ('Delhi NCR', 28.613889)
    ('Tokyo', 35.689722)
    ('New York-Newark', 40.808611)


​    
​    

### 5.10.2 functools.partial()로 인수 고정하기

functools.partial()은 함수를 부분적으로 실행할 수 있게 해주는 고위함수이다. 어떤 함수가 있을 때 partial()을 적용하면 원래 함수의 일부 인수를 고정한 콜러블을 생성한다. 이 기법은 하나 이상의 인수를 받는 함수를 그보다 적은 인수를 받는 콜백 함수를 사용하는 API에 사용하고자 할 때 유용하다.


```python
from operator import mul
from functools import partial

triple = partial(mul, 3)
triple(7)
```




    21