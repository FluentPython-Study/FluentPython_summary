# Chap 3. 딕셔너리와 집합 (요약 먼저)

  딕셔너리는 파이썬의 핵심이다. 기본적인 dict 외에 표준 라이브러리에서는 defaultdict, OrderedDict, ChainMap, Counter 등 바로 사용할 수 있는 간편한 매핑형을 제공한다. 이 딕셔너리들은 모두 collections 모듈에 정의되어 있다. collections 모듈은 확장이 쉬운 UserDict 클래스도 제공한다.

   대부분의 매핑형은

- **setdefault()** : 검색 키가 존재하면 해당 키에 대한 값을 가져오고, 존재하지 않으면 기본값으로 해당 키를 생성한 후 기본값을 반환한다.
- **update()** : 다른 매핑형, 키-값 쌍을 제공하는 반복형, 키워드 인수로부터 항목을 가져와서 대량으로 데이터를 추가하거나 덮어쓸 수 있다. 매핑 생성자도 내부적으로 update() 메서드를 사용하므로 매핑형, 반복형, 키워드 인수로부터 객체를 초기화할 수 있다.



  매칭 API에서 제공하는 \_\_missing\_\_() 메서드는 멋진 연결고리로서, 키를 찾을 수 없을 때 발생하는 일을 정의할 수 있게 해준다.



  collections.abc 모듈은 참조와 자료형 검사를 위해 Mapping과 MutableMapping 추상 베이스 클래스를 제공한다. types 모듈에서 제공하는 MappingProxyType 클래스는 잘 알려져 있지 않지만, 불변형 매핑을 생성한다. 그리고 Set과 MutableSet에 대한 추상 베이스 클래스도 제공한다.

  dict와 set의 기반이 되는 **해시 테이블**은 상당히 빠르다. 해시 테이블을 이해하면 항목들의 순서가 정렬되어 있지 않은 이유 및 심지어 조용히 재정렬되는 이유를 알 수 있다. 해시 테이블은 속도가 빠른 반면 메모리 공간을 많이 사용한다.



## 3.3 공통적인 매핑 메서드

### 3.3.1 존재하지 않는 키를 setdefault()로 처리하기


```python
somelist = ['a', 'b', 'c', 'b', 'a', 'b', 'c']
result = {}

for i in somelist:
    result.setdefault(i, 0)
    result[i] += 1
    print(result)
```

    {'a': 1}
    {'b': 1, 'a': 1}
    {'b': 1, 'c': 1, 'a': 1}
    {'b': 2, 'c': 1, 'a': 1}
    {'b': 2, 'c': 1, 'a': 2}
    {'b': 3, 'c': 1, 'a': 2}
    {'b': 3, 'c': 2, 'a': 2}


## 3.4 융통성 있게 키를 조회하는 매핑
### 3.4.1 defaultdict : 존재하지 않는 키에 대한 또 다른 처리


```python
from collections import defaultdict

int_dict = defaultdict(int)
print(int_dict)
int_dict['key1']
```

    defaultdict(<class 'int'>, {})


### 3.4.2 \_\_missing\_\_() 메서드


```python
class StrKeyDict0(dict):

    def __missing__(self, key):
        if isinstance(self, str):   # 빈 문자열 입력
            raise KeyError(key)  
        return self[str(key)]
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
        
    def __contains__(self, key):
        return str(key) in self.keys()
    
if __name__ == "__main__":
    d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    print(d['2'])
    print(d[4])
    print(2 in d)
```

    two
    four
    True


## 3.5 그 외 매핑형 :collections.Counter


```python
import collections

ct = collections.Counter('baabracadabra')
print(ct)

ct.update('aaaaaazzzz')
print(ct)

print(ct.most_common(3))
```

    Counter({'a': 6, 'b': 3, 'r': 2, 'c': 1, 'd': 1})
    Counter({'a': 12, 'z': 4, 'b': 3, 'r': 2, 'c': 1, 'd': 1})
    [('a', 12), ('z', 4), ('b', 3)]


## 3.6 UserDict 상속하기

  dict보다는 Userdict를 상속해서 매핑형을 만드는 것이 쉽다. 내장형에서는 아무런 문제없이 상속할 수 있는 메서드들을 오버라이드해야 하는 구현의 특이성 때문에 dict보다는 Userdict를 상속하는 것이 낫다. (내장형 상속은 뭔가 까다롭다고 한다 -> 12장)
  UserDict는 dict를 상속하지 않고 내부에 실제 항목을 담고 있는 data라고 하는 dict 객체를 갖고 있다. 이렇게 구현함으로써 \_\_setitem\_\_()등의 특수메서드를 구현할 때 발생하는 원치 않는 재귀적 호출을 피할 수 있으며, \_\_contains\_\_() 메서드를 간단히 구현할 수 있다.


```python
import collections

class StrKeyDict(collections.UserDict):
    
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def __contains__(self, key):
        return str(key) in self.data
    
    def __setitem__(self, key, item):
        delf.data[str(key)] = item
        
if __name__ == "__main__":
    d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    print(d['2'])
    print(d[4])
    print(2 in d)
```

    two
    four
    True


## 3.7 불변 매핑


```python
from types import MappingProxyType

d= {1: 'A'}

d_proxy = MappingProxyType(d)
print(d_proxy)

d_proxy[1] = 'B'
```

    {1: 'A'}



    ---------------------------------------------------------------------------
    
    TypeError                                 Traceback (most recent call last)
    
    <ipython-input-29-f02ac3445e8c> in <module>
          6 print(d_proxy)
          7 
    ----> 8 d_proxy[1] = 'B'


    TypeError: 'mappingproxy' object does not support item assignment


## 3.8 집합 이론

 집합 요소는 반드시 해시할 수 있어야 한다.

> *해시가능하다*
>
> 1. 객체의 수명 주기 동안 언제나 동일한 값을 반환하는 \_\_hash\_\_() 메서드를 제공해서 hash() 함수를 지원한다.
> 2. \_\_eq\_\_() 메서드를 통해 동치성을 판단할 수 있다.
> 3. a == b가 참이면, hash(a) == hash(b)도 반드시 참이어야 한다.

set은 해시 가능하지 않지만 frozenset은 해시 가능하므로, fozenset이 set에 들어갈 수 있다. 

  고유함을 보장하는 것 외에 집합형은 중위 연산자를 이용해서 기본적인 집합 연산을 구현한다. 집합 연산을 현명하게 이용하면 파이썬 프로그램의 소스 코드 크기와 실행 시간을 줄일 수 있을 뿐 아니라, 루프나 조건절이 없어지므로 코드의 가독성이 높아진다.



## 3.9 dict와 set의 내부 구조

### 3.9.2 딕셔너리 안의 해시 테이블

  해시 테이블은 희소 배열(sparse array)(중간에 빈 항목을 가진 배열)이다. 데이터 구조 교과서를 보면 해시 테이블 안에 있는 항목을 종종 '버킷(bucket)'이라고 한다. dict 해시 테이블에는 각 항목별로 버킷이 있고, 버킷에는 키에 대한 참조와 항목의 값에 대한 참조가 들어간다. 모든 버킷의 크기가 동일하므로 오프셋을 계산해서 각 버킷에 바로 접근할 수 있다.

  파이썬은 버킷의 1/3 이상을 비워두려고 노력한다. 해시 테이블 항목이 많아지면, 더 넓은 공간에 복사해서 버킷 공간을 확보한다. 



#### 해시 테이블 알고리즘

  my_dict[search_key]에서 값을 가져오기 위해 파이썬은 \_\_hash\_\_(search_key)를 호출해서 search_key의 해시값을 가져오고, 해시값의 최하위 비트를 해시 테이블 안의 버킷에 대한 오프셋으로 사용한다(사용하는 비트 수는 현재 테이블 크기에 따라 달라진다). 찾아낸 버킷이 비어있으면 KeyError를 발생시키고, 그렇지 않으면 버킷에 들어있는 항목인 (found_key : found_value) 쌍을 검사해서 search_key == found_key인지 검사한다. 이 값이 일치하면 항목을 찾은 것이므로 found_value를 반환한다.

  그렇지만 search_key와 found_key가 다른 경우에는 해시 충돌(hash collision)이 발생한 것이다. 해시 충돌은 해시 함수가 임의로 객체를 적은 수의 비트로 매핑하기 때문에 발생한다. 해시 충돌을 해결하기 위해 알고리즘은 해시의 다른 비트들을 가져와서 특정한 방식으로 조작한 후 그 결과를 이용해서 다른 버킷을 조회한다. 이떄 버킷이 비어 있으면 KeyError를 발생시킨다. 그렇지 않고 키가 일치하면 항목 값을 반환하고, 키가 일치하지 않으면 다시 충돌 해결 프로세스를 반복한다.

  항목을 추가하거나 갱신하는 과정도 동일하다. 다만 빈 버킷을 찾으면 새로운 항목을 추가하고, 동일한 키를 가진 버킷을 찾으면 버킷의 값을 새로운 값으로 갱신한다.

  그리고 항목을 추가할 때 해시 테이블에 항목이 너무 많다고 파이썬이 판단하면 더 큰 공간을 가진 새로운 위치에서 해시 테이블을 다시 만든다. 해시 테이블이 커지면 더 많은 해시 비트를 버킷 오프셋으로 사용하며, 더 많은 비트를 사용할수록 충돌률은 낮아진다.

  해시테이블을 이렇게 구현하려면 상당히 많은 작업이 필요할 것처럼 느껴지지만, dict 안에 수백만 개의 항목이 있어도 충돌 없이 검색되는 경우가 많으며, 한 번 검색할 때마다 발생하는 평균 충돌 횟수는 1에서 2 사이다. 일반적으로 운이 아주 안 좋은 키의 경우에도 몇 번의 충돌을 겪고 난 후에는 원하는 항목을 찾을 수 있다.

### 3.9.3 dict 작동 방식에 의한 영향

- 단점
    - 키 객체는 반드시 해시 가능해야한다.
    - dict의 메모리 오버헤드가 크다.
    - 딕셔너리에 항목을 추가하면 기존 키의 순서가 변경될 수 있다.
- 장점
    - 키 검색이 아주 빠르다
    - 키 순서는 삽입 순서에 따라 달라진다.



### 3.9.4 집합의 작동 방식 - 현실적으로 미치는 영향

  set과 frozenset도 해시 테이블을 이용해서 구현하지만, 각 버킷이 항목에 대한 참조만을 담고 있다는 점이 다르다(항목 자체가 dict에서의 키처럼 사용되지만, 이 키를 통해 접근할 값이 없다.) set이 파이썬 언어에 추가되기 전까지는 가짜 값을 가진 딕셔너리를 사용해서 키가 들어 있는지 빠르게 검색하곤 했다. set도 dict와 동일하게 작동하므로 dict의 특징을 그대로 갖는다.

- 단점
    - set 요소는 반드시 해시 가능해야한다.
    - set의 메모리 오버헤드가 상당히 크다.
    - 요소를 집합에 추가하면 다른 요소의 순서가 바뀔 수 있다.
- 장점
    - 집합에 속해 있는지 매우 효율적으로 검사할 수 있다.
    - 요소의 순서는 요소를 추가한 순서에 따라 달라진다.
