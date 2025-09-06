from typing import TypeVar, Optional, Callable, overload

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

@overload
def or_else_throw(value: Optional[T], error: E) -> T: ...
@overload
def or_else_throw(value: Optional[T], error: Callable[[], E]) -> T: ...

def or_else_throw(value: Optional[T], error):
    """
    value가 None이면 예외를 던진다.

    error는 Exception 인스턴스 또는 예외 팩토리(Callable[[], Exception]) 모두 허용.
    """
    if value is None:
        raise (error() if callable(error) else error)
    return value