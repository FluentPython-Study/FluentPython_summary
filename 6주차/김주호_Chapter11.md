# Chapter 11. 인터페이스 : 프로토콜에서 ABC까지

학습 목표 : 

- 프로토콜이라고 불리는 인터페이스의 상당히 동적인 성질
- ABC의 정적 인터페이스 선언 알아보기
- `__subclasshok__()`으로 가상 서브클래스와 동적 서브클래스를 탐지하는 ABC (동적 측면)

파이썬은 시퀀스 프로토콜을 깊숙이 지원한다. 클래스가 단지 `__getitem__()`만 구현하여도 파이썬은 그 객체를 반복할 수 있고, in 연산자도 제대로 작동한다. `멍키 패칭`은 프로그램의 동적 성질을 잘 보여준다. 부분적으로 구현된 프로토콜도 매우 유용하다. 가변 시퀀스 프로토콜의 `__setitem__()` 메서드만 추가해도 표준 라이브러리에서 제공하는 `random.shuffle()`을 사용할 수 있게 된다. 기존 프로토콜을 이해하면 파이썬 표준 라이브러리가 제공하는 풍부한 기능의 대부분을 사용할 수 있다.

FrenchDeck2 예제는 ABC의 주요 장단점을 명확히 보여준다. abc.MutableSequence를 상속함으로써 우리에게 필요 없는 insert()와 `__delitem__()` 메서드를 구현해야 한다. 한편 파이썬 초보자도 FrenchDeck2 클래스가 가변 시퀀스라는 것을 알 수 있다. 게다가 abc.MutableSequence로부터 바로 사용할 수 있는 메서드 11개를 불려받는다. 그 중 5개는 abc.Sequence가 제공한다.

- ABC를 만드는 동기

    추상 베이스 클래스를 정의함으로써 일련의 서브클래스에 대한 공통된 API를 규정할 수 있다. 이 기능은 특히 애플리케이션 소스 코드에 익숙지 않은 사람들이 플러그인 확장을 제공하려 할 때 유용하다.

Tombola ABC를 이용하면서 우리는 구상 서브클래스 3개를 생성했다. 2개는 Tombola를 상속하고, 나머지 하나는 Tombola에 등록한 가상 서브클래스다. 이들 클래스 모두 동일한 일련의 테스트를 통과한다.

또한 여러 내장 자료형이 collections.abc 모듈의 ABC에 어떻게 등록되어 있는지 설명한다. 따라서, memoryview가 abc.Sequence를 상속하지 않더라도 `isinstance(memoryview, abc.Sequence)` 코드가 True를 반환한다. 그리고 마지막으로 `__subclasshook__()` 메서드는 등록되지 않은 클래스도 간단하든 복잡하든 어떤 테스트를 통과하면 ABC가 서브클래스로 인식할 수 있게 해준다. 표준 라이브러리에 있는 예제는 단지 메서드명을 확인해서 테스트한다.

사용자가 확장할 수 있는 프레임워크를 만들지 않는 한 우리가 직접 ABC를 만들지 않아야 한다는 알렉스 마르텔리의 충고가 있다. 일상적으로 우리는 프레임워크를 만들기보다는 기존 ABC를 상속하거나 ABC에 등록하는 일을 주로 한다. 상속이나 등록보다는 드물지만 ABC를 이용해서 isinstance()로 검사를 하기도 한다. 그리고 ABC 클래스를 처음부터 만드는 일은 이보다도 훨씬 더 드물다.



## 11.2 파이썬은 시퀀스를 찾아낸다.

파이썬 데이터 모델은 가능한 한 많이 핵심 프로토콜과 협업하겠다는 철학을 가지고 있다. 시퀀스의 경우, 가장 단순한 객체를 사용하는 경우에도 파이썬은 최선을 다한다.



## 11.3 런타임에 프로토콜을 구현하는 멍키 패칭

- 멍키 패칭 :  소스코드를 건드리지 않고 런타임에 클래스나 모듈을 변경하는 행위

```python
>>> def set_card(deck, position, card):
... deck._cards[position] = card
...
>>> FrenchDeck.__setitem__ = set_card
>>> shuffle(deck)

>>> deck[:5]
[Card(rank='3', suit='hearts'), Card(rank='4', suit='diamonds'), Card(rank='4',
suit='clubs'), Card(rank='7', suit='hearts'), Card(rank='9', suit='spades')]
```



## 11.5 ABC 상속하기

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]
        
        def __len__(self):
            return len(self._cards)
        
        def __getitem__(self, position):
            return self._cards[position]
        
        def __setitem__(self, position, value): 
            self._cards[position] = value
           
        # MutableSequence 클래스를 상속했으므로, 구현해야함.
        def __delitem__(self, position): 
            del self._cards[position]
            
        # MutableSequence 클래스를 상속했으므로, 구현해야함.        
        def insert(self, position, value): 
            self._cards.insert(position, value)
```



## 11.7 ABC의 정의와 사용

- 다음의 상황을 가정

    웹사이트나 모바일 앱에서 광고를 무작위 순으로 보여주어야 하지만, 광고 목록에 들어 있는 광고를 모두 보여주기 전까지는 같은 광고를 반복하면 안 된다.

```python
import abc

class Tombola(abc.ABC):
    
    @abc.abstractmethod
    def load(self, iterable):
        """iterable에서 항목들을 추가한다."""
        
    @abc.abstractmethod
    def pick(self):
            """무작위로 항목을 하나 제거하고 반환.
            객체가 비어있을 때 이 메서드를 실행하면 'LookupError' 발생     
            """
    def loaded(self):
        """최소 1개의 항목이 있으면 True를 반환"""
        return bool(self.inspect())
    def inspect(self):
        """현재 안에 있는 항목들로 구성된 정렬된 튜플을 반환."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
                self.load(items)
                return tuple(sorted(items))
```

### 11.7.2 Tombola ABC 상속하기

```python
import random
from tombola import Tombola

class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)
        
    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)
        
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
            def __call__(self)
```

```python
import random
from tombola import Tombola

class LotteryBlower(Tombola):
    
    def __init__(self, iterable):
        self._balls = list(iterable)
        
    def load(self, iterable):
        self._balls.extend(iterable)
        
    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty BingoCage')
            return self._balls.pop(position)
        
    def loaded(self):
        return bool(self._balls)
    
    def inspect(self):
        return tuple(sorted(self._balls))

```

### 17.3 Tombola의 가상 서브클래스

구스 타이핑의 본질적인 기능은 어떤 클래스가 ABC를 상속하지 않더라도 그 클래스의 **가상 서브클래스**로 등록할 수 있다는 것이다. 이렇게 함으로써 이 클래스가 ABC에 정의된 인터페이스를 충실히 구현한다고 약속하는 것이다. 그리고 파이썬은 검사하지 않고 우리를 믿어준다. 그러나 우리가 거짓말을 하면 런타임 예외가 발생한다.

ABC의 `register()` 메서드를 호출하면 클래스가 등록된다. 등록된 클래스는 ABC의 가상 서브클래스가 되어 issubclass()와 isinstance() 함수에 의해 인식되지만, ABC에서 상속한 메서드나 속성은 전형 없다.

```python
from random import randrange
from tombola import Tombola

@Tombola.register 
class TomboList(list): 
    
    def pick(self):
        if self: 
            position = randrange(len(self))
            return self.pop(position) 
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend
            
    def loaded(self):
        return bool(self) 
    
    def inspect(self):
        return tuple(sorted(self))
```

Tomblist는 Tombola의 서브클래스인것 처럼 판단된다.



## 11.10 오리처럼 행동할 수 있는 거위

`__subclasshook__()`은 구스 타이핑에 약간의 덕 타이핑 유전자를 추가한다. ABC를 이용해서 공식적으로 인터페이스를 정의할 수 있고, 어디에서든 `isinstance()` 검사를 할 수 있다. 또 어떤 메서드를 구현하기만 하면, 전혀 상관없는 클래스들이 함께 어울리게 만들 수 있다.

```python
class Sized(metaclass=ABCMeta):
    
    __slots__ = ()
    
    @abstractmethod
    def __len__(self):
        return 0
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__): 
                return True 
        return NotImplemented 
```

