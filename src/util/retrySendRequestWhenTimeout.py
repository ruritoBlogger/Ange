from typing import Any, Callable
import time
from timeout_decorator import TimeoutError

def retrySendRequestWhenTimeout(func: Callable[[Any], Any], *args) -> Any:
    """yfinanceのAPIを叩く, またタイムアウトした際はもう一度処理を挟む

    Args:
        target (Callable[[Any], Any]): 叩きたい関数

    Returns:
        Any: 関数の結果
    """
    try:
        result = func(*args)
        return result
    except TimeoutError:
        print("retry func because yfinance api is timeout...")
        time.sleep(10)
        return retrySendRequestWhenTimeout(func, args)

