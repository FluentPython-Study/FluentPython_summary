#chapter 3
#dictionary
#dictionary 와 set 은 hash table engine 을 통해 구현됨
# 내장함수는 __builtiins__.__dict__ 에 있음

#키가 모두 해시 가능해야함!!!

# 수명 주기 동안 변하지 않는 해시값(__hash__() method) can compare with other object (__eq__() method)
# 해시 가능함
#튜플은 안에 들어있는 항목이 모두 해시 가능해야 해시 가능함
'''a=dict(one=1, two=2, three =3)
b = {'one':1, 'two':2, 'three':3}
c=dict(zip(['one', 'two', 'three'], [1,2,3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e=dict({'three':3, 'one':1, 'two':2}) 전부 dictionary 만드는 방법임'''

#지능형 딕셔너리 생성 가능
Dial_codes = [(86, 'c'),   (82, 'K'),
   (1, 'US'),
   (45, 'DK')
  ]

country_code = {country:code for code, country in Dial_codes}
print (country_code)
print ({code:country.upper() for country, code in country_code.items() if code<66})

# 메서드 확인 필요
'''update() method ->duck typing
if m gets keys() method, update() justify mapping
if m doesn't, update() think m is consist of (key, value) and repeat m

존재하지 않는 키 k 로 d[k] 접근시 dict 는 error. 
d[k] 대신 d.get[k, default] 사용 하여 keyerror 처리 회피'''

'''import sys
import re
#import collections

word_re = re.compile(r'\w+')
index = {}  #index = collections.defaultdict(list)

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in word_re.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location) #index[word].append(location)

for word in sorted(index, key=str.upper):
    print(word, index[word])
'''

#my_dict.setdefault(key, []).append(new_value)
'''== if key not in my_dict:
          my_dict[key] = []
       my_dict[key].append(new_value)'''

#defaultdict = 존재하지 않는 key 에 대한 처리방법
'''list() 호출
new-key 를 키로 사용해서 새로운 리스트 삽입
리스트 참조 반환
'''

#__missing__() method -> dict class 상속하면 key error 발생시키지 않음
#__getitem__() method 호출 시에만 __missing__() 호출
#get() or in method 는 영향 없음

class StrKeyDict0(dict):  #class 가 dict를 상속함

    def __missing__(self, key):
        if isinstance(key, str): #key 가 문자열이고 존재하지 않으면 keyerror ->없으면 stk(k) 가 있으면 항상 작동
            #but str(k) 없으면 무한 재귀적으로 호출
            raise KeyError(key)
        return self[str(key)] #key 를 문자열로 만들고 조회

    def get(self, key, default=None):
        try:
            return self[key] #__getitem__() method 에 위임함
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()
    # k in my_dict 로 호출하면 dict class 의 __contains__() 를 호출하므로 재귀적 호출 문제가 생김

d= StrKeyDict0([('2', 'two'), ('4', 'four')])


print (d.get(1, 'N/A'))
print (1 in d)

#UserDict 는 상속받아 써야 함, dict 보다 이걸 상속받는 게 mapping 에 좋음
#내장 class 는 오버라이드 해야 함..나중에 설명

import collections

class StrKeyDict(collections.UserDict): #UserDict 는 MutableMapping 상속함

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data #저장된 키가 모두 문자형이므로 바로 조회 가능

    def __setitem__(self, key, item):
        self.data[str(key)] = item #모든 키를 문자열 변환

# 결론적으로 StrKeyDict 는 모든 맵핑을 상속받게 되어 도든 기능을 갖게 된다
'''
from types import MappingProxyType
d = {1:'A'}
d_proxy = MappingProxyType(d)
d_proxy
Out[39]: mappingproxy({1: 'A'})
d_proxy[1]
Out[40]: 'A'
d_proxy[2]

TypeError: 'mappingproxy' object does not support item assignment
d[2] = 'B'
d_proxy
Out[44]: mappingproxy({1: 'A', 2: 'B'})
d_proxy[2]
Out[45]: 'B' 
'''

#3.8 set
# frozenset = 불변형집합
# set 은 해시가능하지 않지만 frozenset 은 해시 가능함 =>set 에 frozenset 포함 가능

'''found = len(needles & haystack) where needles and haystack are set type both.
위와 아래는 같은 동작 코드
found = 0
for n in needles: # needles and haystack become any object
    if n in haystack:
        found +=1
        
found = len(set(needles) & set(haystack)) or len(set(needles).intersection(haystack))
# needles and haystack become any object
'''

#집합은 {1, 2} 등의 표기, 공집합은 표기 못하므로 set() 으로 표기해야 함
# set([1,2,3]) 보다 {1, 2, 3} 으로 표기할 경우 BUILD_SET 특수 바이트코드를 이용하므로 더 빠름
#frozenset 은 언제나 frozenset([1,2,3]) 으로 생성해야 함
#지능형집합
from unicodedata import name
s = {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
print (s)

#3.9 dict/set 의 내부 구조
#해시테이블은 희소배열(sparse array), 중간에 빈 항목을 가진 배열 -> bucket
#dict hashtable 에 각 항목 별로 bucket 이 있고, bucket 에는 키에 대한 참조와 항목의 값에 대한 참조가 들어감
#my_dict[search_key] ->__hash__(search_key) -> value of search_key _>최하위비트를 버킷의 offset 으로 사용
#bucket 이 비어있으면 keyError, (found_key:found_value) -> found_key == search_key -> return found_value

#if found_key != search_key, 충돌해결 process 진행
#dict 는 공간 활용도는 좋지 않음
# 해시충돌이 일어나면 order 는 달라진다
# 딕셔너리를 반복하는 동안 딕셔너리 내용을 변경하는 것은 좋지 않은 방법
# 1. 처음부터 끝까지 딕셔너리 검색하면서 필요한 항목은 별도의 딕셔너리에 추가
# 2. 별도의 딕셔너리로 원래 딕셔너리 갱신의 두 단계로 진행하자
