# Chapter 9. 파이썬스러운 객체

--------

이 장에서는 특별 메서드 및 파이썬스러운 클래스를 생성하는 관례에 대해 설명한다. 파이썬스러운 객체는 요구사항을 만족하는 한 가장 단순해야 하며, 언어 기능을 모두 갖출 필요는 없다. 이 장에서는 Vector2d 코드를 계속 개선하면서 **파이썬 특별 메서드와 코딩 관례**를 설명한다.

- 문자열.바이트로 표현하는 모든 메서드: `__repr__(), __str__(), __format__(), __bytes__()`
- 객체를 숫자로 변환하는 여러 메서드: `__abs__(), __bool__(), __hash__()`
- bytes로 변환하고 해시할 수 있게 해주는 메서드: `__eq__(), __hash__()`

bytes로 변환하는 동안 대안 생성자 `Vector2d.frombytes()`도 구현 했다. 대안 생성자를 기반으로 `@classmethod @staticmethod` 데커레이터도 설명했다. `@classmethod` 데커레이터는 아주 유용하다. `@staticmethod`는 그닥 유용하지 않으며, 이보다는 모듈 수준의 함수를 사용하는 것이 더 간단하다. 

포맷 명시 간이 언어(format specification mini-language)는 `__format__()` 메서드를 구현해서 쉽게 확장할 수 있다. `__format__()` 메서드는 

- `format(obj, format_spec)` 내장 함수의 format_spec이나 
- `str.format()` 메서드에 사용되는 문자열 안에 있는 '{:<format_spec>}' 치환 필드를 파싱한다.

Vector2d를 해시 가능하게 만들기 위해 준비하면서, x와 y의 속성을 비공개로 구현하고 읽기 전용 프로퍼티로 공개함으로써 실수로 값을 변경하지 못하도록 불변형으로 만들었다. 그러고 나서 객체 속성들의 해시를 XOR하는 권장 기법을 이용해서 `__hash__()`메서드를 구현한다.

또한 메모리 절약과 Vector2d에서 `__slots__` 속성을 선언할 때 주의해야 할 점을 설명했다. `__slots__`는 사용하기 약간 까다로우므로 (수백만개 쯤 되는) 아주 많은 객체를 다룰 때만 사용할 가치가 있다. 

마지막으로 self.typecode 등의 객체 속성을 이용해서 클래스 속성을 오버라이드 하는 방법에 대해 설명한다. 

1. 객체 속성을 이용해서 오버라이드하는 방법
2. 클래스를 상속해서 서브클래스의 클래스 수준에서 덮어쓰는 방법



## 9.2 벡터 클래스의 부활

```python
from array import array
import math

class Vector2d:
 	typecode = 'd'
 	
    def __init__(self, x, y):
 		self.x = float(x)
 		self.y = float(y)
        
     def __iter__(self):
         return (i for i in (self.x, self.y))

     def __repr__(self):
         class_name = type(self).__name__
         return '{}({!r}, {!r})'.format(class_name, *self)

     def __str__(self):
         return str(tuple(self))

     def __bytes__(self):
         return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

     def __eq__(self, other):
         return tuple(self) == tuple(other)

     def __abs__(self):
         return math.hypot(self.x, self.y)

     def __bool__(self):
         return bool(abs(self)) 
```



## 9.6 해시 가능한 Vector2d

- Vector2d를 불변형으로 만들기

```python
class Vector2d:
	typecode = 'd'
        	
	def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        
        @property
        def x(self):
            return self.__x
        
        @property
        def y(self):
            return self.__y
        
        def __iter__(self):
            return (i for i in (self.x, self.y)) 
```



- 완전한 코드

```python
from array import array
import math
class Vector2d:
    typecode = 'd'
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        @property
        def x(self):
            return self.__x
        
        @property
        def y(self):
            return self.__y
        
        def __iter__(self):
            return (i for i in (self.x, self.y))
        
        def __repr__(self):
            class_name = type(self).__name__
            return '{}({!r}, {!r})'.format(class_name, *self)
        
        def __str__(self):
            return str(tuple(self))
        
        def __bytes__(self):
            return (bytes([ord(self.typecode)]) +
                    bytes(array(self.typecode, self)))
		
        def __eq__(self, other):
            return tuple(self) == tuple(other)
        
        def __hash__(self):
            return hash(self.x) ^ hash(self.y)
        
        def __abs__(self):
            return math.hypot(self.x, self.y)
        
        def __bool__(self):
            return bool(abs(self))
        
        def angle(self):
            return math.atan2(self.y, self.x)
        
        def __format__(self, fmt_spec=''):
            if fmt_spec.endswith('p'):
                fmt_spec = fmt_spec[:-1]
                coords = (abs(self), self.angle())
                outer_fmt = '<{}, {}>'
                else:
                    coords = self
                    outer_fmt = '({}, {})'
                    components = (format(c, fmt_spec) for c in coords)
                    return outer_fmt.format(*components)
                
        @classmethod
        def frombytes(cls, octets):
            typecode = chr(octets[0])
            memv = memoryview(octets[1:]).cast(typecode)
            return cls(*memv)
```



## 9.7 파이썬에서의 비공개 속성과 보호된 속성

파이썬에는 private 수정자가 있는 자바와 달리 비공개 변수를 생성할 수 있는 방법이 없다. 서브 클래스에서 '비공개' 성격의 속성을 실수로 변경하지 못하게 하는 간단한 메커니즘은 있다. 이름 장식은 안전을 제공하지만, 보안 기능은 아니다. 실수로 접근하는 것을 막도록 설계되어 있지만 고의적인 악용을 막지는 못한다.



## 9.8 `__slots__` 클래스 속성으로 공간 절약하기

- 슈퍼클래스에서 상속받은 `__slots__` 속성은 서브클래스에 영향을 미치지 않는다. 파이썬은 각 클래스에서 개별적으로 정의된 `__slot__` 속성만 고려한다.
- 클래스 안에 __slot__을 명시하는 경우, 객체는 __slots__에 명시되지 않은 속성을 가질 수 없게 된다. 이는 __slots__가 존재하는 이유는 아니며, 실제로는 부작용이다.
- 주의할 점
    - 인터프리터는 상속된 `__slot__`속성을 무시하므로 각 클래스마다 `__slot__`속성을 다시 정의해야 한다.
    - `__dict__`를 `__slot__`에 추가하지 않는 한 객체는 `__slots__`에 나열된 속성만 가질 수 있다. (그러나 `__dict__`를 `__slot__`에 추가하면 메모리 절감 효과가 반감될 수 있다)
    - `__weakref__`를 `__slots__`에 추가하지 않으면 객체가 약한 참조의 대상이 될 수 없다.



## 9.9 클래스 속성 오버라이드

클래스 속성은 공개되어 있고 모든 서브클래스가 상속하므로, 클래스 데이터 속성을 커스터마이즈할 때는 클래스를 상속하는 것이 일반적인 방식이다.

```
>>> from vector2d_v3 import Vector2d
>>> class ShortVector2d(Vector2d): #
... typecode = 'f'
...
>>> sv = ShortVector2d(1/11, 1/27) #
>>> sv
ShortVector2d(0.09090909090909091, 0.037037037037037035) #
Overriding class attributes | 269
>>> len(bytes(sv)) #
9
```

