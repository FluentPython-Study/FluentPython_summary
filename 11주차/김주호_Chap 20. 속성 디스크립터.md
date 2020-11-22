# Chap 20. 속성 디스크립터

---

디스크립터는 파이썬의 독특한 특징으로서, 애플리케이션 수준뿐만 아니라 언어의 기반 구조에도 적용되어 있다. 프로퍼티 외에도 메서드 및 `@classmethod`와 `@staticmethod` 데커레이터가 디스크립터를 활용하는 파이썬 기능이다. 파이썬을 정복하려면 디스크립터를 알아야 한다. 

## 20.1 디스크립터 예: 속성 검증

### 20.1.1 LineItem 버전 #3 : 간단한 디스크립터

\_\_get\_\_(), \_\_set\_\_(), \_\_delete\_\_()  메서드를 구현하는 클래스가 디스크립터다. 디스크립터는 클래스의 객체를 다른 클래스의 클래스 속성으로 정의해서 사용한다.

우리는 Quantity 디스크립터 클래스를 생성하고, LineItem 클래스는 두 개의 Quantity 객체를 사용할 것이다. 하나는 wight 속성을, 다른 하나는 price 속성을 관리하기 위해 사용한다.

```python
class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name
        
    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')
            
class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')
                
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
    def subtotal(self):
        return self.weight * self.price

```

관리 대상 속성에 값을 할당할 때 \_\_set\_\_()이 호출된다. 여기서 self는 디스크립터 객체(즉, LineItem.weight나 LineItem.price), instance는 관리 대상 객체(LineItem 객체), value는 할당할 값이다.

각각의 관리 대상 속성은 저장소 속성과 이름이 똑같으며, 별도의 게터 논리를 구현할 필요가 없으므로 Quantity 클래스에 \_\_get\_\_() 메서드가 필요없다.



### 20.1.2 LineItem 버전 #4 : 자동 저장소 속성명

```python
class Quantity:
    __counter = 0 
    
    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1
        
    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name)
       
    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')
                
                
class LineItem:
    weight = Quantity()
    price = Quantity()
    
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
    def subtotal(self):
        return self.weight * self.price
```

여기서는 instance.\_\_dict\_\_ 대신 고수준 getattr()과 setattr() 내장 함수를 이용해서 값을 저장할 수 있덨다. 관리 대상 속성과 저장소 속성의 이름이 다르기 때문에 저장소 속성에 getattr()을 호출하더라도 디스크립터를 실행하지 않으므로, 무한 재귀가 발생하지 않는다.



### 20.1.3 LineItem 버전 #5 : 새로운 디스크립터형

```python
import abc

class AutoStorage:
    __counter = 0
    
    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1
        
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)
        
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
        
        
class Validated(abc.ABC, AutoStorage):
    
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)
        
    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""
        
        
class Quantity(Validated):
    """a number greater than zero"""
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
            return value
        
        
class NonBlank(Validated):
    """a string with at least one non-space character"""
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
            return value 
```

Quantity와 NonBlock 디스크립터 클래스ㅡㄹ 사용해서 객체 속성을 자동으로 검증할 수 있다. 이 디스크립터를 사용한 최신 LineItme 클래스는 아래와 같다.

```python
import model_v5 as model

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

이러한 descripter는 오버라이딩 디스크립터라고도 한다. 디스크립터의 \_\_set\_\_() 메서드가 관리 대상 객체 안에 있는 동일한 이름의 속성 설정을 오버라이드(즉, 가로채서 변경하기)하기 때문이다. 그러나 오버라이드하지 않는 논오버라이딩 디스크립터도 있다. 이 둘의 차이점에 대해서는 다음 절에서 자세히 설명한다.



## 20.2 오버라이딩 디스크립터와 논오버라이딩 디스크립터

### 20.2.1 오버라이딩 디스크립터

\_\_set\_\_() 메서드를 구현하는 디스크립터를 오버라이딩 디스크립터라고 한다. 비록 클래스 속성이기는 하지만, \_\_set\_\_() 메서드를 구현하는 디스크립터는 객체 속성에 할당하려는 시도를 가로채기 때문이다. 프로퍼티도 오버라이딩 디스크립터라고 할 수 있다. 세터 함수를 제공하지 않더라도, property 클래스에서 기본적으로 제공하는 \_\_set\_\_() 메서드가 읽기 전용 속성임을 알려주기 위해 AtrributeError를 발생시킨다.

### 20.2.2 \_\_get\_\_()이 없는 오버라이딩 디스크립터

일반적으로 오버라이딩 디스크립터는 \_\_set\_\_()과 \_\_get\_\_() 메서드를 모두 구현하지만, \_\_set\_\_() 메서드만 오버라이드할 수도 있다. 이때는 저장 연산만 디스크립터가 처리한다. 객체를 통해 디스크립터를 확인해보면 읽기 접근을 처리하는 \_\_get\_\_() 메서드가 없으므로 디스크립터 객체 자체가 반환된다. 객체의 \_\_dict\_\_에 직접 접근해서 새로운 값을 가진 동일한 이름의 객체 속성을 생성하더라도, 이후의 쓰기 접근은 \_\_set\_\_() 메서드라 가로채지만, 그 속성을 읽을 때는 디스크립터 객체가 아니라 새로운 값을 그대로 반환한다. 즉, 읽기 연산의 경우에만 객체 속성이 디스크립터를 가린다.

### 20.2.3 논오버라이딩 디스크립터

디스크립터가 \_\_set\_\_() 메서드를 구현하지 않으면 논오버라이딩 디스크립터가 된다. 동일한 이름의 객체 속성을 설정하면 디스크립터를 가리므로, 그 객체에는 디스크립터가 작동하지 않는다. 메서드는 논오버라이딩 디스크립터로 구현된다.

디스크립터와 동일한 이름을 가진 객체 속성에 값을 할당하는 여러 연산이 디스크립터의 \_\_set\_\_() 메서드 존재여부에 따라 결과가 달라진다. 클래스 안의 속성을 설정하는 것은 이 클래스에 연결된 디스크립터가 통제할 수 없다.



## 20.3 메서드는 디스크립터

```python
import collections

class Text(collections.UserString):
    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]
```

```python
 >>> word = Text('forward')
 >>> word
 Text('forward')
 >>> word.reverse()
 Text('drawrof')
 >>> Text.reverse(Text('backward'))
 Text('drawkcab')
 >>> type(Text.reverse), type(word.reverse)
 (<class 'function'>, <class 'method'>)
 >>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))
 ['diaper', (30, 20, 10), Text('desserts')]
 >>> Text.reverse.__get__(word)
 <bound method Text.reverse of Text('forward')>
 >>> Text.reverse.__get__(None, Text)
 <function Text.reverse at 0x101244e18>
 >>> word.reverse
 <bound method Text.reverse of Text('forward')>
 >>> word.reverse.__self__
 Text('forward')
 >>> word.reverse.__func__ is Text.reverse
 True

```

바인딩된 메서드 객체는 호출을 실제로 처리하는 \_\_call\_\_() 메서드도 가지고 있다. \_\_call\_\_()은 메서드의 \_\_self\_\_ 속성을 첫 번째 인수로 전달해서 \_\_fucn\_\_ 속성이 참조하는 원래 함수를 호출한다. 전형적인 self 인자는 이런 방식으로 바인딩된다.