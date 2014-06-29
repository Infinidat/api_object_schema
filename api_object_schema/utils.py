def loose_isinstance(obj, type_):
    """
    Like isinstance, only handles ridiculous cases like isinstance(True, int) and isinstance(u"hello", str)
    """
    if type_ is int or type_ is long:
        if isinstance(obj, bool):
            return False
        elif isinstance(obj, (int, long)):
            return True
        # fallthrough
    elif type_ is str and isinstance(obj, unicode):
        return True
    return isinstance(obj, type_)
