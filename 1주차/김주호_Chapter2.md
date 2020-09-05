# Chap2. 시퀀스(요약 먼저)

  표준 라이브러리에서 제공하는 시퀀스형을 제대로 파악하고 있어야 간결하고, 효율적이며, 파이썬스러운 코드를 작성할 수 있다.

  파이썬 시퀀스는 가변형과 불변형으로 구분하기도 하지만, 균일 시퀀스와 컨테이너 시퀀스로 분류하는 것도 도움이 된다. 

- 균일(flat) 시퀀스 : 
    - 단 하나의 자료형만을 담을 수 있는 str, bytes, bytearray, memoryview, array.array 형
    - 작고, 빠르고, 사용하기 쉽지만 숫자, 문자, 바이트처럼 원자적인 데이터만 저장할 수 있다. 
- 컨테이너(container) 시퀀스 : 
    - 서로 다른 자료형의 항목을 담을 수 있는 list, tuple, collections.deque 형
    - 융통성이 있지만, 가변 객체를 저장할 때는 예상치 못한 일이 발생할 수도 있다. 따라서 내포된 데이터 구조체와 함께 컨테이너 시퀀스를 사용할 때는 주의해야 한다.

  **지능형 리스트(list comprehension)**와 **제너레이터 표현식(generator expression)**은 시퀀스를 생성하고 초기화하는 강력한 표기법이다. 

  파이썬에서 제공하는 **튜플**은 

- 불변 리스트(immutable list)
- 익명 필드를 가진 레코드
    - 튜플 언패킹 : 필드에 접근하는 가장 안전하고 가독성 좋은 방법
    - \* 구문 : 일부 필드를 무시하거나 선택적 필드를 처리하기 상당히 좋다
    - 명명된 튜플(namedtuple) : 
        - 튜플처럼 객체당 오버헤드가 적다.
        - 이름을 이용해서 간단히 필드에 접근한다.
        - \_asdict() 메서드를 사용하면 레코드를 OrderedDict 객체로 export할 수 있다.

로 사용할 수 있다. 

  시퀀스 슬라이싱은 사람들이 흔히 알고 있는 것보다 훨씬 더 강력하다.  Numpy에서 사용되는 다차원 슬라이싱과 생략 기호(...) 표기도 사용자 정의 시퀀스에서 지원할 수 있다. 슬라이스에 할당하는 구문은 가변 시퀀스의 편집을 멋지게 표현한다.

  seq*n 으로 표현되는 **반복 연결**은 편리하게 사용할 수 있으며, 주의해서 사용하면 가변 항목을 담은 리스트의 리스트를 초기화할 수도 있다. +=와 *= 복합 할당 연산자는 가변/불변 시퀀스 여부에 따라 다르게 작동한다. 복합 할당 연산자는 

- 대상 시퀀스가 불변인 경우 : 새로운 시퀀스를 생성
- 대상 시퀀스가 가변인 경우 : 대상 시퀀스를 직접 변경

  하지만 시퀀스 구현 방식에 따라 그러지 않을 수도 있다.



  sort() 메서드와 sorted() 내장 함수는 사용하기 쉬우며, 선택적인 key 인수에 정렬 기준을 계산하는 **함수**를 지정할 수 있으므로 융통성도 뛰어나다. 한편, key는 min()과 max() 내장 함수와도 사용할 수 있다. 정렬된 시퀀스의 순서를 유지하면서, 항목을 추가하려면 **bisect.insort()** 메서드를 사용하고, 정렬된 시퀀스를 효율적으로 검색하려면 **bisect.bisect()** 메서드를 사용하라.

  파이썬 표준 라이브러리는 리스트와 튜플 외에 array.array도 제공한다. Numpy와 SciPy는 표준 라이브러리에 속해 있지 않지만, 대형 데이터셋에 수치 연산을 수행하는 경우에는 이런 라이브러리를 약간만 알아두어도 큰 도움이 된다. 

  마지막으로 기능이 풍부하고 스레드 안전한 collections.deque에 대해 살피고, 리스트 vs API, 표준 라이브러리에서 구현하는 여러 큐 클래스에 대해 간략히 본다.

## 2.4.2 slice 객체 예제


```python
invoice = """
0.....6.................................40........52...55........
1909  Pimoroni PiBrella                     $17.50    3    $52.50
1489  6mm Tactile Switch x20                $4.95     2    $9.90
1510  Panavise Jr. - PV-201                 $28.00    1    $28.00
1601  PiTFT Mini Kit 320x240                $34.95    1    $34.95
"""
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
QUANTITY = slice(52, 55)
ITEM_TOTAL = slice(55, None)

line_items = invoice.split('\n')[2:]

if __name__ == "__main__":
    for item in line_items:
        print(item[UNIT_PRICE], item[DESCRIPTION])
```

        $17.50   Pimoroni PiBrella                 
        $4.95    6mm Tactile Switch x20            
        $28.00   Panavise Jr. - PV-201             
        $34.95   PiTFT Mini Kit 320x240            


​    

## 2.5.1 리스트의 리스트 만들기


```python
board = [['_']*3 for i in range(3)]
print(board)
board[1][2] = 'X'
print(board)

print("==================================================")

weird_board = [['_']*3]*3
print(weird_board)
weird_board[1][2] = '0'
print(weird_board)  # 동일한 리스트에 대한 3개의 참조를 가진 리스트가 되었다.
```

    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    [['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]
    ==================================================
    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    [['_', '_', '0'], ['_', '_', '0'], ['_', '_', '0']]



```python
# board를 만드는 지능형 리스트(list comprehension)는 다음과 같이 작동한다.
board =[]
for i in range(3):
    row = ['_']*3
    board.append(row)
print(board)

# weird_board를 만든 코드는 다음과 같이 작동한다.
row = ['_']*3
board = []
for i in range(3):
    board.append(row)
print(board)

print("겉보기에만 같다")
```

    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    겉보기에만 같다


## 2.8.1 bisect()로 검색하기


```python
import bisect

def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]

if __name__ == "__main__":
    print([grade(score) for score in [33, 99, 77, 89, 90, 100]])
```

    ['F', 'A', 'C', 'B', 'A', 'A']


## 2.8.2 bisect.insort()로 삽입하기


```python
import bisect
import random

SIZE = 8

random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)
```

     1 -> [1]
    13 -> [1, 13]
    14 -> [1, 13, 14]
     5 -> [1, 5, 13, 14]
     1 -> [1, 1, 5, 13, 14]
     5 -> [1, 1, 5, 5, 13, 14]
     9 -> [1, 1, 5, 5, 9, 13, 14]
    11 -> [1, 1, 5, 5, 9, 11, 13, 14]


## 2.9.1 배열

  파이썬 배열은 C 배열만큼 가볍다. 배열을 생성할 때는 배열에 저장되는 각 항목의 C 기반 형을 결정하는 문자인 타입코드를 지정한다. 숫자가 아주 많이 들어 있는 시퀀스의 경우 배열에 저장하면 메모리가 많이 절약된다. 그리고 파이썬은 배열형에 맞지 않는 숫자를 저장할 수 없게 한다.


```python
from array import array
from random import random

floats = array('d', (random() for i in range(10**7)))

fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

print(floats[-1])

floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close

print(floats2[-1])

print(floats2 == floats)
```

    0.24967540607910887
    0.24967540607910887
    True


## 2.9.2 메모리 뷰
메모리 뷰(memoryview) 내장 클래스는 공유 메모리 시퀀스형으로서 bytes를 복사하지 않고 배열의 슬라이스를 다룰 수 있게 해준다. 데이터셋이 커지는 경우 이것은 아주 중요한 기법이다.


```python
import array 

numbers = array.array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
len(memv)

memv_oct = memv.cast('B')
print(memv_oct.tolist())

memv_oct[5] = 4
print(numbers)
```

    [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
    array('h', [-2, -1, 1024, 1, 2])


## 2.9.4 덱 및 기타 큐

덱(collections.deque) 클래스는 큐의 양쪽 어디에서든 빠르게 삽입 및 삭제할 수 있도록 설계된 스레드안전한(thread-safe) 양방향 큐다. 덱은 최대 길이를 설정해서 제한된 항목만 유지할 수도 있으므로 덱이 꽉 찬 후에는 새로운 항목을 추가할 때 반대쪽 항목을 버린다.


```python
from collections import deque
dq = deque(range(10), maxlen=10)

dq.rotate(3)
print(dq)

dq.appendleft(-1)
print(dq)

dq.extend([11, 22, 33])
print(dq)

dq.extendleft([10, 20, 30])
print(dq)
```

    deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
    deque([-1, 7, 8, 9, 0, 1, 2, 3, 4, 5], maxlen=10)
    deque([9, 0, 1, 2, 3, 4, 5, 11, 22, 33], maxlen=10)
    deque([30, 20, 10, 9, 0, 1, 2, 3, 4, 5], maxlen=10)