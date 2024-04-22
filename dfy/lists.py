from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class DestinationList(models.TextField):
    description = "Stores a list of strings"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return value

    def validate(self, value, model_instance):
        if not all(isinstance(item, str) for item in value):
            raise ValidationError(
                _("All elements of the list must be strings."),
                code='invalid_list',
            )

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return value