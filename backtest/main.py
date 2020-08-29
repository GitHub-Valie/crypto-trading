import src.extractor as extractor
import time
import config as cf


def makeTimeStat(start):
    d = time.time() - start
    display = 'Elapsed time: '
    if d // 3600:
        display += str(d // 3600) + 'h '
    if d // 60:
        display += str(d // 60) + 'm '
    display += str(round(d % 60, 2)) + 's'
    print(display)


try:
    while True:
        for symbol in cf.binance['watchlist']:
            t = time.time()
            extractor.startExtract(symbol)
            makeTimeStat(t)
            time.sleep(5)
except KeyboardInterrupt:
    pass
