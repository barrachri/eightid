import pytest
from django.db import connection
from django.core.exceptions import ValidationError

from src.gid import GID, InvalidGID, django
from django_app.app.models import AppModel


class TestModel:

    def test_unique_by_default(self):
        field = django.GIDField()
        assert field.unique

    def test_force_not_unique(self):
        field = django.GIDField(unique=False)
        assert field.unique is False

    def test_to_python(self):
        field = django.GIDField()
        out = field.to_python(16986436871731377766)
        assert isinstance(out, GID)

    def test_to_python_invalid_value(self):
        field = django.GIDField()
        with pytest.raises(InvalidGID):
            field.to_python('xxx')

    def test_to_python_class_string(self):
        field = django.GIDField()
        out = field.to_python('w6vDgXAoFsKcw5DCjQ')
        assert isinstance(out, GID)

    def test_prep(self):
        field = django.GIDField()
        out = field.get_db_prep_value(GID.from_string('w6vCu8OyVjsldmY'), connection=connection)
        assert out == 16986436871731377766

    def test_prep_none(self):
        field = django.GIDField()
        out = field.get_db_prep_value(None, connection=connection)
        assert out is None


class TestAppModel:

    @pytest.mark.django_db
    def test_value_created(self):
        model = AppModel.objects.create()

        assert isinstance(model.id, GID)

    @pytest.mark.django_db
    def test_persist_reload(self):
        model = AppModel.objects.create()
        model.save()
        gid = AppModel.objects.values_list('id', flat=True)[0]

        assert model.id.value == gid.value

    @pytest.mark.django_db
    def test_filter(self):
        AppModel.objects.create()
        model = AppModel.objects.create()
        AppModel.objects.create()
        gid = AppModel.objects.filter(id=model.id).values_list('id', flat=True)[0]

        assert isinstance(model.id, GID)
        assert model.id.value == gid.value

