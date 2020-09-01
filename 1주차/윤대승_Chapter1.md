# Chapter 1 - 파이썬의 데이터 모델

## 특별 메서드
- \_\_getitem\_\_
- \_\_setitem\_\_
- \_\_len\_\_
- ...

이러한 특별 메서드는 보통 파이썬 인터프리터에 의해 호출된다(len(x)를 소스코드에 적으면 x.\_\_len\_\_()을 호출함).<br>
내장 자료형의 경우에는 손쉬운 방법을 선택한다(CPython의 경우 len() 메서드는 PyVarObject C 구조체의 ob_size 필드의 값을 반환함).

## 문자열 표현
- \_\_repr\_\_
- \_\_str\_\_

객체를 문자열로 표현하기 위하여 repr() 내장 메서드에 의해 \_\_repr\_\_() 특별 메서드가 호출된다.<br>
% 연산자를 사용하는 고전 포맷 문자열에서는 %r, str.format() 메서드에서는 !r처럼 대화형 콘솔과 디버거는 평가된 표현식의 결과에 repr()을 호출한다.<br>
\_\_repr\_\_() 메서드가 반환한 문자열은 명확해야 하며, 가능하면 표현된 객체를 재생성하는 데 필요한 소스코드와 일치해야 한다.<br>
위 두가지 특별 메서드 중 하나만 구현해야 한다면 \_\_repr\_\_() 메서드를 구현하는 게 좋다. 파이썬 인터프리터는 \_\_str\_\_() 메서드가 구현되어 있지 않다면 \_\_repr\_\_() 메서드를 호출한다.

## 특별 메서드 테이블
| 범주 | 메서드명 |
|------|--------|
|문자열/바이트 표현|\_\_repr\_\_, \_\_str\_\_, \_\_format\_\_, \_\_bytes\_\_|
|숫자로 변환|\_\_abs\_\_, \_\_bool\_\_, \_\_complex\_\_, \_\_init\_\_, \_\_float\_\_, \_\_hash\_\_, \_\_index\_\_|
|컬렉션 에뮬레이션|\_\_len\_\_, \_\_getitem\_\_, \_\_setitem\_\_, \_\_delitem\_\_, \_\_contains\_\_, \_\_iter\_\_, \_\_reserved\_\_, \_\_next\_\_|
|콜러블 에뮬레이션|\_\_call\_\_|
|콘텍스트 관리|\_\_enter\_\_, \_\_exit\_\_|
|객체 생성 및 소멸|\_\_new\_\_, \_\_init\_\_, \_\_del\_\_|
|속성 관리|\_\_getattr\_\_, \_\_getattribute\_\_, \_\_setattr\_\_, \_\_delattr\_\_, \_\_dir\_\_|
|속성 디스크립터|\_\_get\_\_, \_\_set\_\_, \_\_delete\_\_|
|클래스 서비스|\_\_prepare\_\_, \_\_instancecheck\_\_, \_\_subclasscheck\_\_|

## 연산자 특별 메서드 테이블
|범주|메서드명|연산자|
|--|--|--|
|단항 수치 연산자|\_\_neg\_\_<br>\_\_pos\_\_<br>\_\_abs\_\_|-<br>+<br>abs()|
|향상된 비교 연산자|\_\_lt\_\_<br>\_\_le\_\_<br>\_\_eq\_\_<br>\_\_ne\_\_<br>\_\_gt\_\_<br>\_\_ge\_\_|<<br><=<br>==<br>!=<br>><br>>=|
|산술 연산자|\_\_add\_\_<br>\_\_sub\_\_<br>\_\_mul\_\_<br>\_\_truediv\_\_<br>\_\_floordiv\_\_<br>\_\_mod\_\_<br>\_\_divmod\_\_<br>\_\_pow\_\_<br>\_\_round\_\_|+<br>-<br>*<br>/<br>//<br>%<br>divmod()<br>** 또는 pow()<br>round()|
|역순 산술 연산자|\_\_radd\_\_<br>\_\_rsub\_\_<br>\_\_rmul\_\_<br>\_\_rtruediv\_\_<br>\_\_rfloordiv\_\_<br>\_\_rmod\_\_<br>\_\_rdivmod\_\_<br>\_\_rpow\_\_||
|복합 할당 산술 연산자|\_\_iadd\_\_<br>\_\_isub\_\_<br>\_\_imul\_\_<br>\_\_itruediv\_\_<br>\_\_ifloordiv\_\_<br>\_\_imod\_\_<br>\_\_ipow\_\_|+=<br>-=<br>*=<br>/=<br>//=<br>%=<br>**=|
|비트 연산자|\_\_invert\_\_<br>\_\_lshift\_\_<br>\_\_rshite\_\_<br>\_\_and\_\_<br>\_\_or\_\_<br>\_\_xor\_\_|~<br><<<br>>><br>&<br>\|<br>^|
|역순 비트 연산자|\_\_rlshift\_\_<br>\_\_rrshift\_\_<br>\_\_rand\_\_<br>\_\_rxor\_\_<br>\_\_ror\_\_||
|복합 할당 비트 연산자|\_\_ilshift\_\_<br>\_\_irshift\_\_<br>\_\_iand\_\_<br>\_\_ixor\_\_<br>\_\_ior\_\_|<<=<br>>>=<br>&=<br>^=<br>\|=
