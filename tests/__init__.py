import re
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union

from pytest import warns
from salix import Struct

from omegaconf import II, MISSING


class IllegalType:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, IllegalType):
            return True
        return False


T = TypeVar("T")


class IllegalTypeGeneric(Generic[T]):
    pass


class NonCopyableIllegalType:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NonCopyableIllegalType):
            return True
        return False

    def __copy__(self) -> Any:
        raise NotImplementedError()

    def __deepcopy__(self, memo: Any) -> Any:
        raise NotImplementedError()


class Dataframe:
    """Emulates Pandas Dataframe equality and boolean behavior."""

    def __init__(self) -> None:
        pass

    def __eq__(self, other: Any) -> Any:
        """Mimic pandas DataFrame __eq__, which returns a pandas DataFrame object"""
        return self

    def __bool__(self) -> None:
        """Mimic pandas DataFrame __bool__, which raises a ValueError"""
        raise ValueError


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class User(Struct, frozen=False):
    name: str = MISSING
    age: int = MISSING


class Group(Struct, frozen=False):
    admin: Optional[User] = None


class Enum1(Enum):
    FOO = 1
    BAR = 2


class Users(Struct, frozen=False):
    name2user: Dict[str, User] = {}


class OptionalUsers(Struct, frozen=False):
    name2user: Dict[str, Optional[User]] = {}


class ConfWithMissingDict(Struct, frozen=False):
    dict: Dict[str, Any] = MISSING


class Plugin(Struct, frozen=False):
    name: str = MISSING
    params: Any = MISSING


class ConcretePlugin(Plugin, frozen=False):
    name: str = "foobar_plugin"

    class FoobarParams(Struct, frozen=False):
        foo: int = 10

    params: FoobarParams = FoobarParams()


class NestedInterpolationToMissing(Struct, frozen=False):
    class BazParams(Struct, frozen=False):
        baz: str = "${..name}"

    subcfg: BazParams = BazParams()
    name: str = MISSING


class StructuredInterpolationKeyError(Struct, frozen=False):
    name: str = "${bar}"


class StructuredInterpolationValidationError(Struct, frozen=False):
    x: Optional[int] = None
    y: int = II(".x")


class StructuredWithMissing(Struct, frozen=False):
    num: int = MISSING
    opt_num: Optional[int] = MISSING
    dict: Dict[str, str] = MISSING
    opt_dict: Optional[Dict[str, str]] = MISSING
    list: List[str] = MISSING
    opt_list: Optional[List[str]] = MISSING
    user: User = MISSING
    opt_user: Optional[User] = MISSING
    inter_num: int = II("num")
    inter_user: User = II("user")
    inter_opt_user: Optional[User] = II("opt_user")


class StructuredWithBadDict(Struct, frozen=False):
    foo: Dict[str, str] = 123  # type: ignore


class StructuredWithBadList(Struct, frozen=False):
    foo: List[str] = 123  # type: ignore


class MissingList(Struct, frozen=False):
    list: List[str] = MISSING


class MissingDict(Struct, frozen=False):
    dict: Dict[str, str] = MISSING


class DictEnum(Struct, frozen=False):
    color_key: Dict[Color, str] = {}
    color_val: Dict[str, Color] = {}


class A(Struct, frozen=False):
    a: int = 10


class B(Struct, frozen=False):
    x: A = MISSING


class C(Struct, frozen=False):
    x: Optional[A] = None


class PersonD(Struct, frozen=False):
    age: int = 18
    registered: bool = True


class Module(Struct, frozen=False):
    name: str = MISSING
    classes: List[str] = MISSING


class Package(Struct, frozen=False):
    modules: List[Module] = MISSING


class UntypedList(Struct, frozen=False):
    list: List = [1, 2]  # type: ignore
    opt_list: Optional[List] = None  # type: ignore


class SubscriptedList(Struct, frozen=False):
    list: List[int] = [1, 2]


class SubscriptedListOpt(Struct, frozen=False):
    opt_list: Optional[List[int]] = [1, 2]
    list_opt: List[Optional[int]] = [1, 2, None]


class ListOfAny(Struct, frozen=False):
    list: List[Any]


class UntypedDict(Struct, frozen=False):
    dict: Dict = {"foo": "var"}  # type: ignore
    opt_dict: Optional[Dict] = None  # type: ignore


class SubscriptedDict(Struct, frozen=False):
    dict_str: Dict[str, int] = {"foo": 4}
    dict_enum: Dict[Color, int] = {Color.RED: 4}
    dict_int: Dict[int, int] = {123: 4}
    dict_float: Dict[float, int] = {123.45: 4}
    dict_bool: Dict[bool, int] = {True: 4, False: 5}
    dict_bytes: Dict[bytes, int] = {b"binary": 4}


class SubscriptedDictOpt(Struct, frozen=False):
    opt_dict: Optional[Dict[str, int]] = {"foo": 4}
    dict_opt: Dict[str, Optional[int]] = {"foo": 4, "bar": None}


class DictOfAny(Struct, frozen=False):
    dict: Dict[Any, Any]


class InterpolationList(Struct, frozen=False):
    list: List[float] = II("optimization.lr")


class InterpolationDict(Struct, frozen=False):
    dict: Dict[str, int] = II("optimization.lr")


class Str2Int(Struct, Dict[str, int], frozen=False):
    pass


class DictSubclass(Dict[Any, Any]):
    pass


class ListSubclass(List[Any]):
    pass


class Shape(Tuple[int, int, int]):
    pass


class OptTuple(Struct, frozen=False):
    x: Optional[Tuple[int, ...]] = None


class NestedContainers(Struct, frozen=False):
    dict_of_dict: Dict[str, Dict[str, int]] = {"foo": {"bar": 123}}
    list_of_list: List[List[int]] = [[123]]
    dict_of_list: Dict[str, List[int]] = {"foo": [123]}
    list_of_dict: List[Dict[str, int]] = [{"bar": 123}]


class UnionAnnotations(Struct, frozen=False):
    ubf: Union[bool, float] = True
    oubf: Optional[Union[bool, float]] = None


def warns_dict_subclass_deprecated(dict_subclass: Any) -> Any:
    return warns(
        UserWarning,
        match=re.escape(
            f"Class `{dict_subclass.__name__}` subclasses `Dict`."
            + " Subclassing `Dict` in Structured Config classes is deprecated,"
            + " see github.com/omry/omegaconf/issues/663"
        ),
    )


class InnerX(Struct, frozen=False):
    d: int
    p: int


class InnerY(InnerX, frozen=False):
    q: int


class OuterA(Struct, frozen=False):
    x: InnerX


class OuterB(OuterA, frozen=False):
    x: InnerY  # pyrefly: ignore[bad-override-mutable-attribute]
