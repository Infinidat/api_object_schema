from .special_value import SpecialValue


class ValueTranslator(object):
    """
    This is an abstract base for translator objects.

    Translator objects are used to convert values to and from the system's API layer
    """

    def to_api(self, value):
        """
        Translates a value from Python to its API/json representation

        :return: must be JSON encodable
        """
        if isinstance(value, SpecialValue):
            return value
        return self._to_api(value)

    def from_api(self, value):
        """
        Translates a value from the system API to its Pythonic counterpart
        """
        return self._from_api(value)

    def _to_api(self, value):
        raise NotImplementedError() # pragma: no cover

    def _from_api(self, value):
        raise NotImplementedError() # pragma: no cover


class FunctionTranslator(ValueTranslator):  # pylint: disable=abstract-method
    """
    Implements value translation with the use of functions
    """

    def __init__(self, to_api=None, from_api=None):
        super(FunctionTranslator, self).__init__()
        if to_api is not None:
            self._to_api = to_api
        if from_api is not None:
            self._from_api = from_api


class IdentityTranslator(ValueTranslator):  # pylint: disable=abstract-method
    def identity(self, value):
        return value

    to_api = from_api = identity
