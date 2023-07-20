import sys
from _typeshed import Incomplete
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any
from typing_extensions import Final, TypeAlias

from ._hooks import (
    HookImpl as HookImpl,
    HookSpec as HookSpec,
    _HookCaller,
    _HookImplOpts,
    _HookRelay,
    _HookSpecOpts,
    _Namespace,
    _Plugin,
    normalize_hookimpl_opts as normalize_hookimpl_opts,
)
from ._result import _Result as _Result
from ._tracing import TagTracerSub

if sys.version_info >= (3, 8):
    from importlib.metadata import Distribution
else:
    Distribution: TypeAlias = Any

_BeforeTrace: TypeAlias = Callable[[str, Sequence[HookImpl], Mapping[str, Any]], None]
_AfterTrace: TypeAlias = Callable[[_Result[Any], str, Sequence[HookImpl], Mapping[str, Any]], None]

class PluginValidationError(Exception):
    plugin: _Plugin
    def __init__(self, plugin: _Plugin, message: str) -> None: ...

class DistFacade:
    def __init__(self, dist: Distribution) -> None: ...
    @property
    def project_name(self) -> str: ...
    def __getattr__(self, attr: str, default: Incomplete | None = None) -> Any: ...
    def __dir__(self) -> list[str]: ...

class PluginManager:
    project_name: Final[str]
    trace: Final[TagTracerSub]
    hook: Final[_HookRelay]
    def __init__(self, project_name: str) -> None: ...
    def register(self, plugin: _Plugin, name: str | None = None) -> str | None: ...
    def parse_hookimpl_opts(self, plugin: _Plugin, name: str) -> _HookImplOpts | None: ...
    def unregister(self, plugin: _Plugin | None = None, name: str | None = None) -> _Plugin: ...
    def set_blocked(self, name: str) -> None: ...
    def is_blocked(self, name: str) -> bool: ...
    def add_hookspecs(self, module_or_class: _Namespace) -> None: ...
    def parse_hookspec_opts(self, module_or_class: _Namespace, name: str) -> _HookSpecOpts | None: ...
    def get_plugins(self) -> set[Any]: ...
    def is_registered(self, plugin: _Plugin) -> bool: ...
    def get_canonical_name(self, plugin: _Plugin) -> str: ...
    def get_plugin(self, name: str) -> Any | None: ...
    def has_plugin(self, name: str) -> bool: ...
    def get_name(self, plugin: _Plugin) -> str | None: ...
    def check_pending(self) -> None: ...
    def load_setuptools_entrypoints(self, group: str, name: str | None = None) -> int: ...
    def list_plugin_distinfo(self) -> list[tuple[_Plugin, DistFacade]]: ...
    def list_name_plugin(self) -> list[tuple[str, _Plugin]]: ...
    def get_hookcallers(self, plugin: _Plugin) -> list[_HookCaller] | None: ...
    def add_hookcall_monitoring(self, before: _BeforeTrace, after: _AfterTrace) -> Callable[[], None]: ...
    def enable_tracing(self) -> Callable[[], None]: ...
    def subset_hook_caller(self, name: str, remove_plugins: Iterable[_Plugin]) -> _HookCaller: ...
