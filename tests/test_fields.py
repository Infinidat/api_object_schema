import pytest

from api_object_schema import Field, Fields

def test_field(field):
    assert field.name == "field_name"

def test_fields_get_by_name(fields, field):
    assert fields.get("field_name") is field
    assert fields.get("field_api_name") is None

def test_fields_get_by_api_name(fields, field):
    assert fields.get_by_api_name("field_name") is None
    assert fields.get_by_api_name("field_api_name") is field



#### Fixtures
@pytest.fixture
def field():
    returned = Field(name="field_name", api_name="field_api_name")
    return returned


@pytest.fixture
def fields(field):
    returned = Fields()
    returned.add_field(field)
    return returned
