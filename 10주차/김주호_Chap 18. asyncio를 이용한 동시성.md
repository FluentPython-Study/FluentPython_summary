# Chap 18. asyncio를 이용한 동시성

-----------------

## 18.1 스레드와 코루틴 비교

```python
import threading
import itertools
import time
import sys

class Signal:
    go = True
    
def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))
            
def slow_function():
    # pretend waiting a long time for I/O
    time.sleep(3)
    return 42
def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)
    if __name__ == '__main__':
        main()

```

스레드에 메시지를 보내 종료시켜야한다. 여기서는 signal.go를 사용했다. 스레드 대신 @asyncio.coroutine을 이용해서 동일한 동작을 어떻게 구현할 수 있는지 살펴보면,



```python
import asyncio
import itertools
import sys

@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
    	try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))
                
@asyncio.coroutine
def slow_function():
    # pretend waiting a long time for I/O
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
def supervisor():
    spinner = asyncio.async(spin('thinking!'))
    print('spinner object:', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)
    
if __name__ == '__main__':
    main()
```

데커레이터 사용을 강권한다. @asyncio.coroutine은 코루틴을 일반 함수와 다르게 보이도록 만들며, 코루틴이 yield from 되지 않고, 가비지 컬렉트 되는 경우 경고 메세지를 출력하므로 디버깅에 도움이 된다.



## 18.2 asyncio와 aiohttp로 내려받기

```python
import asyncio
import aiohttp 
from flags import BASE_URL, save_flag, show, main

@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image

@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)

if __name__ == '__main__':
    main(download_many)

```

flags_threadpool.py의 download_one() 함수도 재사용할 수 없었다. 매번 요청할 때마다 download_one() 코루틴 객체가 download_many() 안에서 생성되고, 이 코루틴 객체는 asyncio.wait() 코루틴에 의해 래핑된 후, 모두 loop.run_until_complete() 함수에 의해 구동된다.



## 18. 4 asyncio 내려받기 스크립트 개선

```python
@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(cc, base_url, semaphore, verbose)
             for cc in sorted(cc_list)]
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        try:
            res = yield from future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
                except IndexError:
                    error_msg = exc.__cause__.__class__.__name__
                if verbose and error_msg:
                    msg = '*** Error for {}: {}'
                    print(msg.format(country_code, error_msg))
                    status = HTTPStatus.error
        else:
            status = res.status
            counter[status] += 1
            return counter
        
def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

```

이 예제는 앞선 예제와 달리 Future 객체와 국가 코드 간에 매핑을 사용할 수 없다. asyncio.as_completed()가 반환한 Futrure 객체가 as_completed()를 호출할 때 전달한 객체와 동일하다고 장담할 수 없기 때문이33다.

## 18.6 asyncio 서버 작성

```python
import sys
import asyncio
from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '
index = UnicodeNameIndex()
@asyncio.coroutine
def handle_queries(reader, writer):
    while True:
        writer.write(PROMPT) # can't yield from!
        yield from writer.drain() # must yield from!
        data = yield from reader.readline()
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'
            client = writer.get_extra_info('peername')
            print('Received from {}: {!r}'.format(client, query))
        if query:
            if ord(query[:1]) < 32:
                break
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF)
            yield from writer.drain()
            print('Sent {} results'.format(len(lines)))
            print('Close the client socket')
            writer.close() 
```

입출력 메서드들 중 일부는 코루틴이므로 yield from 으로 구동해야 하며, 그 외 일반 함수들은 호출해야 한다는 것이 주의할 점이다.