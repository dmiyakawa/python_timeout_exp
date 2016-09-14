#!/usr/bin/env python
#
# Tested on Python 2.6.6, 2.7.12, 3.5.2
#
# See also:
# - http://qiita.com/toshitanian/items/133b42355b7867f5c458
# - https://github.com/pnpnpn/timeout-decorator
# - http://qiita.com/siroken3/items/4bb937fcfd4c2489d10a
#

# https://docs.python.org/2.6/library/__future__.html
from __future__ import print_function

from functools import wraps
import signal
import time


class TimeoutError(Exception):
    pass


def timeout(seconds):
    def handler(signum, frame):
        raise TimeoutError()

    def decorate(function):
        @wraps(function)
        def new_function(*args, **kwargs):
            if seconds > 0:
                old = signal.signal(signal.SIGALRM, handler)
                signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                return function(*args, **kwargs)
            finally:
                if seconds:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old)
        return new_function
    return decorate


def time_consuming_function(t=100):
    for i in range(t):
        print(i)
        time.sleep(1)


@timeout(5)
def run_with_timeout(t):
    time_consuming_function(t)


if __name__ == '__main__':
    try:
        run_with_timeout(100)
    except TimeoutError:
        print("Timeout")
