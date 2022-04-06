import os
import time
import base64
import datetime
from typing import List
from functools import cached_property

#  01 Jan 2022 00:00:00.000 GMT
epoch = 1640995200000

# 8 bytes
raw_len = 8

size = 64
timestamp_bits = 32


def timestamp() -> int:
    """Seconds from epoch"""
    now = time.time_ns() // 1_000_000
    cid_epoch = now - epoch
    return cid_epoch


def random_bits(n: int) -> List[int]:
    return list(os.urandom(n))


def generate_gid() -> List[int]:
    id = [0] * raw_len
    now = timestamp()

    id[0] = (now >> 24) & 0xFF
    id[1] = (now >> 16) & 0xFF
    id[2] = (now >> 8) & 0xFF
    id[3] = (now) & 0xFF

    randb = random_bits(4)

    id[4] = randb[0]
    id[5] = randb[1]
    id[6] = randb[2]
    id[7] = randb[3]

    return id


class InvalidXid(Exception):
    pass


class GID(object):
    """
    A short id base on 8 bytes (it fits in a PostgreSQL BigInt).

    16 bites bytes are taken from the timestamp.
    16 bites bytes are random generated (4.294.967.296 of unique numbers).

    The string representation is based on urlsafe_b64, with the padding stripped.

    So it's quite compact, fitting in less than 20 chars.

    """

    __slots__ = ("value", "__dict__")

    def __init__(self, id=None):
        if id is None:
            id = generate_gid()
        self.value = id

    def __str__(self) -> str:
        return self.string

    def __int__(self) -> int:
        return self.int

    @cached_property
    def string(self) -> str:
        byte_value = self.bytes
        return packing(byte_value)

    @cached_property
    def random(self) -> int:
        """Return the random part of the GID."""
        return (
            self.value[4] << 24
            | self.value[5] << 16
            | self.value[6] << 8
            | self.value[7]
        )

    @cached_property
    def datetime(self) -> datetime.datetime:
        """Return the timestamp as datetime."""
        return datetime.datetime.fromtimestamp(self.time)

    @cached_property
    def int(self):
        """Return the GID as int."""
        return int.from_bytes(self.value, "big")

    @cached_property
    def time(self) -> int:
        """Return the timestamp of the GID."""
        return (
            self.value[0] << 24
            | self.value[1] << 16
            | self.value[2] << 8
            | self.value[3]
        )

    @cached_property
    def bytes(self) -> bytes:
        """Return the GID as bytes."""
        return "".join(map(chr, self.value)).encode("utf-8")

    @classmethod
    def from_string(cls, s: str) -> "GID":
        value = list(map(ord, unpacking(s)))
        return cls(value)

    @classmethod
    def from_int(cls, i: int) -> "GID":
        value = list(i.to_bytes(8, "big"))
        return cls(value)


def packing(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def unpacking(s: str):
    padded_s = s + "=="
    return base64.urlsafe_b64decode(padded_s.encode("utf-8")).decode("utf-8")
