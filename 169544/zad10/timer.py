from typing import Any
import time
from collections.abc import Callable
def timer[F:Callable[..., Any]](func:F)->F:
    def wrapper(*args:Any,**kwargs:Any)->Any:
        wynik1=time.perf_counter()
        result=func(*args,**kwargs)
        wynik2=time.perf_counter()
        wynik3=wynik2-wynik1
        print(f"Czas {wynik3}")
        return result
    return wrapper

@timer
def add(x:int,y:int)->int:
    return x+y
