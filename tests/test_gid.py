from datetime import datetime

import pytest

from src.gid import (
    GID,
    packing,
    timestamp,
    unpacking,
    generate_gid,
    right_timestamp,
)


def test_generate_gid():
    gid = generate_gid()
    assert len(gid) == 8


def test_timestamp():
    time = timestamp()

    assert isinstance(time, int)


def test_timestamp_conversion():
    assert right_timestamp(timestamp())


def test_gid_int_bit_length():
    gid = GID()

    assert gid.integer.bit_length() <= 63


def test_gid_datetime():
    gid = GID()

    now = datetime.now()
    assert gid.datetime.year == now.year
    assert gid.datetime.month == now.month
    assert gid.datetime.day == now.day
    assert gid.datetime.hour == now.hour
    assert gid.datetime.minute == now.minute
    assert gid.datetime.second == now.second


@pytest.mark.parametrize("execution_number", range(100))
def test_gid(execution_number):
    gid = GID()

    assert len(gid.value) == 8
    assert int(gid) == gid.integer
    assert str(gid) == gid.string
    assert len(str(gid)) <= 22
    assert isinstance(gid.integer, int)
    assert isinstance(gid.bytes, bytes)
    assert isinstance(str(gid), str)
    assert isinstance(gid.random, int)
    assert isinstance(gid.time, int)
    assert isinstance(gid.datetime, datetime)


def test_create_from_string():
    gid = GID()
    gid_stringified = str(gid)

    new_gid = GID.from_string(gid_stringified)

    assert gid.integer == new_gid.integer
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

    assert gid.integer == new_gid.integer
    assert gid.bytes == new_gid.bytes
    assert str(gid) == str(new_gid)
    assert int(gid) == int(new_gid)
    assert gid.random == new_gid.random
    assert gid.time == new_gid.time
    assert gid.datetime == new_gid.datetime


def test_packing():
    message = b"ciao-there"
    assert packing(message) == "Y2lhby10aGVyZQ"


def test_unpacking():
    message = "Y2lhby10aGVyZQ"
    assert unpacking(message) == "ciao-there"
