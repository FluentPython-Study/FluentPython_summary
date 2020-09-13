#Chaper 1

# __getitem__() -> 특별 메서드 (던더 getitem 으로 발음)
# 특별 메서드는 interpreter 가 호출하기 위해 필요한 것임.

# 1.1 카드 한벌 구현
import collections

Card = collections.namedtuple('Card', ['rank', 'suit']) # 개별 카드를 나타내는 클래스 구현 ->Card(rank, suit) tuple 로 구현, global 변수

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA') # card number 구현 2~10, JQKA in rank 변수
    suits = 'Spades Diamonds Clubs Hearts'.split() # Card 무늬 표시, split 으로 각자 나눔

    def __init__(self): # Card 변수에서 입력된 값 사용하여 카드 변수 생성 ->chapter 2 지능형리스트 사용함. 데카르트곱!
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self): # 갖고 있는 카드의 수 반환
        return len(self._cards)

    def __getitem__(self, position): # 카드 indexing, 카드는 2~A 로 순서대로, Spade ~ 순서대로
        return self._cards[position]



beer_card = Card('7', 'Diamonds')
print (beer_card)

deck = FrenchDeck()
print (len(deck))

print(deck[0])
print(deck[1])

from random import choice # random card 뽑기
print (choice(deck))
print (choice(deck))
print (choice(deck))
print (choice(deck))

# 특별 메서드를 class 에 구현하면 굳이 메서드명을 외울 필요 없다 -> very good!
# 파이썬에서 기능 별도 구현 필요없음


for card in deck:
    print (card)

for card in reversed(deck):
    print (card)

print (Card('Q', 'Hearts') in deck)

print (Card('J', 'Beasts') in deck)

suit_values = dict(Spades = 3, Hearts = 2, Diamonds = 1, Clubs = 0)
# dictionary 표현할 때 {key:item} 으로 표현하지 않아도 이런 방법으로 표현 가능, 타자치기 더 쉬움!

def Spades_high(card): # card number 와 모양으로 card 별로 숫자 ranking
    rank_value = FrenchDeck.ranks.index(card.rank)  # FrenchDeck class 로 선언된 카드의 rank 순서를 indexing 하여 value 매김
    return rank_value * len(suit_values) + suit_values[card.suit]
    # 숫자별로 indexing 한 것을 모양 종류에 곱하여 숫자에 ranking + 모양 별 가산점 부여


for card in sorted(deck, key=Spades_high):
    print (card)

# for i in x: -> iter(x) 호출하는 것 -> x.__iter__() 호출하는 것임
# 특별 메서드 호출이 필요할 경우 일반적으로 파이썬 내장함수를 호출하는 것이 더 좋음(len(), str(), iter() 등)
# 사용자정의 속성을 만들 때 __xxx__ 는 피하는 것이 좋음

# 1.2 수치형 흉내

from math import hypot

class Vector:
    def __init__(self, x=0, y=0): # 그냥 self, x, y 로 주면 안되는 건지? x=0, y=0 으로 주는 이유는? x, y 변수가 numeric 이라서?
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)
    '''왜 %r 을 사용하는가?%r 과 %s 는 모두 문자열을 출력함. %s -> str() but %r -> repr(), official string representation 함.
    http://satyajit.ranjeev.in/2012/03/14/python-repr-str.html
    When I use the built-in function str() to display today:

>>> str(today)
'2012-03-14 09:21:58.130922'
You can see that the date was displayed as a string in a way that the user can understand the date and time. Now lets see when I use the built-in function repr():

>>> repr(today)
'datetime.datetime(2012, 3, 14, 9, 21, 58, 130922)'
You can see that this also returned a string but the string was the “official” representation of a datetime object. What does official mean? Using the “official” string representation I can reconstruct the object:

>>> eval('datetime.datetime(2012, 3, 14, 9, 21, 58, 130922)')
datetime.datetime(2012, 3, 14, 9, 21, 58, 130922)

Most functions while trying to get the string representation use the __str__ function, 
if missing uses __repr__. Thus in a general every class you code must have a __repr__ and 
if you think it would be useful to have a string version of the object, 
as in the case of datetime create a __str__ function.'''

    def __abs__(self): # vector 크기 검출 -> 피타고라스 정리 이용하여 계산함 -> hypot 함수
        return hypot(self.x, self.y) # a = sqrt(x**2 +y**2), hypot 함수를 매일 호출해야 하므로 직접 수식을 써서 하면? 어차피 sqrt 등 필요'''

    def __bool__(self): # vector 의 크기가 0 이면 False 반환 -> bool 함수가 없으면 python은 len 함수 이용
        return bool(abs(self))

    def __add__(self, other): # vector 합
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar): # vector scalar 곱, vector * 숫자는 가능하지만 숫자 * vector 는 불가능함. 교환법칙을 어겼음.
        return Vector(self.x * scalar, self.y * scalar)


# Chapter 2

#2.1 sequence -> container sequence(list, tuple, collections..) -> 객체 참조
# 균일 sequence -> str, bytes, bytearray, memoryview, array.array -> 메모리 주소에 값을 직접 담음

#2.2 list comprehension->가독성 굿, 가끔은 속도도 굿

#version 1
symbols1 = "!@#$%"
codes = []
for symbol in symbols1:
    codes.append(ord(symbol))

#version 2
symbols2 = "!@#$%"
codes2 = [ord(symbol) for symbol in symbols2]

#-> version 2 가 가독성이 좋음
# 반드시 사용할 리스트만 지능형 리스트로 만들자! 나중엔 더 복잡해질수도 있는 단점, 코드 짧게 해야 장점이 살아남
#람다는 기능적으로 문제가 있다? 하지만 문제가 뭔지는 안나옴..
#filter, map 함수를 사용하는 것보다 지능형 리스트가 더 깔끔하고 빠름

#지능형 리스트를 이용한 데카르트 곱
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors
                         for size in sizes] # python 은 괄호 내 개행 무시함. 지능형 리스트에서 조건을 줄맞춰 써놓으면 뭐가 먼저 나올지 알아보기 편함

#지능형 리스트는 리스트만 만듦

# 제너레이터 표현식
#지능형 리스트와 동일한 구문 사용, but 대괄호 대신 괄호
# 제너레이터 표현식은 한번에 하나의 항목을 생성하므로 리스트를 불필요하게 생성하지 않음
symbols = "!@#$%"
tuple(ord(symbol) for symbol in symbols)
import array
array.array('I', (ord(symbol) for symbol in symbols))

#2.3 tuple - 언팩킹 까지
'''tuple 은 record 기능도 있음, for loop 에서 %s 등 쓸때 언팩킹도 가능함. 더미변수 쓸때는 _ 사용'''

#튜플 언팩킹 = 반복형 언팩킹 = 한번에 하나의 항목을 생성함
#병렬 할당할 때 하나의 변수에 하나씩 할당됨








