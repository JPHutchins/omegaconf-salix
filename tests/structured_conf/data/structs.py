import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union, cast

from salix import Struct

from omegaconf import II, MISSING, SI
from tests import Color, Enum1

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import TypedDict


class InstanceDict:
    pass


class NotStructuredConfig:
    name: str = "Bond"
    age: int = 7

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, type(self)):
            return self.name == other.name and self.age == other.age
        return False


if sys.version_info >= (3, 8):  # pragma: no cover

    class TypedDictSubclass(TypedDict):
        foo: str


class StructuredWithInvalidField(Struct, frozen=False):
    bar: NotStructuredConfig = NotStructuredConfig()


class User(Struct, frozen=False):
    name: str = MISSING
    age: int = MISSING


class ExtensibleUser(Struct, InstanceDict, frozen=False):
    name: str = MISSING
    age: int = MISSING


class UserList(Struct, frozen=False):
    list: List[User] = MISSING


class UserDict(Struct, frozen=False):
    dict: Dict[str, User] = MISSING


class UserWithDefaultName(User, frozen=False):
    name: str = "bob"


class MissingUserField(Struct, frozen=False):
    user: User = MISSING


class MissingUserWithDefaultNameField(Struct, frozen=False):
    user: UserWithDefaultName = MISSING


class OptionalUser(Struct, frozen=False):
    user: Optional[User] = None


class InterpolationToUser(Struct, frozen=False):
    user: User = User("Bond", 7)
    admin: User = II("user")
    admin_list: List[User] = [II("user")]
    admin_dict: Dict[str, User] = {"bond": II("user")}


class AnyTypeConfig(Struct, frozen=False):
    with_default: Any = "Can get any type at runtime"
    null_default: Any = None
    # Access to this prior to assigning a value to it will result in
    # a MissingMandatoryValue exception.
    # Equivalent to "???" in YAML files
    mandatory_missing: Any = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Any = II("with_default")

    # specific types assigned
    int_default: Any = 12
    float_default: Any = 10.0
    str_default: Any = "foobar"
    bool_default: Any = True
    enum_default: Any = Color.BLUE

    # test mixing with variable with a specific type annotation
    typed_int_default: int = 10


class BoolConfig(Struct, frozen=False):
    # with default value
    with_default: bool = True

    # default is None
    null_default: Optional[bool] = None

    # explicit no default
    mandatory_missing: bool = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: bool = II("with_default")


class IntegersConfig(Struct, frozen=False):
    # with default value
    with_default: int = 10

    # default is None
    null_default: Optional[int] = None

    # explicit no default
    mandatory_missing: int = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: int = II("with_default")


class StringConfig(Struct, frozen=False):
    # with default value
    with_default: str = "foo"

    # default is None
    null_default: Optional[str] = None

    # explicit no default
    mandatory_missing: str = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: str = II("with_default")


class FloatConfig(Struct, frozen=False):
    # with default value
    with_default: float = 0.10

    # default is None
    null_default: Optional[float] = None

    # explicit no default
    mandatory_missing: float = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: float = II("with_default")


class BytesConfig(Struct, frozen=False):
    # with default value
    with_default: bytes = b"binary"

    # default is None
    null_default: Optional[bytes] = None

    # explicit no default
    mandatory_missing: bytes = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: bytes = II("with_default")


class PathConfig(Struct, frozen=False):
    # with default value
    with_default: Path = Path("hello.txt")

    # default is None
    null_default: Optional[Path] = None

    # explicit no default
    mandatory_missing: Path = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Path = II("with_default")


class EnumConfig(Struct, frozen=False):
    # with default value
    with_default: Color = Color.BLUE

    # default is None
    null_default: Optional[Color] = None

    # explicit no default
    mandatory_missing: Color = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Color = II("with_default")


class LiteralConfig(Struct, frozen=False):
    with_default: Literal["foo", "bar", True, b"baz", 5, Color.GREEN] = "foo"
    null_default: Optional[Literal["foo", "bar", True, b"baz", 5, Color.GREEN]] = None
    mandatory_missing: Literal["foo", "bar", True, b"baz", 5, Color.GREEN] = MISSING
    interpolation: Literal["foo", "bar", True, b"baz", 5, Color.GREEN] = II(
        "with_default"
    )


class LiteralContainers(Struct, frozen=False):
    list_: List[Literal["foo", "bar"]] = cast(List[Literal["foo", "bar"]], ["foo"])
    dict_: Dict[str, Literal["foo", "bar"]] = cast(Dict[str, Literal["foo", "bar"]], {"key": "foo"})


class ConfigWithList(Struct, frozen=False):
    list1: List[int] = [1, 2, 3]
    list2: Tuple[int, int, int] = (1, 2, 3)
    missing: List[int] = MISSING


class ConfigWithDict(Struct, frozen=False):
    dict1: Dict[str, Any] = {"foo": "bar"}
    missing: Dict[str, Any] = MISSING


class ConfigWithDict2(Struct, frozen=False):
    dict1: Dict[str, int] = {"foo": 2}


class Nested(Struct, frozen=False):
    # with default value
    with_default: int = 10

    # default is None
    null_default: Optional[int] = None

    # explicit no default
    mandatory_missing: int = MISSING

    # Note that since relative interpolations are not yet supported,
    # Nested configs and interpolations does not play too well together
    interpolation: int = II("value_at_root")


class NestedSubclass(Nested, frozen=False):
    additional: int = 20


class NestedConfig(Struct, frozen=False):
    default_value: Nested

    # with default value
    user_provided_default: Nested = Nested(with_default=42)

    value_at_root: int = 1000


class NestedWithAny(Struct, InstanceDict, frozen=False):
    var: Any = Nested()


class NoDefaultValue(Struct, frozen=False):
    no_default: Any


class Interpolation(Struct, frozen=False):
    x: int = 100
    y: int = 200
    # The real type of y is int, cast the interpolation string
    # to help static type checkers to see this truth
    z1: int = II("x")
    z2: str = SI("${x}_${y}")


class RelativeInterpolation(Struct, frozen=False):
    x: int = 100
    y: int = 200
    z1: int = II(".x")
    z2: str = SI("${.x}_${.y}")


class BoolOptional(Struct, frozen=False):
    with_default: Optional[bool] = True
    as_none: Optional[bool] = None
    not_optional: bool = True


class IntegerOptional(Struct, frozen=False):
    with_default: Optional[int] = 1
    as_none: Optional[int] = None
    not_optional: int = 1


class FloatOptional(Struct, frozen=False):
    with_default: Optional[float] = 1.0
    as_none: Optional[float] = None
    not_optional: float = 1


class StringOptional(Struct, frozen=False):
    with_default: Optional[str] = "foo"
    as_none: Optional[str] = None
    not_optional: str = "foo"


class ListOptional(Struct, frozen=False):
    with_default: Optional[List[int]] = [1, 2, 3]
    as_none: Optional[List[int]] = None
    not_optional: List[int] = [1, 2, 3]


class TupleOptional(Struct, frozen=False):
    with_default: Optional[Tuple[int, int, int]] = (1, 2, 3)
    as_none: Optional[Tuple[int, int, int]] = None
    not_optional: Tuple[int, int, int] = (1, 2, 3)


class EnumOptional(Struct, frozen=False):
    with_default: Optional[Color] = Color.BLUE
    as_none: Optional[Color] = None
    not_optional: Color = Color.BLUE


class DictOptional(Struct, frozen=False):
    with_default: Optional[Dict[str, int]] = {"a": 10}
    as_none: Optional[Dict[str, int]] = None
    not_optional: Dict[str, int] = {"a": 10}


class NoneTypeAnnotations(Struct, frozen=False):
    none: None = None
    none_type: type(None) = None  # type: ignore[valid-type]
    list_none: list[None] = [None]
    list_none_type: list[type(None)] = [None]
    dict_none: dict[str, None] = {"key": None}
    tuple_none: tuple[None] = (None,)


class RecursiveDict(Struct, frozen=False):
    d: Dict[str, "RecursiveDict"] = MISSING


class StructuredOptional(Struct, frozen=False):
    with_default: Optional[Nested] = Nested()
    as_none: Optional[Nested] = None
    not_optional: Nested = Nested()


class FrozenClass(Struct):
    user: User = User(name="Bart", age=10)
    x: int = 10
    list: List[int] = [1, 2, 3]


class ContainsFrozen(Struct, frozen=False):
    x: int = 10
    frozen: FrozenClass = FrozenClass()


class WithListField(Struct, frozen=False):
    list: List[int] = [1, 2, 3]


class WithDictField(Struct, frozen=False):
    dict: Dict[str, int] = {"foo": 10, "bar": 20}


if sys.version_info >= (3, 8):  # pragma: no cover

    class WithTypedDictField(Struct, frozen=False):
        dict: TypedDictSubclass


class ErrorDictObjectKey(Struct, frozen=False):
    # invalid dict key, must be str
    dict: Dict[object, str] = {object(): "foo", object(): "bar"}


class RegularClass:
    pass


class ErrorDictUnsupportedValue(Struct, frozen=False):
    # invalid dict value type, not one of the supported types
    dict: Dict[str, RegularClass] = {}


class ErrorListUnsupportedValue(Struct, frozen=False):
    # invalid dict value type, not one of the supported types
    dict: List[RegularClass] = []


class ErrorListUnsupportedStructuredConfig(Struct, frozen=False):
    # Nesting of structured configs in Dict and List is not currently supported
    list: List[User] = []


class InvalidNestedValue(Struct, frozen=False):
    value: int = "not-an-int"  # type: ignore[assignment]


class StructuredWithInvalidNestedValue(Struct, frozen=False):
    inner: InvalidNestedValue = InvalidNestedValue()


class ListExamples(Struct, frozen=False):
    any: List[Any] = [1, "foo"]
    ints: List[int] = [1, 2]
    strings: List[str] = ["foo", "bar"]
    booleans: List[bool] = [True, False]
    colors: List[Color] = [Color.RED, Color.GREEN]


class TupleExamples(Struct, frozen=False):
    any: Tuple[Any, Any] = (1, "foo")
    ints: Tuple[int, int] = (1, 2)
    strings: Tuple[str, str] = ("foo", "bar")
    booleans: Tuple[bool, bool] = (True, False)
    colors: Tuple[Color, Color] = (Color.RED, Color.GREEN)


class DictExamples(Struct, frozen=False):
    any: Dict[str, Any] = {"a": 1, "b": "foo"}
    ints: Dict[str, int] = {"a": 10, "b": 20}
    strings: Dict[str, str] = {"a": "foo", "b": "bar"}
    booleans: Dict[str, bool] = {"a": True, "b": False}
    colors: Dict[str, Color] = {
            "red": Color.RED,
            "green": Color.GREEN,
            "blue": Color.BLUE,
        }
    int_keys: Dict[int, str] = {1: "one", 2: "two"}
    float_keys: Dict[float, str] = {1.1: "one", 2.2: "two"}
    bool_keys: Dict[bool, str] = {True: "T", False: "F"}
    enum_key: Dict[Color, str] = {Color.RED: "red", Color.GREEN: "green"}


class DictOfObjects(Struct, frozen=False):
    users: Dict[str, User] = {"joe": User(name="Joe", age=18)}


class DictOfObjectsMissing(Struct, frozen=False):
    users: Dict[str, User] = {"moe": MISSING}


class ListOfObjects(Struct, frozen=False):
    users: List[User] = [User(name="Joe", age=18)]


class ListOfObjectsMissing(Struct, frozen=False):
    users: List[User] = [MISSING]


class DictSubclass:
    class Str2Str(Struct, Dict[str, str], frozen=False):
        pass

    class Str2Int(Struct, Dict[str, int], frozen=False):
        pass

    class Int2Str(Struct, Dict[int, str], frozen=False):
        pass

    class Float2Str(Struct, Dict[float, str], frozen=False):
        pass

    class Bool2Str(Struct, Dict[bool, str], frozen=False):
        pass

    class Color2Str(Struct, Dict[Color, str], frozen=False):
        pass

    class Color2Color(Struct, Dict[Color, Color], frozen=False):
        pass

    class Str2User(Struct, InstanceDict, Dict[str, User], frozen=False):
        pass

    class Str2StrWithField(Struct, InstanceDict, Dict[str, str], frozen=False):
        foo: str = "bar"

    class Str2IntWithStrField(Struct, Dict[str, int], frozen=False):
        foo: int = 1

    class Str2UserWithField(Struct, InstanceDict, Dict[str, User], frozen=False):
        foo: User = User("Bond", 7)

    class Error:
        class User2Str(Struct, Dict[User, str], frozen=False):
            pass


class Plugin(Struct, frozen=False):
    name: str = MISSING
    params: Any = MISSING


class ConcretePlugin(Plugin, frozen=False):
    name: str = "foobar_plugin"

    class FoobarParams(Struct, frozen=False):
        foo: int = 10

    params: FoobarParams = FoobarParams()


class PluginWithAdditionalField(Plugin, frozen=False):
    name: str = "foobar2_plugin"
    additional: int = 10


# Does not extend Plugin, cannot be assigned or merged
class FaultyPlugin(Struct, frozen=False):
    name: str = "faulty_plugin"


class PluginHolder(Struct, frozen=False):
    none: Optional[Plugin] = None
    missing: Plugin = MISSING
    plugin: Plugin = Plugin()
    plugin2: Plugin = ConcretePlugin()


class LinkedList(Struct, frozen=False):
    next: Optional["LinkedList"] = None
    value: Any = MISSING


class RecursiveList(Struct, frozen=False):
    d: List["RecursiveList"] = MISSING


class MissingTest:
    class Missing1(Struct, frozen=False):
        head: LinkedList = MISSING

    class Missing2(Struct, frozen=False):
        head: LinkedList = LinkedList(next=MISSING, value=1)


class NestedWithNone(Struct, frozen=False):
    plugin: Optional[Plugin] = None


class StructuredUnion(Struct, frozen=False):
    x: Union[int, Plugin] = 10


class ContainerUnion(Struct, frozen=False):
    x: Union[List[int], Dict[str, int]] = [1, 2]


class WithNativeMISSING(Struct, frozen=False):
    num: int


class MissingStructuredConfigField(Struct, frozen=False):
    plugin: Plugin = MISSING


class ListClass(Struct, frozen=False):
    list: List[int] = []
    tuple: Tuple[int, int] = (1, 2)


class UntypedList(Struct, frozen=False):
    list: List = [1, 2]  # type: ignore
    opt_list: Optional[List] = None  # type: ignore


class UntypedDict(Struct, frozen=False):
    dict: Dict = {"foo": "var"}  # type: ignore
    opt_dict: Optional[Dict] = None  # type: ignore


class StructuredSubclass:
    class ParentInts(Struct, frozen=False):
        int1: int
        int2: int
        int3: int
        int4: int = MISSING

    class ChildInts(ParentInts, frozen=False):
        int2: int = 5
        int3: int = 10
        int4: int = 15

    class ParentContainers(Struct, frozen=False):
        list1: List[int] = MISSING
        list2: List[int] = [5, 6]
        dict: Dict[str, Any] = MISSING

    class ChildContainers(ParentContainers, frozen=False):
        list1: List[int] = [1, 2, 3]
        dict: Dict[str, Any] = {"a": 5, "b": 6}

    class ParentNoDefaultFactory(Struct, frozen=False):
        no_default_to_list: Any
        int_to_list: Any = 1

    class ChildWithDefaultFactory(ParentNoDefaultFactory, frozen=False):
        no_default_to_list: Any = ["hi"]
        int_to_list: Any = ["hi"]


class LeadingUnderscoreFields(Struct, frozen=False):
    _foo: str = "x"
    _bar: str = "y"


class NestedContainers:
    class ListOfLists(Struct, frozen=False):
        lls: List[List[str]]
        llx: List[List[User]]
        llla: List[List[List[Any]]]
        lloli: List[List[Optional[List[int]]]]
        lls_default: List[List[str]] = cast(
                List[List[str]], [[], ["abc", "def", 123, MISSING], MISSING]
            )
        lolx_default: List[Optional[List[User]]] = [
                [],
                [User(), User(age=7, name="Bond"), MISSING],
                MISSING,
            ]

    class DictOfDicts(Struct, frozen=False):
        dsdsi: Dict[str, Dict[str, int]]
        dsdbi: Dict[str, Dict[bool, int]]
        dsdsx: Dict[str, Dict[str, User]]
        odsdsi_default: Optional[Dict[str, Dict[str, int]]] = cast(
                Optional[Dict[str, Dict[str, int]]],
                {
                    "dsi1": {},
                    "dsi2": {"s1": 1, "s2": "123", "s3": MISSING},
                    "dsi3": MISSING,
                },
            )
        dsdsx_default: Dict[str, Dict[str, User]] = {
                "dsx1": {},
                "dsx2": {
                    "s1": User(),
                    "s2": User(age=7, name="Bond"),
                    "s3": MISSING,
                },
                "dsx3": MISSING,
            }

    class ListsAndDicts(Struct, frozen=False):
        lldsi: List[List[Dict[str, int]]]
        ldaos: List[Dict[Any, Optional[str]]]
        dedsle: Dict[Color, Dict[str, List[Enum1]]]
        dsolx: Dict[str, Optional[List[User]]]
        oldfox: Optional[List[Dict[float, Optional[User]]]]
        dedsle_default: Dict[Color, Dict[str, List[Enum1]]] = {
                Color.RED: {"a": [Enum1.FOO, Enum1.BAR]},
                Color.GREEN: {"b": []},
                Color.BLUE: {},
            }

    class WithDefault(Struct, frozen=False):
        dsolx_default: Dict[str, Optional[List[User]]] = {"lx": [User()], "n": None}


class UnionsOfPrimitveTypes:
    class Simple(Struct, frozen=False):
        uis: Union[int, str]
        ubc: Union[bool, Color]
        uxf: Union[bytes, float]
        ouis: Optional[Union[int, str]]
        uois: Union[Optional[int], str]
        uisn: Union[int, str, None]
        uisN: Union[int, str, type(None)]  # type: ignore

    class WithDefaults(Struct, frozen=False):
        uis: Union[int, str] = "abc"
        ubc1: Union[bool, Color] = True
        ubc2: Union[bool, Color] = Color.RED
        uxf: Union[bytes, float] = 1.2
        ouis: Optional[Union[int, str]] = None
        uisn: Union[int, str, None] = 123
        uisN: Union[int, str, type(None)] = "abc"  # type: ignore

    class WithExplicitMissing(Struct, frozen=False):
        uis_missing: Union[int, str] = MISSING

    class WithBadDefaults1(Struct, frozen=False):
        uis: Union[int, str] = None  # type: ignore

    class WithBadDefaults2(Struct, frozen=False):
        ubc: Union[bool, Color] = "abc"  # type: ignore

    class WithBadDefaults3(Struct, frozen=False):
        uxf: Union[bytes, float] = True

    class WithBadDefaults4(Struct, frozen=False):
        oufb: Optional[Union[float, bool]] = Color.RED  # type: ignore

    class ContainersOfUnions(Struct, frozen=False):
        lubc: List[Union[bool, Color]]
        dsubf: Dict[str, Union[bool, float]]
        dsoubf: Dict[str, Optional[Union[bool, float]]]
        lubc_with_default: List[Union[bool, Color]] = [True, Color.RED]
        dsubf_with_default: Dict[str, Union[bool, float]] = {"abc": True, "xyz": 1.2}

    class InterpolationFromUnion(Struct, frozen=False):
        ubi: Union[bool, int]
        oubi: Optional[Union[bool, int]]
        an_int: int = 123
        a_string: str = "abc"
        missing: int = MISSING
        none: Optional[int] = None
        ubi_with_default: Union[bool, int] = II("an_int")
        oubi_with_default: Optional[Union[bool, int]] = II("none")

    class InterpolationToUnion(Struct, frozen=False):
        a_float: float = II("ufs")
        bad_int_interp: bool = II("ufs")
        ufs: Union[float, str] = 10.1

    class BadInterpolationFromUnion(Struct, frozen=False):
        a_float: float = 10.1
        ubi: Union[bool, int] = II("a_float")

    if sys.version_info >= (3, 10):

        class SupportPEP604(Struct, frozen=False):
            """https://peps.python.org/pep-0604/"""

            uis: int | str
            ouis: Optional[int | str]
            uisn: int | str | None = None
            uis_with_default: int | str = 123


if sys.version_info >= (3, 9):

    class SupportPEP585(Struct, frozen=False):
        """
        PEP 585 – Type Hinting Generics In Standard Collections
        https://peps.python.org/pep-0585/

        This means lower-case dict/list/tuple annotations
        can be used instad of uppercase Dict/List/Tuple.
        """

        dict_: dict[int, str] = {123: "abc"}
        list_: list[int] = [123]
        tuple_: tuple[int] = (123,)
        dict_no_subscript: dict = {123: "abc"}  # type: ignore[type-arg]
        list_no_subscript: list = [123]  # type: ignore[type-arg]
        tuple_no_subscript: tuple = (123,)  # type: ignore[type-arg]


class HasForwardRef(Struct, frozen=False):
    class CA(Struct, frozen=False):
        x: int = 3

    class CB(Struct, frozen=False):
        sub: "HasForwardRef.CA"

    a: CA
    b: CB


class HasBadAnnotation1(Struct, frozen=False):
    data: object


class HasBadAnnotation2(Struct, frozen=False):
    data: object()  # type: ignore
