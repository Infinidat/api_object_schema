from api_object_schema.utils import loose_isinstance

def test_loose_isinstance():
    for type, matching, not_matching in [
            (str, ["hello", u"hello"], [1, True, None]),
            (bool, [True, False], ["s", 1.0, 1]),
            (int, [100L, 100, 183874837847398473], [1.2, "hello", True, False]),
            (long, [100L, 100, 183874837847398473], [1.2, "hello", True, False]),
            ]:
        for m in matching:
            assert loose_isinstance(m, type)
        for m in not_matching:
            assert not loose_isinstance(m, type)
