import pytest

from api_object_schema import Field, MethodBinding

# pylint: disable=redefined-outer-name

def test_translators(field, obj):
    assert len(field.binding.to_api_translators) == 1
    assert len(field.binding.from_api_translators) == 1

    original_value = obj.f()
    assert field.binding.get_api_value_from_object(None, type(obj), obj) == original_value * 2
    assert field.binding.get_value_from_api_value(None, type(obj), obj, original_value * 2) == original_value


@pytest.fixture
def obj():

    class Obj(object):

        def f(self):
            return 1337

    return Obj()

@pytest.fixture
def field():
    field_binding = MethodBinding('f').to_api(lambda x: x * 2).from_api(lambda x: int(x // 2))
    return Field('some_field', type=int, binding=field_binding)
