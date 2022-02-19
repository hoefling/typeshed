import importlib.abc
import types
import zipimport
from _typeshed import Self
from abc import ABCMeta
from typing import IO, Any, Callable, Generator, Iterable, Sequence, TypeVar, overload

LegacyVersion = Any  # from packaging.version
Version = Any  # from packaging.version

_T = TypeVar("_T")
_NestedStr = str | Iterable[str | Iterable[Any]]
_InstallerType = Callable[[Requirement], Distribution | None]
_EPDistType = Distribution | Requirement | str
_MetadataType = IResourceProvider | None
_PkgReqType = str | Requirement
_DistFinderType = Callable[[_Importer, str, bool], Generator[Distribution, None, None]]
_NSHandlerType = Callable[[_Importer, str, str, types.ModuleType], str]

def declare_namespace(name: str) -> None: ...
def fixup_namespace_packages(path_item: str) -> None: ...

class WorkingSet:
    entries: list[str]
    def __init__(self, entries: Iterable[str] | None = ...) -> None: ...
    def require(self, *requirements: _NestedStr) -> Sequence[Distribution]: ...
    def run_script(self, requires: str, script_name: str) -> None: ...
    def iter_entry_points(self, group: str, name: str | None = ...) -> Generator[EntryPoint, None, None]: ...
    def add_entry(self, entry: str) -> None: ...
    def __contains__(self, dist: Distribution) -> bool: ...
    def __iter__(self) -> Generator[Distribution, None, None]: ...
    def find(self, req: Requirement) -> Distribution | None: ...
    def resolve(
        self, requirements: Iterable[Requirement], env: Environment | None = ..., installer: _InstallerType | None = ...
    ) -> list[Distribution]: ...
    def add(self, dist: Distribution, entry: str | None = ..., insert: bool = ..., replace: bool = ...) -> None: ...
    def subscribe(self, callback: Callable[[Distribution], None]) -> None: ...
    def find_plugins(
        self, plugin_env: Environment, full_env: Environment | None = ..., fallback: bool = ...
    ) -> tuple[list[Distribution], dict[Distribution, Exception]]: ...

working_set: WorkingSet = ...

require = working_set.require
run_script = working_set.run_script
iter_entry_points = working_set.iter_entry_points
add_activation_listener = working_set.subscribe

class Environment:
    def __init__(self, search_path: Sequence[str] | None = ..., platform: str | None = ..., python: str | None = ...) -> None: ...
    def __getitem__(self, project_name: str) -> list[Distribution]: ...
    def __iter__(self) -> Generator[str, None, None]: ...
    def add(self, dist: Distribution) -> None: ...
    def remove(self, dist: Distribution) -> None: ...
    def can_add(self, dist: Distribution) -> bool: ...
    def __add__(self, other: Distribution | Environment) -> Environment: ...
    def __iadd__(self: Self, other: Distribution | Environment) -> Self: ...
    @overload
    def best_match(self, req: Requirement, working_set: WorkingSet) -> Distribution: ...
    @overload
    def best_match(self, req: Requirement, working_set: WorkingSet, installer: Callable[[Requirement], _T] = ...) -> _T: ...
    @overload
    def obtain(self, requirement: Requirement) -> None: ...
    @overload
    def obtain(self, requirement: Requirement, installer: Callable[[Requirement], _T] = ...) -> _T: ...
    def scan(self, search_path: Sequence[str] | None = ...) -> None: ...

def parse_requirements(strs: str | Iterable[str]) -> Generator[Requirement, None, None]: ...

class Requirement:
    unsafe_name: str
    project_name: str
    key: str
    extras: tuple[str, ...]
    specs: list[tuple[str, str]]
    # TODO: change this to packaging.markers.Marker | None once we can import
    #       packaging.markers
    marker: Any | None
    @staticmethod
    def parse(s: str | Iterable[str]) -> Requirement: ...
    def __contains__(self, item: Distribution | str | tuple[str, ...]) -> bool: ...
    def __eq__(self, other_requirement: object) -> bool: ...

def load_entry_point(dist: _EPDistType, group: str, name: str) -> Any: ...
def get_entry_info(dist: _EPDistType, group: str, name: str) -> EntryPoint | None: ...
@overload
def get_entry_map(dist: _EPDistType) -> dict[str, dict[str, EntryPoint]]: ...
@overload
def get_entry_map(dist: _EPDistType, group: str) -> dict[str, EntryPoint]: ...

class EntryPoint:
    name: str
    module_name: str
    attrs: tuple[str, ...]
    extras: tuple[str, ...]
    dist: Distribution | None
    def __init__(
        self,
        name: str,
        module_name: str,
        attrs: tuple[str, ...] = ...,
        extras: tuple[str, ...] = ...,
        dist: Distribution | None = ...,
    ) -> None: ...
    @classmethod
    def parse(cls, src: str, dist: Distribution | None = ...) -> EntryPoint: ...
    @classmethod
    def parse_group(cls, group: str, lines: str | Sequence[str], dist: Distribution | None = ...) -> dict[str, EntryPoint]: ...
    @classmethod
    def parse_map(
        cls, data: dict[str, str | Sequence[str]] | str | Sequence[str], dist: Distribution | None = ...
    ) -> dict[str, EntryPoint]: ...
    def load(self, require: bool = ..., env: Environment | None = ..., installer: _InstallerType | None = ...) -> Any: ...
    def require(self, env: Environment | None = ..., installer: _InstallerType | None = ...) -> None: ...
    def resolve(self) -> Any: ...

def find_distributions(path_item: str, only: bool = ...) -> Generator[Distribution, None, None]: ...
def get_distribution(dist: Requirement | str | Distribution) -> Distribution: ...

class Distribution(IResourceProvider, IMetadataProvider):
    PKG_INFO: str
    location: str
    project_name: str
    key: str
    extras: list[str]
    version: str
    parsed_version: tuple[str, ...]
    py_version: str
    platform: str | None
    precedence: int
    def __init__(
        self,
        location: str | None = ...,
        metadata: _MetadataType = ...,
        project_name: str | None = ...,
        version: str | None = ...,
        py_version: str = ...,
        platform: str | None = ...,
        precedence: int = ...,
    ) -> None: ...
    @classmethod
    def from_location(
        cls, location: str, basename: str, metadata: _MetadataType = ..., **kw: str | None | int
    ) -> Distribution: ...
    @classmethod
    def from_filename(cls, filename: str, metadata: _MetadataType = ..., **kw: str | None | int) -> Distribution: ...
    def activate(self, path: list[str] | None = ...) -> None: ...
    def as_requirement(self) -> Requirement: ...
    def requires(self, extras: tuple[str, ...] = ...) -> list[Requirement]: ...
    def clone(self, **kw: str | int | None) -> Requirement: ...
    def egg_name(self) -> str: ...
    def __cmp__(self, other: Any) -> bool: ...
    def get_entry_info(self, group: str, name: str) -> EntryPoint | None: ...
    @overload
    def get_entry_map(self) -> dict[str, dict[str, EntryPoint]]: ...
    @overload
    def get_entry_map(self, group: str) -> dict[str, EntryPoint]: ...
    def load_entry_point(self, group: str, name: str) -> Any: ...

EGG_DIST: int
BINARY_DIST: int
SOURCE_DIST: int
CHECKOUT_DIST: int
DEVELOP_DIST: int

def resource_exists(package_or_requirement: _PkgReqType, resource_name: str) -> bool: ...
def resource_stream(package_or_requirement: _PkgReqType, resource_name: str) -> IO[bytes]: ...
def resource_string(package_or_requirement: _PkgReqType, resource_name: str) -> bytes: ...
def resource_isdir(package_or_requirement: _PkgReqType, resource_name: str) -> bool: ...
def resource_listdir(package_or_requirement: _PkgReqType, resource_name: str) -> list[str]: ...
def resource_filename(package_or_requirement: _PkgReqType, resource_name: str) -> str: ...
def set_extraction_path(path: str) -> None: ...
def cleanup_resources(force: bool = ...) -> list[str]: ...

class IResourceManager:
    def resource_exists(self, package_or_requirement: _PkgReqType, resource_name: str) -> bool: ...
    def resource_stream(self, package_or_requirement: _PkgReqType, resource_name: str) -> IO[bytes]: ...
    def resource_string(self, package_or_requirement: _PkgReqType, resource_name: str) -> bytes: ...
    def resource_isdir(self, package_or_requirement: _PkgReqType, resource_name: str) -> bool: ...
    def resource_listdir(self, package_or_requirement: _PkgReqType, resource_name: str) -> list[str]: ...
    def resource_filename(self, package_or_requirement: _PkgReqType, resource_name: str) -> str: ...
    def set_extraction_path(self, path: str) -> None: ...
    def cleanup_resources(self, force: bool = ...) -> list[str]: ...
    def get_cache_path(self, archive_name: str, names: Iterable[str] = ...) -> str: ...
    def extraction_error(self) -> None: ...
    def postprocess(self, tempname: str, filename: str) -> None: ...

@overload
def get_provider(package_or_requirement: str) -> IResourceProvider: ...
@overload
def get_provider(package_or_requirement: Requirement) -> Distribution: ...

class IMetadataProvider:
    def has_metadata(self, name: str) -> bool: ...
    def metadata_isdir(self, name: str) -> bool: ...
    def metadata_listdir(self, name: str) -> list[str]: ...
    def get_metadata(self, name: str) -> str: ...
    def get_metadata_lines(self, name: str) -> Generator[str, None, None]: ...
    def run_script(self, script_name: str, namespace: dict[str, Any]) -> None: ...

class ResolutionError(Exception): ...

class DistributionNotFound(ResolutionError):
    @property
    def req(self) -> Requirement: ...
    @property
    def requirers(self) -> set[str]: ...
    @property
    def requirers_str(self) -> str: ...
    def report(self) -> str: ...

class VersionConflict(ResolutionError):
    @property
    def dist(self) -> Any: ...
    @property
    def req(self) -> Any: ...
    def report(self) -> str: ...
    def with_context(self, required_by: set[Distribution | str]) -> VersionConflict: ...

class ContextualVersionConflict(VersionConflict):
    @property
    def required_by(self) -> set[Distribution | str]: ...

class UnknownExtra(ResolutionError): ...

class ExtractionError(Exception):
    manager: IResourceManager
    cache_path: str
    original_error: Exception

class _Importer(importlib.abc.MetaPathFinder, importlib.abc.InspectLoader, metaclass=ABCMeta): ...

def register_finder(importer_type: type, distribution_finder: _DistFinderType) -> None: ...
def register_loader_type(loader_type: type, provider_factory: Callable[[types.ModuleType], IResourceProvider]) -> None: ...
def register_namespace_handler(importer_type: type, namespace_handler: _NSHandlerType) -> None: ...

class IResourceProvider(IMetadataProvider): ...
class NullProvider: ...
class EggProvider(NullProvider): ...
class DefaultProvider(EggProvider): ...

class PathMetadata(DefaultProvider, IResourceProvider):
    def __init__(self, path: str, egg_info: str) -> None: ...

class ZipProvider(EggProvider): ...

class EggMetadata(ZipProvider, IResourceProvider):
    def __init__(self, zipimporter: zipimport.zipimporter) -> None: ...

class EmptyProvider(NullProvider): ...

empty_provider: EmptyProvider

class FileMetadata(EmptyProvider, IResourceProvider):
    def __init__(self, path_to_pkg_info: str) -> None: ...

def parse_version(v: str) -> Version | LegacyVersion: ...
def yield_lines(strs: _NestedStr) -> Generator[str, None, None]: ...
def split_sections(strs: _NestedStr) -> Generator[tuple[str | None, str], None, None]: ...
def safe_name(name: str) -> str: ...
def safe_version(version: str) -> str: ...
def safe_extra(extra: str) -> str: ...
def to_filename(name_or_version: str) -> str: ...
def get_build_platform() -> str: ...
def get_platform() -> str: ...
def get_supported_platform() -> str: ...
def compatible_platforms(provided: str | None, required: str | None) -> bool: ...
def get_default_cache() -> str: ...
def get_importer(path_item: str) -> _Importer: ...
def ensure_directory(path: str) -> None: ...
def normalize_path(filename: str) -> str: ...
