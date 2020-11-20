# Chap 19. 동적 속성과 프로퍼티

-------

## 19.1 동적 속성을 이용한 데이터 랭글링

```python
from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'

def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())
            
    with open(JSON) as fp:
        return json.load(fp)
```



### 19.1.1 동적 속성을 이용해서 JSON과 유사한 데이터 둘러보기

```python
>>> from osconfeed import load
>>> raw_feed = load()
>>> feed = FrozenJSON(raw_feed)
>>> len(feed.Schedule.speakers)
357
>>> sorted(feed.Schedule.keys())
['conferences', 'events', 'speakers', 'venues']
>>> for key, value in sorted(feed.Schedule.items()):
    ... print('{:3} {}'.format(len(value), key))
    ...
    
1 conferences
484 events
357 speakers
53 venues

>>> feed.Schedule.speakers[-1].name
'Carina C. Zona'
>>> talk = feed.Schedule.events[40]
>>> type(talk)
<class 'explore0.FrozenJSON'>
>>> talk.name
'There *Will* Be Bugs'
>>> talk.speakers
[3471, 5199]
>>> talk.flavor
Traceback (most recent call last):
    ...
    KeyError: 'flavor'

```

FrozenJSON 클래스의 핵심은 \_\_getattr\_\_() 메서드다. 이 메서드는 속성을 가져오기 위한 일반적인 과정이 실패할 때(즉, 지명한 속성을 객체, 클래스, 슈퍼클래스에서 찾을 수 없을 때)만 인터프리터에서 호출한다는 점에 유의해야 한다. 마지막 행은 구현에 관련된 작은 문제를 보여준다. 이상적으로는 없는 속성을 읽을 때 AttributeError 예외가 발생해야 한다.

```python
from collections import abc

class FrozenJSON:
 """A read-only façade for navigating a JSON-like object
 using attribute notation
 """

def __init__(self, mapping):
    self.__data = dict(mapping)
    
def __getattr__(self, name):
    if hasattr(self.__data, name):
        return getattr(self.__data, name)
    else:
        return FrozenJSON.build(self.__data[name])
    
@classmethod
def build(cls, obj):
    if isinstance(obj, abc.Mapping):
        return cls(obj)
    elif isinstance(obj, abc.MutableSequence):
        return [cls.build(item) for item in obj]
    else:
        return obj

```

대안 생성자로서, 일반적으로 `@classmethod` 데커레이터가 사용된다. obj가 매핑형이면, 이 객체로부터 FrozenJSON 객체를 생성한다. 피드를 순회하면서 내포된 데이터 구조체들이 계속해서 FrozenJSON으로 변환된다. 그러나 이 정도 크기의 데이터셋에서 데이터를 순회만 하는 코드에서는 이 변환 작업이 큰 문제가 되지 않는다.



### 19.1.3 \_\_new\_\_()를 이용한 융통성 있는 객체 생성

흔히 \_\_init\_\_() 메서드를 생성자 메서드라고 부르지만, 생성자라는 말은 다른 언어에서 빌려온 용어일 뿐이다. 실제로 객체를 생성하는 특별 메서드는 \_\_ new\_\_()이다. 실제 생성자인 \_\_ new\_\_() 메서드느 object 클래스에서 상속받은 메서드로도 충분하므로 직접 구현할 일은 거의 없다.

```python
from collections import abc

class FrozenJSON:
 """A read-only façade for navigating a JSON-like object
 using attribute notation
 """

def __new__(cls, arg):
    if isinstance(arg, abc.Mapping):
        return super().__new__(cls)
    elif isinstance(arg, abc.MutableSequence):
        return [cls(item) for item in arg]
    else:
        return arg

def __init__(self, mapping):
    self.__data = {}
    for key, value in mapping.items():
        if iskeyword(key):
            key += '_'
            self.__data[key] = value

def __getattr__(self, name):
    if hasattr(self.__data, name):
        return getattr(self.__data, name)
    else:
        return FrozenJSON(self.__data[name]) 

```

\_\_new\_\_() 메서드는 일반적으로 해당 클래스의 객체를 생성하므로 클래스를 첫 번째 인수로 받는다. 따라서 FrozenJSON.__new\_\_() 안에서 super().\_\_new\_\_(cls)는 object.\_\_new\_\_(FrozenJSON)을 호출하는 셈이 되어 object 클래스가 실제로는 FrozenJSON 객체를 생성한다. 즉, 실제로는 파이썬 인터프리터 내부에서 C언어로 구현된 object.\_\_new\_\_()가 객체를 생성하지만, 생성된 객체의 \_\_class\_\_속성은 FrozenJSON 가리키게 된다.



## 19.2 속성을 검증하기 위해 프로퍼티 사용하기

### 19.2.1 LineItem 버전 #1 : 주문 항목 클래스

```python
class LineItem:
def __init__(self, description, weight, price):
    self.description = description
        self.weight = weight
        self.price = price
        
def subtotal(self):
    return self.weight * self.price

```

### 19.2.2 LineItem 버전 #2 : 검증하는 프로퍼티

```python
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
        def subtotal(self):
            return self.weight * self.price
        
        @property
        def weight(self):
            return self.__weight
        
        @weight.setter
        def weight(self, value):
            if value > 0:
                self.__weight = value
            else:
                raise ValueError('value must be > 0')
```



## 19.3 프로퍼티 제대로 알아보기

내장된 property()는 비록 데커레이터로 사용되는 경우가 많지만, 사실상 클래스다. 파이썬에서 함수와 클래스는 서로 교환할 수 있는 경우가 많다. 함수와 클래스는 모두 콜러블이고 객체를 생성하기 위한 new 연산자가 없으므로, 생성자를 호출하는 것은 팩토리 함수를 호출하는 것과 차이가 없다. 그리고 장식된 함수를 적절히 대체할 수 있는 콜러블을 생성한다면 둘 다 데커레이터로 사용할 수 있다.

```python
property(fget=None, fset=None, fdel=None, doc=None)
```

```python
class LineItem:
    
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
    def subtotal(self):
        return self.weight * self.price
    
    def get_weight(self):
        return self.__weight
    
    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
            
    weight = property(get_weight, set_weight) 

```

경우에 따라서 고전적인 구문이 데터레이터 구문보다 나을 때도 있다. 잠시 후에 설명할 프로퍼티 팩토리가 그 사례다. 한편 메서드가 많이 있는 클래스 본체 안에서 프로퍼티는 메서드명 앞에 get과 set을 사용하는 관례에 의존하지 않고도 어느 것이 게터고, 어느 것이 세터인지 명확히 보여준다.



### 19.3.1 객체 속성을 가리는 프로퍼티

```python
>>> class Class: #
... 	data = 'the class data attr'
... 	@property
... 	def prop(self):
... 		return 'the prop value'
...

>>> obj = Class()
>>> vars(obj) #
{}
>>> obj.data #
'the class data attr'
>>> obj.data = 'bar' #
>>> vars(obj) #
{'data': 'bar'}
>>> obj.data #
'bar'
>>> Class.data #
'the class data attr'

```

### 19.3.2 프로퍼티 문서화

```python
weight = property(get_weight, set_weight, doc='weight in kilograms')
```

```python
class Foo:
    
    @property
    def bar(self):
        '''The bar attribute'''
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value
```

프로퍼티에 대한 핵심사항을 살펴봤으니, 이제 두 개의 거의 동일한 세터/게터를 직접 구현하지 않고도 LineItem의 weight와 price 속성이 0보다 큰 값을 받을 수 있도록 보호하는 문제로 돌아간다.



## 19.4 프로퍼티 팩토리 구현하기

여기서는 quantity()라는 프로퍼티 팩토리를 만든다. 

```python
class LineItem:
     weight = quantity('weight')
     price = quantity('price')
    
     def __init__(self, description, weight, price):
         self.description = description
         self.weight = weight
         self.price = price
     
     def subtotal(self):
         return self.weight * self.price 
```

프로퍼티를 전통적인 방식으로 구현하는 겨웅에는 값을 저장할 속성명이 게터와 세터 메서드 안에 하드코딩된다. 그러나 여기서 qty_getter()와 qty_setter()는 범용 함수로서, 객체의 \_\_dict\_\_안에 있는 어느 속성에서 값을 가져오고 어느 속성에 값을 저장할지 판단하기 위해 storage_name에 의존한다. quantity() 팩토리 함수가 호출될 때마다 프로퍼티를 생성하므로, storate_name은 고유한 값으로 설정되어야 한다.



## 19.5 속성 제거 처리하기

```python
del my_object.an_attribute
```

```python
class BlackKnight:
    def __init__(self):
         self.members = ['an arm', 'another arm',
         'a leg', 'another leg']
         self.phrases = ["'Tis but a scratch.",
         "It's just a flesh wound.",
         "I'm invincible!",
        "All right, we'll call it a draw."]
            
    @property
    def member(self):
        print('next member is:')
        return self.members[0]
    
    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))
```

