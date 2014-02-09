from api_object_schema import TypeInfo


def test_invalid_types():
    assert_not_valid(TypeInfo(str), 2)
    assert_not_valid(TypeInfo(bool), 2)
    assert_not_valid(TypeInfo(int), True)
    assert_not_valid(TypeInfo(str), True)
    assert_valid(TypeInfo(str), "hello")
    assert_valid(TypeInfo(str), "")
    assert_valid(TypeInfo(int), 10)
    assert_valid(TypeInfo(bool), True)

def test_charsets():
    type_info = TypeInfo(str, charset="abc")
    assert_not_valid(type_info, "abcd")
    assert_not_valid(type_info, "def")
    assert_valid(type_info, "aaa")
    assert_valid(type_info, "")
    assert_valid(type_info, "abbbaacccb")

def test_min_max():
    assert_not_valid(TypeInfo(int, min=120), 119)
    assert_not_valid(TypeInfo(int, max=120), 121)
    assert_not_valid(TypeInfo(int, min=120, max=140), 119)
    assert_valid(TypeInfo(int, min=120), 121)
    assert_valid(TypeInfo(int, max=120), 29)
    assert_valid(TypeInfo(int, min=120, max=140), 121)

def test_min_max_length():
    assert_not_valid(TypeInfo(str, max_length=5), "hello!!!")
    assert_not_valid(TypeInfo(str, min_length=5), "hell")
    assert_not_valid(TypeInfo(str, min_length=5, max_length=6), "hello!!!")
    assert_not_valid(TypeInfo(str, min_length=5, max_length=6), "hell")
    assert_valid(TypeInfo(str, min_length=5, max_length=6), "hello")
    assert_valid(TypeInfo(str, min_length=5), "hello there")
    assert_valid(TypeInfo(str, max_length=5), "hey")


def assert_not_valid(type_info, value):
    result, explanation = type_info.is_valid_value_explain(value)
    assert result == type_info.is_valid_value(value)
    assert not result, "{0}: Unexpectedly valid: {1!r}".format(type_info, value)
    assert isinstance(explanation, str)

def assert_valid(type_info, value):
    result, explanation = type_info.is_valid_value_explain(value)
    assert result == type_info.is_valid_value(value)
    assert result, "{0}: Unexpectedly invalid: {1!r} ({2})".format(type_info, value, explanation)

    assert explanation is None
