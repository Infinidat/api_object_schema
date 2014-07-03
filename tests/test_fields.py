import pytest
from api_object_schema._compat import with_metaclass
from api_object_schema import Field, Fields, FieldsMeta
from sentinels import NOTHING

class MyObj(object):
    pass

def test_field_string_types():

    f = Field('name', type='{0}:MyObj'.format(__name__))
    assert f.type.type is MyObj


@pytest.mark.parametrize('invalid_type', ['a', 'a.b.c', __name__, 'x:y:z', 'x:y'])
def test_field_invalid_string_types(invalid_type):
    f = Field('name', type=invalid_type)
    with pytest.raises(ValueError) as caught:
        f.type.type
    assert 'Invalid type string: ' in str(caught.value)


def test_field(field):
    assert field.name == "field_name"


def test_fields_get_by_name(fields, field):
    assert fields.get("field_name") is field
    assert fields.get("field_api_name") is None


def test_fields_get_by_api_name(fields, field):
    assert fields.get_by_api_name("field_name") is None
    assert fields.get_by_api_name("field_api_name") is field


def test_get_or_fabricate(fields, field):
    assert fields.get_or_fabricate("field_name") is field
    assert fields.get_or_fabricate("fake_field").name == "fake_field"


def test_get_all_field_names():
    class ObjectWithFields(with_metaclass(FieldsMeta)):
        FIELDS = [
            Field(name="field_a"),
            Field(name="field_b", api_name="field_b_api_name"),
        ]
    obj = ObjectWithFields()
    fields_json = {"field_a": "", "field_b_api_name": "", "fake_field": ""}
    expected = set(["field_a", "field_b", "fake_field"])
    assert obj.fields.get_all_field_names_or_fabricate(fields_json) == expected


def test_data_model_functions(fields):
    assert len(fields) == 1
    assert list(fields) == [fields['field_name']]
    aliases = [fields.field_name,
               fields['field_name'], fields.get('field_name')]
    assert len(set(aliases)) == 1

    with pytest.raises(AttributeError):
        fields.fake_name


def test_fields_fields(field):
    fields = Fields.from_fields_list([field])
    fields.update([Field(name="field_a"), Field(name="field_b")])
    fields.add_field(Field(name="field_c", is_identity=True))
    assert fields.get_identity_fields() == [fields.field_c]


def test_generate_field_default():
    assert Field(name="field_name").generate_default() is NOTHING
    assert Field(name="field_name", default=1).generate_default() == 1
    assert Field(name="field_name", default=lambda:
                 True).generate_default() is True


def test_get_is_visible():
    obj = {'some_val': None}
    assert Field(name="field_name").get_is_visible(obj) == True
    assert Field(name="field_name",
                 is_visible=False).get_is_visible(obj) is False
    assert Field(name="field_name", is_visible=lambda obj:
                 obj['some_val']).get_is_visible(obj) is None


# Fixtures
@pytest.fixture
def field():
    returned = Field(name="field_name", api_name="field_api_name")
    return returned


@pytest.fixture
def fields(field):
    returned = Fields()
    returned.add_field(field)
    return returned
