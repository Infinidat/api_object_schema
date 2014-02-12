class FieldBinding(object):

    _field = None

    def set_field(self, field):
        assert self._field is None
        self._field = field

    def get_api_value_from_object(self, obj):
        raise NotImplementedError() # pragma: no cover

    def set_object_value_from_api(self, obj, api_value):
        raise NotImplementedError() # pragma: no cover


class NoBinding(FieldBinding):
    pass

class AttributeBinding(FieldBinding):
    def __init__(self, attribute_name=None):
        super(AttributeBinding, self).__init__()
        self._attribute_name = attribute_name

    def get_api_value_from_object(self, obj):
        return getattr(obj, self._attribute_name or self._field.name)

    def set_object_value_from_api(self, obj, api_value):
        return setattr(obj, self._attribute_name or self._field.name, api_value)

class MethodBinding(FieldBinding):
    def __init__(self, getter_method_name=None, setter_method_name=None):
        super(MethodBinding, self).__init__()
        self._getter_method_name = getter_method_name
        self._setter_method_name = setter_method_name

    def get_api_value_from_object(self, obj):
        getter_method_name = self._getter_method_name or "get_{0}".format(self._field.name)
        return getattr(obj, getter_method_name)()

    def set_object_value_from_api(self, obj, api_value):
        setter_method_name = self._setter_method_name or "set_{0}".format(self._field.name)
        return getattr(obj, setter_method_name)(api_value)
