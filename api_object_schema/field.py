from ._compat import string_types, PY2
from .binding import NoBinding
from .type_info import TypeInfo
from sentinels import NOTHING

class Field(object):
    """
    This class represents a single field exposed by a schema
    """

    def __init__(self, name, api_name=None, type=str, mutable=False, creation_parameter=False, is_unique=False, default=NOTHING, is_identity=False, is_filterable=False, is_sortable=False, binding=None, optional=False, sorting_key=None, is_visible=True):
        super(Field, self).__init__()

        #:the name of this field, as will be seen by the Python code interacting with the object(s)
        self.name = name
        if api_name is None:
            api_name = name

        #:the name of this field in the API layer (doesn't have to be the same as *name*)
        self.api_name = api_name
        if not isinstance(type, TypeInfo):
            type = TypeInfo(type)
        #:either the type of the exposed field, or a :class:`.TypeInfo` object specifying type properties
        self.type = type

        #:will this field be editable by the user?
        self.mutable = mutable
        #:Controls whether this field can be passed on object creation
        self.creation_parameter = creation_parameter
        #:If this is a creation parameter, controls whether we can omit this parameter
        self.optional = optional
        #:If True, means that this field value must be unique across the API
        self.is_unique = is_unique
        #:If True, this field is a part of an set of fields used to identify this object in the API
        self.is_identity = is_identity
        #:Can we filter objects according to this field
        self.is_filterable = is_filterable
        #:Can we sort according to this field?
        self.is_sortable = is_sortable
        #:Controls how the API value is computed from an existing Python object, and how the respective field is
        #:updated on an object.
        self.binding = self.get_default_binding_object() if binding is None else binding
        self.binding.set_field(self)
        #:If specified, will be used to generate defaults for this field if required and not specified by the user.
        #:Can be either a value or a callable generating a default
        self._default = default
        #:If sortable field, will be used to get sorting key
        self.sorting_key = sorting_key
        #:If specified, will return if a field should be visible for specific object
        self._is_visible = is_visible


    def get_default_binding_object(self):
        return NoBinding()

    def notify_added_to_class(self, cls):
        pass

    def generate_default(self):
        if hasattr(self._default, "__call__"):
            return self._default()
        return self._default

    def get_is_visible(self, obj):
        if hasattr(self._is_visible, "__call__"):
            return self._is_visible(obj)
        return self._is_visible

    def externalize(self, obj):
        field_value = self.binding.get_api_value_from_object(obj)
        api_value = self.type.translator.to_api(field_value)
        api_value = self.type.api_type(api_value)
        return api_value

    def get_internal_value(self, data):
        internal_value = self.type.translator.from_api(data)
        validation_type = self.type.type
        if PY2 and validation_type is str:
            validation_type = string_types
        if internal_value is not None and not isinstance(internal_value, validation_type):
            raise TypeError("{0!r} is not of field internal type(s) {1!r}".format(internal_value, validation_type))
        return internal_value

    def internalize(self, obj, data):
        internal_value = self.get_internal_value(data)
        return self.binding.set_object_value_from_api(obj, internal_value)
