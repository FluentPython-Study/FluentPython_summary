

# Chap 17. Future를 이용한 동시성

-------------

## 17.1 세 가지 스타일의 웹 내려받기

### 17.1.1 순차 내려받기 스크립트

```python
import os
import time
import sys
import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'
def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)
 
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

def show(text):
    print(text, end=' ')
    sys.stdout.flush()
    
def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))
  
if __name__ == '__main__':
    main(download_many) 
```



concurrent.futures 패키지의 가장 큰 특징은 ThreadPoolExecutor와 ProcessPoolExecutor 클래스인데, 이 클래스들은 콜러블 객체를 서로 다른 스레드나 프로세스에서 실행할 수 있게 해주는 인터페이스를 구현한다. 이 클래스들은 작업자 스레드나 작업자 프로세스를 관리하는 풀과 실행할 작업을 담은 큐를 가지고 있다.

```python
from concurrent import futures
from flags import save_flag, get_flag, show, main
MAX_WORKERS = 20

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))

if __name__ == '__main__':
    main(download_many) 
```



## 17.2 블로킹 I/O와 GIL

CPython 인터프리터는 내부적으로 스레드 안전하지 않으므로, 전역 인터프리터 락 (GIL)을 가지고 있다. GIL은 한 번에 한 스레드만 파이썬 바이트 코드를 실행하도록 제한한다. 그렇기 때문에 단일 파이썬 프로세스가 동시에 다중 CPU 코어를 사용할 수 없다.

블로킹 입출력을 실행하는 모든 표준 라이브러리 함수는 OS에서 결과를 기다리는 동안 GIL을 해제한다. 즉, 입출력 위주의 작업을 실행하는 파이썬 프로그램은 파이썬으로 구현하더라도 스레드를 이용함으로써 이득을 볼 수 있다는 것이다.



## 17.3 concurrent.futures로 프로세스 실행하기

```python
def download_many(cc_list):
     workers = min(MAX_WORKERS, len(cc_list))
     with futures.ThreadPoolExecutor(workers) as executor:
```

To this : 

```python
def download_many(cc_list):
     with futures.ProcessPoolExecutor() as executor:
```

입출력 위주의 연산을 수행하는 경우에는 ThreadPoolExecutor에 수십 내지 수천 개의 스레드를 사용할 수 있다. 최적의 스레드 수는 처리할 작업의 특성과 가용한 메모리에 따라 다르므로, 신중히 테스트해서 최적의 스레드 수를 찾아야 한다.



## 17.4 Executor.map() 실험

```python
from time import sleep, strftime
from concurrent import futures
def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)
    
   
def loiter(n): 
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10
    
def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5)) // 5개의 작업 요청
    display('results:', results) # .
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))
        
main()    
```

Executor.map()은 사용하기 쉽지만, 호출한 순서 그대로 결과를 반환하는 특징이 있다.



## 17.5 진행 상황 출력하고 에러를 처리하며 내려받기

### 17.5.1 flags2 예제에서의 에러처리

```python
def get_flag(base_url, cc):
 url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
 resp = requests.get(url)
 if resp.status_code != 200:
 resp.raise_for_status()
 return resp.content


def download_one(cc, base_url, verbose=False):
     try:
         image = get_flag(base_url, cc)
     except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = 'not found'
        else:
            raise
     else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
        
        if verbose:
            print(cc, msg)
            return Result(status, cc) 

```

파이썬 쓰레드는 입출력 위주의 애플리케이션에 잘 맞으며, 경우에 따라 concurrent.futures패키지를 이용하면 아주 간단히 처리할 수 있다.