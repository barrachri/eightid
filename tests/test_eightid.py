from datetime import datetime

import pytest

from src.eightid import (
    EightID,
    packing,
    timestamp,
    unpacking,
    right_timestamp,
    generate_eightid,
)


def test_generate_eightid():
    eightid = generate_eightid()
    assert len(eightid) == 8


def test_timestamp():
    time = timestamp()

    assert isinstance(time, int)


def test_timestamp_conversion():
    assert right_timestamp(timestamp())


def test_eightid_int_bit_length():
    eightid = EightID()

    assert eightid.integer.bit_length() <= 63


def test_eightid_datetime():
    eightid = EightID()

    now = datetime.now()
    assert eightid.datetime.year == now.year
    assert eightid.datetime.month == now.month
    assert eightid.datetime.day == now.day
    assert eightid.datetime.hour == now.hour
    assert eightid.datetime.minute == now.minute
    assert eightid.datetime.second == now.second


@pytest.mark.parametrize("execution_number", range(100))
def test_eightid(execution_number):
    eightid = EightID()

    assert len(eightid.value) == 8
    assert int(eightid) == eightid.integer
    assert str(eightid) == eightid.string
    assert len(str(eightid)) <= 22
    assert isinstance(eightid.integer, int)
    assert isinstance(eightid.bytes, bytes)
    assert isinstance(str(eightid), str)
    assert isinstance(eightid.random, int)
    assert isinstance(eightid.time, int)
    assert isinstance(eightid.datetime, datetime)


def test_create_from_string():
    eightid = EightID()
    eightid_stringified = str(eightid)

    new_eightid = EightID.from_string(eightid_stringified)

    assert eightid.integer == new_eightid.integer
    assert eightid.bytes == new_eightid.bytes
    assert str(eightid) == str(new_eightid)
    assert int(eightid) == int(new_eightid)
    assert eightid.random == new_eightid.random
    assert eightid.time == new_eightid.time
    assert eightid.datetime == new_eightid.datetime


def test_create_from_int():
    eightid = EightID()
    eightid_integerified = int(eightid)
    new_eightid = eightid.from_int(eightid_integerified)

    assert eightid.integer == new_eightid.integer
    assert eightid.bytes == new_eightid.bytes
    assert str(eightid) == str(new_eightid)
    assert int(eightid) == int(new_eightid)
    assert eightid.random == new_eightid.random
    assert eightid.time == new_eightid.time
    assert eightid.datetime == new_eightid.datetime


def test_packing():
    message = b"ciao-there"
    assert packing(message) == "Y2lhby10aGVyZQ"


def test_unpacking():
    message = "Y2lhby10aGVyZQ"
    assert unpacking(message) == "ciao-there"
