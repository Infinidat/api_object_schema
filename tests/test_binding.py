import pytest
from api_object_schema import (Field, FieldBinding, NoBinding, EmptyBinding,
                               AttributeBinding, MethodBinding,
                               FunctionBinding, ConstBinding, CountBinding)


def test_field_binding():
    binding = FieldBinding()
    fake_field = object()
    binding.set_field(fake_field)

    with pytest.raises(AssertionError):
        binding.set_field(fake_field)

def test_no_binding():
    binding = NoBinding()
    with pytest.raises(NotImplementedError):
        binding.get_api_value_from_object(None)

    with pytest.raises(NotImplementedError):
        binding.set_object_value_from_api(None, None)

def test_empty_binding():
    empty_list = Field(name="field_name", type=list, binding=EmptyBinding())
    empty_dict = Field(name="field_name", type=dict, binding=EmptyBinding())

    assert empty_list.binding.get_api_value_from_object(None) == []
    assert empty_dict.binding.get_api_value_from_object(None) == {}

    with pytest.raises(NotImplementedError):
        empty_list.binding.set_object_value_from_api(None, None)
    with pytest.raises(NotImplementedError):
        empty_dict.binding.set_object_value_from_api(None, None)

def test_attribute_binding():
    class Obj(object):
        def __init__(self): self.val = None

    field = Field(name="field_name", binding=AttributeBinding('val'))
    obj = Obj()
    field.binding.set_object_value_from_api(obj, 'bla')
    assert field.binding.get_api_value_from_object(obj) == 'bla'

    field = Field(name="val", binding=AttributeBinding())
    obj = Obj()
    field.binding.set_object_value_from_api(obj, 'abc')
    assert field.binding.get_api_value_from_object(obj) == 'abc'

def test_method_binding():
    class Obj(object):
        def __init__(self): self.attr = None
        def get_attr(self): return self.attr
        def set_attr(self, value): self.attr=value

    field = Field(name="attr", binding=MethodBinding())
    obj = Obj()
    field.binding.set_object_value_from_api(obj, 'bla')
    assert field.binding.get_api_value_from_object(obj) == 'bla'

def test_function_binding():
    def get_value(obj):
        return obj['some_attr']
    def set_value(obj, value):
        obj['some_attr'] = value

    binding_func = lambda: FunctionBinding(get_func=get_value, set_func=set_value)
    str_field = Field(name="field_name", type=str, binding=binding_func())
    int_field = Field(name="field_name", type=int, binding=binding_func())
    obj = {}

    str_value = 'a value'
    int_value = 5

    binding = binding_func()
    binding.set_object_value_from_api(obj, str_value)
    assert binding.get_api_value_from_object(obj) == str_value
    binding.set_object_value_from_api(obj, int_value)
    assert binding.get_api_value_from_object(obj) == int_value

    str_field.internalize(obj, str_value)
    assert str_field.externalize(obj) == str_value
    with pytest.raises(TypeError):
        int_field.internalize(obj, str_value)

    int_field.internalize(obj, int_value)
    assert int_field.externalize(obj) == int_value
    with pytest.raises(TypeError):
        str_field.internalize(obj, int_value)

def test_const_binding():
    binding = ConstBinding('some_value')
    assert binding.get_api_value_from_object(None) == 'some_value'

    with pytest.raises(NotImplementedError):
        binding.set_object_value_from_api(None, None)

def test_count_binding():
    class Obj(object):
        a_list = ['a', 'b', 'c']
    field = Field(name="field_name", type=list, binding=CountBinding('a_list'))

    assert field.binding.get_api_value_from_object(Obj()) == 3

    with pytest.raises(NotImplementedError):
        field.binding.set_object_value_from_api(None, None)
