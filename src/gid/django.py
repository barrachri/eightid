from django.core.exceptions import ValidationError
from django.db.models.fields import BigIntegerField
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import GID


class GIDField(BigIntegerField):
    default_error_messages = {
        "invalid": _("'%(value)s' is not a valid GID."),
    }
    description = "GID: a (really) short id, fitting in 8 bytes"

    def __init__(self, *args, **kwargs) -> None:
        # unique=True is a much more sensible default for UUIDs
        kwargs.setdefault("unique", True)
        kwargs["default"] = GID
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return value

        return int(value)

    def to_python(self, value):
        if isinstance(value, GID):
            return value

        elif isinstance(value, int):
            return GID.from_int(value)

        elif isinstance(value, str):
            return GID.from_string(value)

        return value

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value
        return GID.from_int(value)
