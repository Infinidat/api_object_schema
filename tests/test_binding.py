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

    binding = FunctionBinding(get_func=get_value, set_func=set_value)
    field = Field(name="field_name", binding=binding)
    obj = {}

    binding.set_object_value_from_api(obj, 'a value')
    assert binding.get_api_value_from_object(obj) == 'a value'

    field.internalize(obj, 'a value')
    assert field.externalize(obj)  =='a value'

    with pytest.raises(TypeError):
        field.internalize(obj, 5)

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
