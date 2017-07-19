from ._compat import itervalues
from .field import Field


class FieldsMeta(type):

    FIELD_FACTORY = Field

    def __new__(cls, classname, bases, classdict):  # pylint: disable=bad-mcs-classmethod-argument
        returned = type.__new__(cls, classname, bases, classdict)
        returned.fields = fields = Fields(field_factory=cls.FIELD_FACTORY)
        for base in bases:
            if not isinstance(base, FieldsMeta):
                continue
            fields.update(base.fields)

        for field in classdict.get("FIELDS", []):
            fields.add_field(field)
            field.notify_added_to_class(returned)

        return returned


class Fields(object):

    def __init__(self, field_factory=Field, forbid_api_name_overrides=False, forbid_name_overrides=False):
        super(Fields, self).__init__()
        self._fields = {}
        self._fields_by_api_name = {}
        self._identity_fields = []
        self._field_factory = field_factory
        self._forbid_name_overrides = forbid_name_overrides
        self._forbid_api_name_overrides = forbid_api_name_overrides

    @classmethod
    def from_fields_list(cls, fields, **kwargs):
        returned = cls(**kwargs)
        for field in fields:
            returned.add_field(field)
        return returned

    def update(self, other_fields):
        for field in other_fields:
            self.add_field(field)

    def add_field(self, field):
        if self._forbid_name_overrides:
            assert field.name not in self._fields
        if self._forbid_api_name_overrides:
            assert field.api_name not in self._fields_by_api_name
        self._fields[field.name] = field
        self._fields_by_api_name[field.api_name] = field
        if field.is_identity:
            self._identity_fields.append(field)

    def get_identity_fields(self):
        return self._identity_fields

    def get_all_field_names_or_fabricate(self, api_object_json):
        """
        Given an example of an object from the system's API, returns the formal set of field names supported
        by this object type (after transformation to logical names)
        """
        returned = set()
        for field_name in api_object_json:
            logical_field = self._fields_by_api_name.get(field_name)
            if logical_field is not None:
                field_name = logical_field.name
            returned.add(field_name)
        return returned

    def get(self, field_name, default=None):
        return self._fields.get(field_name, default)

    def get_by_api_name(self, field_name, default=None):
        return self._fields_by_api_name.get(field_name, default)

    def get_or_fabricate(self, field_name):
        returned = self.get(field_name, None)
        if returned is None:
            return self._field_factory(field_name)
        return returned

    def __getattr__(self, attr):
        try:
            return self[attr]
        except LookupError:
            raise AttributeError(attr)

    def __getitem__(self, item):
        return self._fields[item]

    def __contains__(self, item):
        return item in iter(self)

    def __iter__(self):
        return itervalues(self._fields)

    def __len__(self):
        return len(self._fields)
