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

# 2.1 sequence -> container sequence(list, tuple, collections..) -> 객체 참조
# 균일 sequence -> str, bytes, bytearray, memoryview, array.array -> 메모리 주소에 값을 직접 담음

# 2.2 list comprehension->가독성 굿, 가끔은 속도도 굿

# version 1
symbols1 = "!@#$%"
codes = []
for symbol in symbols1:
    codes.append(ord(symbol))

# version 2
symbols2 = "!@#$%"
codes2 = [ord(symbol) for symbol in symbols2]

# -> version 2 가 가독성이 좋음
# 반드시 사용할 리스트만 지능형 리스트로 만들자! 나중엔 더 복잡해질수도 있는 단점, 코드 짧게 해야 장점이 살아남
# 람다는 기능적으로 문제가 있다? 하지만 문제가 뭔지는 안나옴..
# filter, map 함수를 사용하는 것보다 지능형 리스트가 더 깔끔하고 빠름

# 지능형 리스트를 이용한 데카르트 곱
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors
           for size in sizes]  # python 은 괄호 내 개행 무시함. 지능형 리스트에서 조건을 줄맞춰 써놓으면 뭐가 먼저 나올지 알아보기 편함

# 지능형 리스트는 리스트만 만듦

# 제너레이터 표현식
# 지능형 리스트와 동일한 구문 사용, but 대괄호 대신 괄호
# 제너레이터 표현식은 한번에 하나의 항목을 생성하므로 리스트를 불필요하게 생성하지 않음
symbols = "!@#$%"
tuple(ord(symbol) for symbol in symbols)
import array

array.array('I', (ord(symbol) for symbol in symbols))

# 2.3 tuple - 언팩킹 까지
'''tuple 은 record 기능도 있음, for loop 에서 %s 등 쓸때 언팩킹도 가능함. 더미변수 쓸때는 _ 사용'''

# 튜플 언팩킹 = 반복형 언팩킹 = 한번에 하나의 항목을 생성함
# 병렬 할당할 때 하나의 변수에 하나씩 할당됨

lax_coordinates = (33.9534, -118.34235)
latitude, longitude = lax_coordinates

divmod(20, 8)
t = (20, 8)
print(divmod(*t))
quotient, remainder = divmod(*t)

# unpacking으로 함수 호출자에 여러 값을 간단히 반환 가능

# * 사용하여 초과항목 잡기

a, b, *rest = range(5)
print(a, b, rest)
a, *body, c, d = range(5)
print(a, body, c, d)

# tuple 은 다른 튜플을 내포할 수 있음
metro_areas = [
    ('Tokyo', 'JP', 36.033, (35.236325, 124.15325)),
    ('Delhi NCR', 'IN', 21.1253, (23.1235235, -19.23523))
]

print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long'))  # cell 제목 만들기 위한 양식 확립
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:  # 마지막을 튜플로 할당하여 언팩킹
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))  # formatting 으로 미리 양식 지정해놓고 나중에 조건으로 삽입 가능함!!

# 2.3.4. 명명된 tuple
# 예제 1.1 Card = collections.namedtuble('Card, ['rank', 'suit'])

from collections import namedtuple

City = namedtuple('City', 'name country population coordiates')  # string 이 자동으로 split 되어 명명됨
# 명명된 튜플은 class명과 field 명의 리스트로 2개의 매개변수가 필요함
tokyo = City('Tokyo', 'JP', 36.044, (2351235, 1236123))
print(tokyo)

print(tokyo.population)
Latlong = namedtuple('Latlong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 124125, Latlong(2351235, 124124))
delhi = City._make(delhi_data)  # City class 이용해서 delhi field 생성 = City(*delhi_data)
print(delhi._asdict())  # delhi 의 object data 를 반환함 by dictionary.
for key, value in delhi._asdict().items():
    print(key + ':', value)

# 2.3.5. 불변 list 로써의 tuple
# 추가, 삭제, reverse 빼고 list 와 같은 method 사용

# 2.4. slicing
'''slicing 시 마지막 항목이 포함되지 않으면서 생기는 장점
1. 마지막 점만 이용해서 범위를 지정할 때 길이를 계산하기 쉬움
2. 마지막 점에서 시작점을 빼면 역시 길이를 계산하기 쉬움
3. x 인덱스를 기준으로 겹침 없이 시퀀스를 분할하기 쉬움 (ex) [:x] , [x:]

a:b:c 표기법은 [] 안에서만 사용 가능, -> slice(a, b, c)
seq[start:stop:step] -> seq.__getitem__(slice(start, stop, step)) calling
slice 객체를 알면 각 슬라이스에 이름을 붙일 수 있게 해준다

SKU = slice(0, 6)
Description = slice(6, 40)
Unit_price = slice(40, 52)
Quantity = slice(52, 55)
Item_total = slice(55, None)
line_items = invoice.split('\n')[2:]
for item in line_items:
    print(item[Unit_price], item[Description]) -> slicing 에 이름을 붙여서 가독성이 매우 좋아짐

'''

# __getitem__() 또는 __setitem__() which are perform [] calculator -> a[i, j] 를 tuple로 받음
# a[i,j] -> __getitem__((i,j))

# ... 생략 기호는 ellipsis 클래스의 객체임, Ellipsis 로 명칭을 사용
# 생략기호는 f(a, ..., z) or a[i:...] 처럼 슬라이스의 한 부분으로 사용 가능
# in Numpy, x[i, ...] == x[i, :, :, :] where x has 4 dimentional complex
# slicing 은 value extraction 뿐 아니라 가변 시퀀스(list 같은) 의 값을 변경할 때도 사용할 수 있음

l = list(range(10))
print(l)
l[2:5] = [20, 30]
print(l)
del l[5:7]
print(l)
l[3::2] = [11, 22]
print(l)
l[2:5] = [100]  # 할당의 대상이 slice 인 경우 우변도 반복 가능한 객체가 와야 함
print(l)

# 2.5. 덧셈과 곱셈 연산자
# 덧셈 곱셈은 피연산자를 변경하지 않고 객체를 새로 만들어냄

board = [['_'] * 3 for i in range(3)]
print(board)
board[2][1] = 'X'
print(board)
# 위의 코드는 아래의 코드와 본질적으로 똑같이 작동함
board = []
for i in range(3):
    row = ['_'] * 3  # 반복할 때마다 row 객체를 새로 만들어서 추가함 -> 객체가 따로 작동함
    board.append(row)

print(board)

weird = [['_'] * 3] * 3  # 3개가 모두 동일한 객체를 참조하므로 3개의 내포된 list 를 따로 사용할 수 없음
print(weird)
weird[2][1] = 'X'
print(weird)
# 위의 코드는 아래의 코드와 본질적으로 똑같이 작동함
row = ['_'] * 3
board = []
for i in range(3):
    board.append(row)  # 같은 row 를 3번 반복하여 추가함

print(board)

# 2.6. 시퀀스의 복합 할당
# += 특수 메서드는 __iadd__(). 만약 __iadd__() 없으면 __add__() 호출
# 차이점 -> __iadd__() 는 객체를 직접 변경, __add__() 는 객체를 새로 생성한 후 다시 할당
# 불변 시퀀스는 객체를 새로 생성하여 계산 실행함->비효율적임 but str 만 다름
# tuple 에 내포된 list 는 extend 로 오류 없이 추가 가능함 t= (10, 20, [30, 40]) 의 경우 t[2].extend([50, 60])
# 튜플에 가변항목을 넣는것은 별로 좋지 않음, += 연산은 더하기 먼저 진행 후 할당이 진행됨(tuple 가변항목이 변경되고 할당이 되지 않음)

# 2.7. list.sort() -> in-place 함수 (바로 그 자리에서 list 정렬) -> list 변함
# 객체를 직접 변경하는 함수나 메서드는 객체 변경되고 새로운 객체가 생성되지 않음을 보이기 위해 None 을 반환함
# fluent interface 에 대한 자세한 설명 공부 필요
# sorted() 함수는 새로운 list 를 생성하여 반환 -> 반복 가능한 모든 개체를 인수로 받을 수 있음
fruits = ['strawberry', 'apple', 'banana']
print(sorted(fruits))
print(fruits)
print(sorted(fruits, reverse=True))
print(sorted(fruits, key=len))
print(sorted(fruits, key=len, reverse=True))
print(fruits)
fruits.sort()
print(fruits)

# 2.8. bisect로 관리
import bisect
import sys

haystack = [1, 3, 4, 5, 6, 7, 8, 9, 5, 410]
needles = [0, 1, 2, 5, 6, 8, 9, 23]

row_fmt = '{0:2d} @ {1:2d}     {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(needles):
        position = bisect_fn(haystack, needle)  # haystack 안에서 needle 의 삽입 위치 찾아내기
        offset = position * '  |'  # position 비례해서 | 만들기
        print(row_fmt.format(needle, position, offset))  # raw format 과 삽입위치를 보여주는 행을 출력


if __name__ == '__main__':
    if sys.argv[-1] == 'left':  # 마지막 명령행 인수에 따라 사용할 bisect 함수를 선택
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect

print('DEMO:', bisect_fn.__name__)  # 사용한 함수의 이름을 출력
print('haystack ->', ' '.join('%2d' % n for n in haystack))
demo(bisect_fn)


# bisect_right (default) -> 리스트 항목이 needle 과 같을 경우 항목 바로 뒤에 삽입
# bisect_left -> 삽입 위치에 넣고 원래 항목을 뒤로 한칸 밈

def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)  # breakpoint 에 따라 score 를 0,1,2,3,4 로 indexing
    return grades[i]  # indexing 된 position 에 따라 성적 반환


print([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])

# 정렬 후 정렬상태를 유지하는 함수 = bisect.insort()
# insort(seq, item) -> seq 을 오름차순 유지한 채로 item을 삽입

import bisect
import random

SIZE = 7

random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE + 2)  # 새 item 을 random 생성
    bisect.insort(my_list, new_item)  # my_list 의 오름차순 유지한 채로 new_item 삽입
    print('%2d ->' % new_item, my_list)

# 숫자로 구성된 리스트를 다루고 있다면 배열을 사용하는 것이 더 좋다!

# 2.9 리스트가 답이 아닐 때
'''실수를 천만개 저장해야 할 때->배열이 효율적(array.array)
리스트 양쪽 끝에 항목을 계속 추가하거나 삭제할때는 덱(deque)->양쪽을 사용하는 큐 가 더 빠름'''

'''배열은 메서드에 추가로 frombytes() tofile() 도 사용 가능함
배열 생성 시에는 c 기반 형을 결정하는 문자를 지정한다(타입코드)
'''

from array import array
from random import random

floats = array('d', (random() for i in range(10 ** 7)))  # typecode 'd' = 배밀도 실수
print(floats[-1])  # 배열의 마지막 숫자를 조사함
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10 ** 7)
fp.close()
print(floats2[-1])
print(floats2 == floats)

# pickle 모듈도 공부해야 함...숫자 데이터를 빠르고 융통성 있게 저장할 수 있음
# 배열을 정렬하려면 sorted 함수를 호출하여 배열을 다시 만들어야 함 a = array.array(a, typecode, sorted(a))
# 배열에 정렬을 유지하면서 추가하려면 bisect.insort() 이용

# 2.9 메모리뷰
# 바이트를 이동시키지 않고 c언어의 형변환 연산자처럼 여러바이트로 된 데이터를 읽거나 쓰는 방식을 바꿀수 있게 해준다.

import array

numbers = array.array('h', [-2, -1, 0, 1, 2])  # 짧은 정수(typecode 'h') 다섯 개가 있는 배열
memv = memoryview(numbers)
print(len(memv))
print(memv[0])
memv_oct = memv.cast('B')  # unsigned char 로 변환
print(memv_oct.tolist())  # memv_oct 안의 요소를 리스트로 변환
memv_oct[5] = 4
print(numbers)

# 2.9.3 numpy, scipy
'''import numpy
a = numpy.arange(12)
a
Out[4]: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
type(a)
Out[5]: numpy.ndarray
a.shape
Out[6]: (12,)
a.shape = 3, 4
a
Out[8]: 
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
a[2]
Out[9]: array([ 8,  9, 10, 11])
a[2,1]
Out[10]: 9
a[:,1]
Out[11]: array([1, 5, 9])
a.transpose()
Out[12]: 
array([[ 0,  4,  8],
       [ 1,  5,  9],
       [ 2,  6, 10],
       [ 3,  7, 11]])

import numpy
floats = numpy.loadtxt('floats-10M-lines.txt')
floats[-3:]
floats *= 0.5
from time import perf_counter as pc
t0 = pc(); floats /=3; pc() -t0 # 시간측정'''

# 2.9.4. 덱 및 기타 큐

# append() pop() 은 리스트 끝에 대해 연산 가능. but list[0] 에 대해서는 리스트 전부를 옮겨야 하므로 부담 큼
# 덱(collections.deque) = 양쪽으로 빠르게 컨트롤 가능, 만약 최대길이를 설정하면, 덱이 꽉 찬 후 반대 항목을 버림

from collections import deque

dq = deque(range(10), maxlen=10)
print(dq)
dq.rotate(3)
print(dq)
dq.rotate(-4)
print(dq)
dq.appendleft(-1)
print(dq)
dq.extend([11, 22, 33])
print(dq)
dq.extendleft([10, 20, 30, 40])  # 왼쪽에 역순으로 추가
print(dq)
# 덱의 중간을 삭제/삽입하는 연산은 빠르지 않음
# queue = 공간이 꽉 찼을 때 항목을 버리지 않고 추가를 블로킹, 다른 스레드에서 항목을 제거해서 공간확보할 때까지 기다림.










