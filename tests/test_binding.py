import pytest
from api_object_schema import (
    Field, ObjectAPIBinding, NoBinding, EmptyBinding,
    AttributeBinding, MethodBinding,
    FunctionBinding, ConstBinding, CountBinding)


def test_cannot_assign_to_field_twice():
    binding = ObjectAPIBinding()
    fake_field = object()
    binding.set_field(fake_field)

    with pytest.raises(AssertionError):
        binding.set_field(fake_field)


def test_no_binding():
    field = Field(name='field_name', binding=NoBinding())

    with pytest.raises(NotImplementedError):
        field.binding.get_api_value_from_value(None, None, None, None)


def test_attribute_binding():
    class Obj(object):

        def __init__(self):
            self.val = None

    field = Field(name="field_name", binding=AttributeBinding('val'))
    obj = Obj()
    field.binding.set_object_value(None, type(obj), obj, 'bla')
    assert field.binding.get_object_value(None, Obj, obj) == 'bla'

    field = Field(name="val", binding=AttributeBinding())
    obj = Obj()
    field.binding.set_object_value(None, type(obj), obj, 'abc')
    assert field.binding.get_object_value(None, type(obj), obj) == 'abc'


def test_method_binding():
    class Obj(object):

        def __init__(self):
            self.attr = None

        def get_attr(self):
            return self.attr

        def set_attr(self, value):
            self.attr = value

    field = Field(name="attr", binding=MethodBinding())
    obj = Obj()
    field.binding.set_object_value(object(), type(obj), obj, 'bla')
    assert field.binding.get_object_value(None, type(obj), obj) == 'bla'


def test_function_binding():
    def get_value(obj):
        return obj['some_attr']

    def set_value(obj, value):
        obj['some_attr'] = value

    binding_func = lambda: FunctionBinding(
        get_func=get_value, set_func=set_value)
    str_field = Field(name="field_name", type=str, binding=binding_func())  # pylint: disable=unused-variable
    int_field = Field(name="field_name", type=int, binding=binding_func())  # pylint: disable=unused-variable
    obj = {}

    str_value = 'a value'
    int_value = 5

    binding = binding_func()
    binding.set_object_value(None, type(obj), obj, str_value)
    assert binding.get_object_value(None, type(obj), obj) == str_value
    binding.set_object_value(None, type(obj), obj, int_value)
    assert binding.get_object_value(None, type(obj), obj) == int_value

def test_const_binding():
    binding = ConstBinding('some_value')
    assert binding.get_object_value(None, None, None) == 'some_value'
    assert binding.get_value_from_api_object(None, None, None, None) == 'some_value'

    with pytest.raises(NotImplementedError):
        binding.set_object_value(None, None, None, None)

def test_empty_binding():
    field = Field(name='empty_attr', type=list, binding=EmptyBinding())
    assert field.binding.get_object_value(None, None, None) == []

    with pytest.raises(NotImplementedError):
        field.binding.set_object_value(None, None, None, None)


@pytest.mark.parametrize("list_name", ["a_list", "get_a_list"])
def test_count_binding(list_name):
    class Obj(object):
        a_list = ['a', 'b', 'c']

        def get_a_list(self):
            return self.a_list

    field = Field(name="field_name", type=list,
                  binding=CountBinding(list_name))
    assert field.binding.get_object_value(None, Obj, Obj()) == 3

    with pytest.raises(NotImplementedError):
        field.binding.set_object_value(None, None, None, None)
