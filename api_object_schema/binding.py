import itertools

from .utils import loose_isinstance

# pylint: disable=unused-argument

class ObjectAPIBinding(object):

    """This class is responsible for describing how an API object field translates into a Pythonic
    object field - how it is fetched from the API representation and how it is
    rendered back to the API.
    """

    _field = None

    def __init__(self):
        super(ObjectAPIBinding, self).__init__()
        self.to_api_translators = []
        self.from_api_translators = []

    def set_field(self, field):
        """Assigns this binding to a specific field
        """
        assert self._field is None
        self._field = field

    def to_api(self, func):
        """Appends a translator function to the chain of translators needed to convert a Pythonic value to an API value
        """
        self.to_api_translators.append(func)
        return self

    add_to_api_translator = to_api

    def from_api(self, func):
        """Appends a translator function to the chain of translators needed to convert a Pythonic value to an API value
        """
        self.from_api_translators.append(func)
        return self

    add_from_api_translator = from_api

    def get_value_from_api_object(self, system, objtype, obj, api_obj):
        """This method is used when fetching a field value from an entire API representation of the object itself

        By default, it uses :meth:`.get_value_from_api_value` to carry out its work.

        Besides `api_obj`, all parameters retain their meanings from :meth:`.get_value_from_api_value`.

        :param api_obj: the raw API representation of the object
        """
        return self.get_value_from_api_value(system, objtype, obj, api_obj[self._field.api_name])

    def get_value_from_api_value(self, system, objtype, obj, api_value):
        """This method parses an API value to its Pythonic representation which eventually belongs
        to the Python object in question.

        :param system: the system to which the object belongs
        :param objtype: the class of the Pythonic object in question
        :param obj: the object to which we are computing the field. *this might be None*, if the object hasn't been
           constructed yet
        :param api_value: the raw API value for this field
        """
        returned = api_value
        for translator in itertools.chain(self.from_api_translators, [self._field.type.translator.from_api, self._normalize_value]):
            returned = translator(returned)
        assert returned is None or loose_isinstance(returned, self._field.type.type)
        return returned

    def _normalize_value(self, value):
        return self._coerce(value, self._field.type.type)

    def _normalize_api_value(self, value):
        return self._coerce(value, self._field.type.api_type)

    def _coerce(self, value, result_type):

        if value is None:
            return None

        if not loose_isinstance(value, result_type):
            value = result_type(value)

        return value


    def get_api_value_from_object(self, system, objtype, obj):
        """Retrieves the API representation of the field from a whole Pythonic object containing it.

        By default this is implemented in terms of :meth:`.get_api_value_from_value`
        """
        value = self.get_object_value(system, objtype, obj)
        return self.get_api_value_from_value(system, objtype, obj, value)

    def get_api_value_from_value(self, system, objtype, obj, value):
        """Retrieves the API value from a Pythonic value

        :param system: the system to which this object belongs
        :param objtype: the type of the Pythonic object
        :param obj: the object itself. May be ``None``.
        :param value: the Pythonic value for the field
        """
        returned = value
        for translator in itertools.chain(self.to_api_translators, [self._field.type.translator.to_api, self._normalize_api_value]):
            returned = translator(returned)
        assert returned is None or loose_isinstance(returned, self._field.type.api_type)
        return returned

    def set_object_value(self, system, objtype, obj, value):
        """Controls how a Pythonic value is set for a Pythonic object
        """
        raise NotImplementedError()  # pragma: no cover

    def set_object_value_from_api_value(self, system, objtype, obj, api_value):
        """Controls how an API value is set for a Pythonic object
        """
        value = self.get_value_from_api_value(
            system, objtype, obj, api_value)
        self.set_object_value(system, objtype, obj, value)

    def get_object_value(self, system, objtype, obj):
        """Controls how a Pythonic value is fetched from a Pythonic object
        """
        raise NotImplementedError()  # pragma: no cover

    def set_api_object_value(self, system, objtype, obj, api_obj, value):
        """Controls how a raw API object (or JSON dict) gets assigned a field from a Pythonic value
        """
        api_value = self.get_api_value_from_value(system, objtype, obj, value)
        self.set_api_object_api_value(system, objtype, obj, api_obj, api_value)

    def set_api_object_api_value(self, system, objtype, obj, api_obj, api_value):
        """Controls how a raw API object (or JSON dict) gets assigned a field from an API value
        """
        api_obj[self._field.api_name] = api_value


class NoBinding(ObjectAPIBinding):

    def get_api_value_from_value(self, *args):  # pylint: disable=arguments-differ
        raise NotImplementedError()  # pragma: no cover

    def get_value_from_api_value(self, *args):  # pylint: disable=arguments-differ
        raise NotImplementedError()  # pragma: no cover


class AttributeBinding(ObjectAPIBinding):

    def __init__(self, attribute_name=None):
        super(AttributeBinding, self).__init__()
        self._attribute_name = attribute_name

    def get_object_value(self, system, objtype, obj):
        return getattr(obj, self._attribute_name or self._field.name)

    def set_object_value(self, system, objtype, obj, value):
        return setattr(obj, self._attribute_name or self._field.name, value)


class MethodBinding(ObjectAPIBinding):

    def __init__(self, getter_method_name=None, setter_method_name=None):
        super(MethodBinding, self).__init__()
        self._getter_method_name = getter_method_name
        self._setter_method_name = setter_method_name

    def get_object_value(self, system, objtype, obj):
        getter_method_name = self._getter_method_name or "get_{0}".format(
            self._field.name)
        return getattr(obj, getter_method_name)()

    def set_object_value(self, system, objtype, obj, value):
        setter_method_name = self._setter_method_name or "set_{0}".format(
            self._field.name)
        return getattr(obj, setter_method_name)(value)


class FunctionBinding(ObjectAPIBinding):

    def __init__(self, get_func=None, set_func=None):
        super(FunctionBinding, self).__init__()
        self._get_func = get_func
        self._set_func = set_func

    def get_object_value(self, system, objtype, obj):
        if self._get_func:
            return self._get_func(obj)
        raise NotImplementedError()  # pragma: no cover

    def set_object_value(self, system, objtype, obj, value):
        if self._set_func:
            return self._set_func(obj, value)
        raise NotImplementedError()  # pragma: no cover


class EmptyBinding(ObjectAPIBinding):  # pylint: disable=abstract-method

    def get_object_value(self, system, objtype, obj):
        return self._field.type.type()


class ConstBinding(ObjectAPIBinding):  # pylint: disable=abstract-method

    def __init__(self, value):
        super(ConstBinding, self).__init__()
        self._value = value

    def get_object_value(self, system, objtype, obj):
        return self._value

    def get_value_from_api_object(self, system, objtype, obj, api_obj):
        return self._value


class CountBinding(ObjectAPIBinding):  # pylint: disable=abstract-method

    def __init__(self, list_to_sum_name_or_func):
        super(CountBinding, self).__init__()
        self._list_name_or_func = list_to_sum_name_or_func

    def get_object_value(self, system, objtype, obj):
        list_to_sum = getattr(obj, self._list_name_or_func)
        if hasattr(list_to_sum, "__call__"):
            list_to_sum = list_to_sum()
        return len(list_to_sum)
