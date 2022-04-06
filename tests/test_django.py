import pytest
from django.db import connection
from django.core.exceptions import ValidationError

from src.eightid import EightID, InvalidEightID, django
from django_app.app.models import AppModel


class TestModel:
    def test_unique_by_default(self):
        field = django.EightIDField()
        assert field.unique

    def test_force_not_unique(self):
        field = django.EightIDField(unique=False)
        assert field.unique is False

    def test_to_python(self):
        field = django.EightIDField()
        out = field.to_python(16986436871731377766)
        assert isinstance(out, EightID)

    def test_to_python_invalid_value(self):
        field = django.EightIDField()
        with pytest.raises(InvalidEightID):
            field.to_python("xxx")

    def test_to_python_class_string(self):
        field = django.EightIDField()
        out = field.to_python("w6vDgXAoFsKcw5DCjQ")
        assert isinstance(out, EightID)

    def test_prep(self):
        field = django.EightIDField()
        out = field.get_db_prep_value(
            EightID.from_string("w6vCu8OyVjsldmY"), connection=connection
        )
        assert out == 16986436871731377766

    def test_prep_none(self):
        field = django.EightIDField()
        out = field.get_db_prep_value(None, connection=connection)
        assert out is None


class TestAppModel:
    @pytest.mark.django_db
    def test_value_created(self):
        model = AppModel.objects.create()

        assert isinstance(model.id, EightID)

    @pytest.mark.django_db
    def test_persist_reload(self):
        model = AppModel.objects.create()
        model.save()
        eightid = AppModel.objects.values_list("id", flat=True)[0]

        assert model.id.value == eightid.value

    @pytest.mark.django_db
    def test_filter(self):
        AppModel.objects.create()
        model = AppModel.objects.create()
        AppModel.objects.create()
        eightid = AppModel.objects.filter(id=model.id).values_list(
            "id", flat=True
        )[0]

        assert isinstance(model.id, EightID)
        assert model.id.value == eightid.value
