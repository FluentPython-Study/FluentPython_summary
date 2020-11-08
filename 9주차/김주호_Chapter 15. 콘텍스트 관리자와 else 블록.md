# Chapter 15. 콘텍스트 관리자와 else 블록

-------

## 15.1 이것 다음에 저것 :  if 문 이외에서의 else블록

else절은 if문 뿐만 아니라 for, while, try 문에서도 사용할 수 있다. 비밀스러운 것은 없지만 이 기능은 잘 알려져 있지 않다.

```python
try:
    dangerous_call()
except OSError:
    log('OSError...') 
else:
    after_call()

```

코드의 의도를 명확하고 정확히 표현하기 위해 try 블록 안에는 예외를 발생시킬 가능성이 있는 코드만 넣어야한다.



## 15.2 콘텍스트 관리자와 with 블록

```python
>>> with open('mirror.py') as fp: #
... src = fp.read(60) #
...
>>> len(src)
60
>>> fp #
<_io.TextIOWrapper name='mirror.py' mode='r' encoding='UTF-8'>
>>> fp.closed, fp.encoding #
(True, 'UTF-8')
>>> fp.read(60) #
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
```

콘텍스트 관리자 객체는 with문 뒤의 표현식을 평가한 결과지만, as절에 있는 타깃 변수의 값은 콘텍스트 관리자 객체의 \_\_enter\_\_() 호출 결과이다. 이 메서드는 콘텍스트 관리자 대신 다른 객체를 반환할 수도 있다. 제어 흐름이 with 문을 빠져나온 후에는 \_\_enter\_\_() 메서드가 반환한 객체가 아니라 콘텍스트 관리자 객체의 \_\_exit\_\_() 메서드가 호출된다.



```python
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'
  
	def reverse_write(self, text):
        self.original_write(text[::-1])
  
	def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True 
```



## 15.4 @contextmanager 사용하기

```python
@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    
    def reverse_write(text):
        original_write(text[::-1])
        
    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'
    sys.stdout.write = original_write 
```

본질적으로 @contextlib.contextmanger 데커레이터는 데커레이트된 함수를 \_\_enter\_\_()와 \_\_exit\_\_()  메서드를 구현하는 클래스 안에 넣을 뿐이다.



## 15.5 요약

for, while, try문에서 사용하는 else 블록에 대한 설명으로 시작했다. 이러한 문장에서 else절의 특별한 의미에 익숙해진 후에는 의도를 else를 이용해서 명확히 표현할 수 있게 된다. 

그러고 나서 콘텍스트 관리자와 with 문의 의미를 설명하면서, 자동으로 파일을 닫는 일반적인 용법보다 고차원적인 용법을 살펴보았다. 그리고 \_\_enter\_\_() 와 \_\_exit\_\_() 메서드를 가진 콘텍스트 관리자인 LookingGlass 클래스를 구현하고, \_\_exit\_\_() 메서드에서 예외를 처리하는 방법을 살펴보았다.

마지막으로, contextlib 표준 라이브러리 모듈에 있는 함수들을 살펴보았다. 그 중 하나인 @contextmanager 데커레이터는 하나의 yield 문을 가진 간단한 제너레이터를 이용해서 콘텍스트 관리자를 구현할 수 있게 해준다. 제너레이터를 사용하면 최소 2개의 메서드를 가진 클래스를 정의 하는 것보다 가볍게 콘텍스트 관리자를 만들 수 있다. 