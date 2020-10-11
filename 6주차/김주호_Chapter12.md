# Chapter 12. 내장 자료형 상속과 다중 상속

내장 자료형의 상속과 관련된 문제를 이야기하면서 상속에 대해 설명한다. C언어로 구현된 네이티브 메서드는 몇몇 특별한 경우를 제외하고는 서브클래스가 오버라이드한 메서드를 호출하지 않는다. 그렇기 때문에 `list`, `dict`, `str` 형을 커스터마이즈해야 할 때는 collection 모듈에 정의된 UserList, UserDict, UserString을 사용하는 것이 좋다. 원하는 행동이 내장 자료형이 제공하는 기능과 상당히 다를 때는 collections.abc에서 제공하는 적절한 ABC를 상속해서 직접 구현하는 것이 좋다.

- 다중 상속

`__mro__` 클래스 속성에 저장된 메서드 결정 순서가 상속된 메서드의 이름 충돌 문제를 어떻게 해결하는지 살핀다. 그리고 내장된 함수 `super()`가 `__mro__`에 따라 슈퍼클래스의 매서드를 호출하는 방법에 대해 알아본다. 또한 파이썬 표준 라이브러리에서 제공되느느 Tkinter GUI 툴킷에 다중 상속을 사용하는 방법을 살펴본다. Tkinter는 최신의 모범적인 관례를 따르지 않으므로 믹스인 클래스를 사용하는 방법과 다중 상속을 피하고 대힌 구성을 이용해서 다중 상속 문제를 해결하는 방법을 할아본다. 다중 상속을 남용하는 Tkinter를 분석한 후, 장고의 클래스 기반 뷰 계층구조의 핵심 부분을 조사한다.



## 12.1 내장 자료형의 상속은 까다롭다.

dict 대신 collections.UserDict를 상속하면 문제가 해결된다.

```python
>>> import collections
>>>
>>> class DoppelDict2(collections.UserDict):
... def __setitem__(self, key, value):
... super().__setitem__(key, [value] * 2)
...
>>> dd = DoppelDict2(one=1)
>>> dd
{'one': [1, 1]}
>>> dd['two'] = 2
>>> dd
{'two': [2, 2], 'one': [1, 1]}
>>> dd.update(three=3)
>>> dd
{'two': [2, 2], 'three': [3, 3], 'one': [1, 1]}
>>>
>>> class AnswerDict2(collections.UserDict):
... def __getitem__(self, key):
... return 42
...
>>> ad = AnswerDict2(a='foo')
>>> ad['a']
42
>>> d = {}
>>> d.update(ad)
>>> d['a']
42
>>> d
{'a': 42}
```



## 12.2 다중 상속과 메서드 결정 순서

다이아몬드 문제

```python
class A:
    def ping(self):
        print('ping:', self)
        
class B(A):
    def pong(self):
        print('pong:', self)

class C(A):
    def pong(self):
        print('PONG:', self)

class D(B, C):
    def ping(self):
        super().ping()
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)
```



```python
>>> from diamond import *
>>> d = D()
>>> d.pong() 
pong: <diamond.D object at 0x10066c278>
>>> C.pong(d) # 객체를 인수로 전달해서 슈퍼클래스의 메서드를 직접 호출
PONG: <diamond.D object at 0x10066c278>
```



```python
>>> D.__mro__
(<class 'diamond.D'>, <class 'diamond.B'>, <class 'diamond.C'>,
<class 'diamond.A'>, <class 'object'>)
```



## 12.4 다중상속 다루기

1. 인터페이스 상속과 구현 상속을 구분한다.

    - 인터페이스 상속 : is-a 관계를 의미하는 서브타입을 생성
    - 구현 상속 : 재사용을 통해 코드 중복을 피함

    

2. ABC를 이용해서 인터페이스를 명확히 한다.

3. 코드를 재사용하기 위해 믹스인을 사용한다.

4. 이름을 통해 믹스인임을 명확히 한다.

5. ABC가 믹스인이 될 수는 있지만, 믹스인이라고 해서 ABC인 것은 아니다.

6. 두 개 이상의 구상 클래스에서 상속 받지 않는다.

7. 사용자에게 집합 클래스를 제공한다.

8. 클래스 상속보다 객체 구성을 사용하라

    - 구성을 좋아하게 되면 설계의 융통성이 향상된다.



## 12.5 최신 사례 : 장고 제너릭 뷰의 믹스인

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

