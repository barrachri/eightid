from datetime import datetime

import pytest

from gid import GID, packing, timestamp, unpacking, generate_gid


def test_generate_gid():
    gid = generate_gid()
    assert len(gid) == 8


def test_timestamp():
    time = timestamp()
    assert isinstance(time, int)

@pytest.mark.parametrize('execution_number', range(100))
def test_gid(execution_number):
    gid = GID()

    assert len(gid.value) == 8
    assert int(gid) == gid.int
    assert str(gid) == gid.string
    assert len(str(gid)) <= 20
    assert isinstance(gid.int, int)
    assert isinstance(gid.bytes, bytes)
    assert isinstance(str(gid), str)
    assert isinstance(gid.random, int)
    assert isinstance(gid.time, int)
    assert isinstance(gid.datetime, datetime)

def test_create_from_string():
    gid = GID()
    gid_stringified = str(gid)

    new_gid = GID.from_string(gid_stringified)

    assert gid.int == new_gid.int
    assert gid.bytes == new_gid.bytes
    assert str(gid) == str(new_gid)
    assert int(gid) == int(new_gid)
    assert gid.random == new_gid.random
    assert gid.time == new_gid.time
    assert gid.datetime == new_gid.datetime

def test_create_from_int():
    gid = GID()
    gid_integerified = int(gid)
    new_gid = GID.from_int(gid_integerified)

    assert gid.int == new_gid.int
    assert gid.bytes == new_gid.bytes
    assert str(gid) == str(new_gid)
    assert int(gid) == int(new_gid)
    assert gid.random == new_gid.random
    assert gid.time == new_gid.time
    assert gid.datetime == new_gid.datetime


def test_packing():
    message = b"ciao-there"
    assert packing(message) == 'Y2lhby10aGVyZQ'

def test_unpacking():
    message = 'Y2lhby10aGVyZQ'
    assert unpacking(message) == 'ciao-there'


