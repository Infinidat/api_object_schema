from .field import Field

class BoundFields(object):

    def __init__(self, fields, obj):
        super(BoundFields, self).__init__()
        self.fields = fields
        self.object = obj
        self._cache = {}

    def __getitem__(self, item):
        return self._wrap_field(self.fields[item])

    def __getattr__(self, attr):
        return self._wrap_field(getattr(self.fields, attr))

    def _wrap_field(self, field):
        if isinstance(field, Field):
            field = field.clone_bound(self.object)
        return field
