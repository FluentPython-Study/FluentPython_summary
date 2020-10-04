# Chapter 10. 시퀀스 해킹, 해시, 슬라이스

이 장에서 구현한 Vector 클래스는 단일 반복형 인수를 받는 내장 시퀀스의 다양한 생성자 시그니처를 제외하고는 Vector2d 클래스와 호환되도록 설계되었다. `__getitem__`()과 `__len__`()메서드를 구현함으로써 Vector가 시퀀스처럼 동작한다는 사실을 통해 프로토콜을 설명한다. 덕 타이핑을 지원하는 파이썬 언어에서의 프로토콜은 비공식 인터페이스다.

slice(a,b,c) 객체를 생성하고 `__getitem__`() 메서드에서 처리함으로써 `my_seq[a:b:c]`가 내부적으로 작동하는 방식을 살펴본다. 이 지식을 이용해서 파이썬 시퀀스의 작동 방식과 유사하게 새로운 Vector 객체를 반환함으로써 Vector 클래스가 슬라이싱에 대해 올바로 반응하도록 만든다.

다음단계에서는 my_vec.x와 같은 구문을 이용해서 처음 몇 개의 Vector 요소에 읽기 전용으로 접근할 수 있도록 `__getattr__()` 메서드를 구현했다. `my_vec.x`와 같은 구문을 사용할 수 있게 해주면 사용자들은 my_vec.x = 7처럼 특별 요소에 값을 할당하고 싶어 하게 되므로, 버그가 발생할 수 있다. 이 문제는 `__setattr__()` 메서드를 구현해서 단일 문자 속성에 값을 할당하지 못하게 함으로써 해결한다. `__getattr__()`메서드를 구현하는 경우 일관성 없는 작동을 피하려면 `__setattr__()` 메서드도 함께 구현해야 하는 경우가 대부분이다.

`__hash__()` 메서드를 구현할 때 `functools.reduce()`를 사용할 기회를 가진다. 전체 Vector에 대한 해시를 계산하기 위해 Vector의 각 요소의 해시에 XOR연산자(^)를 연속으로 적용해야 하기 때문이다. `__hash__()` 메서드에서 `reduce()` 함수를 사용한 후, `__eq__()` 메서드를 더 효율적으로 개선하기 위해 내장된 리듀스 함수 중 하나인 `all()`을 사용한다.

마지막으로 기본적인 직교좌표 외에 구면좌표를 지원하는 Vector2d 클래스의 `__format__()` 메서드에 맞춰 Vector 클래스의 `__format__()` 함수도 다시 구현했다. __format__() 및 보조 메서드를 구현하기 위해 약간의 수학과 제너레이터를 사용한다.



## 10.2 Vector 버전 #1 : Vector2d 호환

- Vector 클래스가 Vector2d 클래스를 상속받도록 만들지 않은 이유
    - 생성자가 호환되지 않는다.
    - vector 클래스에 대한 정리가 필요



- 최종 코드

```python
from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools

class Vector:
    typecode = 'd'
    300 | Chapter 10: Sequence hacking, hashing and slicing
        def __init__(self, components):
            self._components = array(self.typecode, components)
            
            def __iter__(self):
                return iter(self._components)
            
            def __repr__(self):
                components = reprlib.repr(self._components)
                components = components[components.find('['):-1]
                return 'Vector({})'.format(components)
            
            def __str__(self):
                return str(tuple(self))
            
            def __bytes__(self):
                return (bytes([ord(self.typecode)]) +
                        bytes(self._components))
            
            def __eq__(self, other):
                return (len(self) == len(other) and
                        all(a == b for a, b in zip(self, other)))
            
            def __hash__(self):
                hashes = (hash(x) for x in self)
                return functools.reduce(operator.xor, hashes, 0)
            
            def __abs__(self):
                return math.sqrt(sum(x * x for x in self))
            
            def __bool__(self):
                return bool(abs(self))
            
            def __len__(self):
                return len(self._components)
            
            def __getitem__(self, index):
                cls = type(self)
                if isinstance(index, slice):
                    return cls(self._components[index])
                elif isinstance(index, numbers.Integral):
                    return self._components[index]
                else:
                    msg = '{.__name__} indices must be integers'
                    raise TypeError(msg.format(cls))
                    shortcut_names = 'xyzt'
                    def __getattr__(self, name):
                        cls = type(self)
                      
                if 0 <= pos < len(self._components):
                        return self._components[pos]
                    msg = '{.__name__!r} object has no attribute {!r}'
                    raise AttributeError(msg.format(cls, name))
                    def angle(self, n):
                        r = math.sqrt(sum(x * x for x in self[n:]))
                        a = math.atan2(r, self[n-1])
                        if (n == len(self) - 1) and (self[-1] < 0):
                            return math.pi * 2 - a
                        else:
                            return a
                        def angles(self):
                            return (self.angle(n) for n in range(1, len(self)))
                        def __format__(self, fmt_spec=''):
                            if fmt_spec.endswith('h'): # hyperspherical coordinates
                                fmt_spec = fmt_spec[:-1]
                                coords = itertools.chain([abs(self)],
                                                         self.angles())
                                outer_fmt = '<{}>'
                                else:
                                    coords = self
                                    outer_fmt = '({})'
                                    components = (format(c, fmt_spec) for c in coords)
                                    return outer_fmt.format(', '.join(components))
                                @classmethod
                                def frombytes(cls, octets):
                                    typecode = chr(octets[0])
                                    memv = memoryview(octets[1:]).cast(typecode)
                                    return cls(memv)
```

