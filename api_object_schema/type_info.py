from ._compat import string_types

from .value_translator import IdentityTranslator

# pylint: disable=redefined-builtin

class TypeInfo(object):

    def __init__(self, type, api_type=None, min_length=None, max_length=None, charset=None, max=None, min=None,
                 translator=IdentityTranslator()):
        super(TypeInfo, self).__init__()

        self._type = type
        self._api_type = api_type
        self._resolved = False

        #: minimum length for parameter
        self.min_length = min_length
        #: maximum length for parameter
        self.max_length = max_length
        if charset is not None:
            charset = set(charset)
        #: sequence of characters the parameter must use
        self.charset = charset
        #: minimum value
        self.min = min
        #: maximum value
        self.max = max
        #:translator to be used when passing values to/from the API
        self.translator = translator

    @property
    def type(self):
        if not self._resolved:
            self._resolve()
        return self._type

    @property
    def api_type(self):
        if not self._resolved:
            self._resolve()
        return self._api_type

    def _resolve(self):
        if isinstance(self._type, string_types):
            self._type = _import_type_by_name(self._type)
        if self._api_type is None:
            self._api_type = self._type
        self._resolved = True

    def is_valid_value(self, value):
        """
        Checks if a given value is valid given the type constraints
        """
        result, _ = self.is_valid_value_explain(value)
        return result

    def is_valid_value_explain(self, value):
        """
        :return: A tuple of (is_valid, reason)
        """
        if type(value) is not self.type:  # pylint: disable=unidiomatic-typecheck
            return (False, "Invalid type")

        if self.charset and not set(value).issubset(self.charset):
            return (False, "Invalid characters")

        if self.min is not None and value < self.min:
            return (False, "Under minimum value")

        if self.max is not None and value > self.max:
            return (False, "Exceeds maximum value")

        if self.min_length is not None and len(value) < self.min_length:
            return (False, "Too short")

        if self.max_length is not None and len(value) > self.max_length:
            return (False, "Too long")

        return (True, None)

def _import_type_by_name(typename):
    if typename.count(':') != 1:
        raise ValueError('Invalid type string: {0!r}'.format(typename))

    module_name, type_name = typename.split(':')
    try:
        module = __import__(module_name, fromlist=[''])

        if not hasattr(module, type_name):
            raise ImportError()
    except ImportError:
        raise ValueError('Invalid type string: {0!r} (import failed)'.format(typename))

    return getattr(module, type_name)
