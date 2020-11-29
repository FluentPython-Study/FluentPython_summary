# Chapter 21. 클래스 메타프로그래밍

-----------

클래스 메타프로그래밍은 실행 도중에 클래스를 생성하거나 커스터마이즈하는 기술을 말한다. 클래스는 파이썬의 일급 객체이므로, class라는 키워드를 사용하지 않고도 언제든 함수를 사용해서 생성할 수 있다. 클래스 데커레이터도 함수지만, 장식된 클래스를 조사하고, 변경하고, 심지어 다른 클래스로 대체할 수 있다.



## 21.1 클래스 팩토리

이 책에서 이미 여러 번 봤지만, 표준 라이브러리에는 collection.namedtuple()이라는 클래스 팩토리가 있다. 이것은 일종의 함수로서, 클래스 명과 속성명을 전달하면 이름으로 항목을 가져올 수 있게 해주고 디버깅하기 좋은 \_\_repr\_\_() 메서드를 제공하는 tuple의 서브클래스를 생성한다.

```python
def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()
        
    except AttributeError: # no .replace or .split
        pass # assume it's already a sequence of identifiers
        field_names = tuple(field_names)
        
def __init__(self, *args, **kwargs):
    attrs = dict(zip(self.__slots__, args))
    attrs.update(kwargs)
    for name, value in attrs.items():
        setattr(self, name, value)
        
def __iter__(self):
    for name in self.__slots__:
        yield getattr(self, name)

def __repr__(self):
    values = ', '.join('{}={!r}'.format(*i) for i
                       in zip(self.__slots__, self))
    return '{}({})'.format(self.__class__.__name__, values)

cls_attrs = dict(__slots__ = field_names,
                 __init__ = __init__,
                 __iter__ = __iter__,
                 __repr__ = __repr__)
return type(cls_name, (object,), cls_attrs) 
```

type(my_object)를 이용해서 객체의 클래스와 동일한 my_object.__class__를 가져오므로, type()을 일종의 함수로 생각하기 쉽다. 그러나 type은 클래스다. 다음과 같이 인수 세 개를 받아서 호출하면 새로운 클래스를 생성하는 일종의 클래스처럼 작동한다.

```python
MyClass = type('MyClass', (MySuperClass, MyMixin),
 {'x': 42, 'x2': lambda self: self.x * 2})
```



## 21.2 디스크립터를 커스터마이즈하기 위한 클래스 데커레이터

LineItem 클래스는 인터프리터에 의해 평가되어 생성된 클래스 객체가 model.entity() 함수에 전달된다. 파이썬은 model.entity()가 반환하는 것을 전역 명칭인 LineItem에 할당한다. 이 예제에서 model.entity()는 LineItem 클래스 안에 있는 각 디스크립터 객체의 strage_name 속성을 변경해서 반환한다.

```python
import model_v6 as model

@model.entity
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()
    
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
    def subtotal(self):
        return self.weight * self.price
```



## 21.3 임포트 타임과 런타임

컴파일 작업은 확실히 임포트 타임의 활동이긴 하지만, 이때 다른 일도 일어난다. 파이썬 대부분의 문장이 사용자 코드를 실행하고 사용자 프로그램의 상태를 변경한다는 의미에서 실행문이기 때문이다. import문은 단지 단순한 선언이 아니며, 처음 임포트되는 모듈의 모든 최상휘 수준의 코드를 실제로 실행한다. 이후에 다시 임포트되는 경우에는 동일 모듈의 캐시를 사용하고 이름들만 바인딩한다. 최상위 수준 코드에는 데이터베이스에 연결하는 등 일반적으로 '런타임'에 수행하는 작업들도 포함될 수 있다. import 문이 각종 '런타임'의 동작을 유발하기 때문에 '임포트 타임'과 '런타임'의 구분이 모호해진다.

인터프리터는 임포트 타임에 클래스 안에 들어있는 클래스의 본체까지 모든 클래스 본체를 실행한다. 클래스 본체를 실행한다는 것은 클래스의 속성과 메서드가 정의되고, 클래스 객체가 만들어짐을 의미한다. 이런 관점에서 보면 클래스 본체는 '최상위의 수준 코드'다. 임포트 타임에 실행되기 때문이다.



## 21.4 메타 클래스 기본지식

메타클래스는 일종의 클래스 팩토리다. 다만 record_factory()와 같은 함수 대신 클래스로 만들어진다는 점이 다르다. 파이썬 객체 모델을 생각해보자. 클래스도 객체이므로, 각 클래스는 다른 어떤 클래스의 객체여야한다. 기본적으로 파이썬 클래스는 type의 객체다.



## 21.5 디스크립터를 커스터마이즈하기 위한 메타클래스

```python
import model_v7 as model

class LineItem(model.Entity):
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()
   
def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price
   
def subtotal(self):
    return self.weight * self.price
```

이 코드는 model_v7.pyㅇ서 메타클래스를 정의하고, model.Entity가 그 메타클래스의 객체여야 제대로 작동한다.



## 21.6 메타클래스 \_\_prepare\_\_() 특별 메서드

몇몇 애플리케이션에서는 클래스의 속성이 정의되는 순서를 알아야 하는 경우가 종종 있다. 지금까지 본 것처럼 type() 생성자와 메타클래스의 \_\_new\_\_() 및 \_\_init\_\_() 메서드는 이름과 속성의 매핑으로 평가된 클래스 본체를 받는다. 그러나 기본적으로 매핑은 딕셔너리형이므로, 메타클래스나 데커레이터가 확인할 수 있을 때는 클래스 본체 안에 등장하는 속성의 순서가 사라져버린다.

이 문제를 해결하려면 파이썬 3에 소개된 \_\_prepare\_\_() 특별 메서드를 사용해야한다. 이 특별 메서드는 메타 클래스에서만 의미가 있으며, 클래스 메서드여야한다.

```python
class EntityMeta(type):
    """Metaclass for business entities with validated fields"""
    
@classmethod
def __prepare__(cls, name, bases):
    return collections.OrderedDict()

def __init__(cls, name, bases, attr_dict):
    super().__init__(name, bases, attr_dict)
    cls._field_names = []
    for key, attr in attr_dict.items():
        if isinstance(attr, Validated):
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)
            cls._field_names.append(key)
            
            
class Entity(metaclass=EntityMeta):
    """Business entity with validated fields"""
    
    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name
```

