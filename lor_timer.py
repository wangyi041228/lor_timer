from aiohttp import ClientSession, TCPConnector, client_exceptions
from asyncio import get_event_loop, gather
from json import loads
from time import time, sleep, strftime, localtime


async def get_url(url, hard=True):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(url) as r:
                    _result = await r.text()
                    if hard:
                        if r.status == 200:
                            return _result
                    else:
                        if r.status == 200:
                            return _result
                        elif r.status == 403:
                            return None
        except client_exceptions.ClientConnectorError:
            return None
        except Exception as e:
            print(type(e), e, e.args)


if __name__ == '__main__':
    port = 21337
    urls = [f'http://127.0.0.1:{port}/static-decklist',
            f'http://127.0.0.1:{port}/game-result',
            f'http://127.0.0.1:{port}/positional-rectangles']
    t = 0.0
    g = False
    o = ''
    start = time()
    results = [''] * 3
    while True:
        tasks = [get_url(url) for url in urls]
        _results = list(get_event_loop().run_until_complete(gather(*tasks)))
        print('\r', end='')
        s_t = f'[{strftime("%H:%M:%S", localtime())}]'  # "%y-%m-%d %H:%M:%S"
        if results[1] != _results[1]:
            if results[2]:
                res = loads(results[2])
                o = res.get('OpponentName')
        if _results[0]:
            cs = loads(_results[0]).get('CardsInDeck')
            if g:
                if cs is None:
                    s = time() - start
                    g = False
                    t += s
                    u = int(s)
                    v = int(t)
                    print(f'对手：{o}\n用时：{u // 60}:{u % 60:0>2d} ({u}s)\n累计：{v // 60}:{v % 60:0>2d} ({v}s)\n')
            else:
                if type(cs) is dict:
                    start = time()
                    g = True
                    print(s_t, '开始对局')
        print('\r' + s_t, end='')
        if g:
            s = time() - start
            _t = t + s
            u = int(s)
            v = int(_t)
            print(f' {u // 60}:{u % 60:0>2d} ({u}s) | {v // 60}:{v % 60:0>2d} ({v}s)。', end='')
        results = _results
        sleep(0.1)
