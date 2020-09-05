# 1주차
# Chapter 1. 파이썬 데이터 모델(요약 먼저)
  이 챕터는 \_\_repr\_\_() 등의 특별한 메서드가 모든 형의 객체 행동을 일관성 있게 유지하는 데 핵심적인 역할을 하는 과정을 설명한다. 파이썬은 일관성으로 존경받는 언어이다. 
  특별 메서드를 구현하면, 사용자 정의 객체도 내장형 객체처럼 작동하게 되어, 파이썬스러운(pythonic) 표현력 있는 코딩 스타일을 구사할 수 있다. 

  파이썬 객체는 기본적으로 자신을 '문자열' 형태로 제공해야 하는데, 

- 디버깅 및 로그에 사용하는 형태
- 사용자에게 보여주기 위한 형태

2가지가 있다. 그렇기 때문에 데이터 모델에 \_\_repr\_\_()과 \_\_str\_\_() 특별 메서드가 있는 것이다.

## 파이썬 카드 한 벌 예제


```python
import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
    
if __name__ == '__main__':
    beer_card = Card('7', 'diamonds')
    print(beer_card)
    
    # __init__()
    deck = FrenchDeck()
    # __len__()
    print(len(deck))
    # __getitem__()
    print(deck[0])
    
    print(choice(deck))
```

    Card(rank='7', suit='diamonds')
    52
    Card(rank='2', suit='spades')
    Card(rank='10', suit='clubs')


## 특별 메서드를 사용하는 방법에 관한 예제


```python
from math import hypot

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)
    
    def __abs__(self):
        return hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    
if __name__ == "__main__":
    print(Vector(1,2)+Vector(3,4))
```
