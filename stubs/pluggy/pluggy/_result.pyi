import sys
from collections.abc import Callable
from types import TracebackType
from typing import Generic, TypeVar

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

_ExcInfo: TypeAlias = tuple[type[BaseException], BaseException, TracebackType]
_T = TypeVar("_T")

class HookCallError(Exception): ...

class _Result(Generic[_T]):
    _result: _T
    _exception: BaseException
    def __init__(self, result: _T | None, exception: BaseException | None) -> None: ...
    @property
    def excinfo(self) -> _ExcInfo | None: ...
    @property
    def exception(self) -> BaseException | None: ...
    @classmethod
    def from_call(cls, func: Callable[[], _T]) -> _Result[_T]: ...
    def force_result(self, result: _T) -> None: ...
    def force_exception(self, exception: BaseException) -> None: ...
    def get_result(self) -> _T: ...
