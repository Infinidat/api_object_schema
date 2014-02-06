import pytest

from api_object_schema import Field, Fields

def test_field(field):
    assert field.name == "name"

#### Fixtures
@pytest.fixture
def field():
    returned = Field(name="name", api_name="api_name")
    return returned


@pytest.fixture
def fields():
    returned = Fields()
    returned.add_field(field())
    return returned
