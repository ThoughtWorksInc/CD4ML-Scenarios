from cd4ml.utils.utils import get_uuid


def test_uuid_unique():
    # assert they are unique
    uuids = [get_uuid() for _ in range(100)]
    assert len(uuids) == len(set(uuids))
