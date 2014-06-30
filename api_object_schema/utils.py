from ._compat import PY2

def loose_isinstance(obj, type_):
    """
    Like isinstance, only handles ridiculous cases like isinstance(True, int) and isinstance(u"hello", str)
    """
    if type_ is int or (PY2 and type_ is long):
        if isinstance(obj, bool):
            return False
        elif isinstance(obj, (int, long) if PY2 else int):
            return True
        # fallthrough
    elif type_ is str and PY2 and isinstance(obj, unicode):
        return True
    return isinstance(obj, type_)
