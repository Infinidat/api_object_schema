from api_object_schema._compat import PY2
from api_object_schema.utils import loose_isinstance

_INT_VALUES = [100, 183874837847398473]
if PY2:
    _INT_VALUES.append(long(100))  # pylint: disable=undefined-variable

_COMBINATIONS = [
    (str, ["hello", u"hello"], [1, True, None]),
    (bool, [True, False], ["s", 1.0, 1]),
    (int, _INT_VALUES, [1.2, "hello", True, False]),
]

if PY2:
    _COMBINATIONS.append((long, _INT_VALUES, [1.2, "hello", True, False]))  # pylint: disable=undefined-variable

def test_loose_isinstance():
    for type_, matching, not_matching in _COMBINATIONS:
        for m in matching:
            assert loose_isinstance(m, type_)
        for m in not_matching:
            assert not loose_isinstance(m, type_)
