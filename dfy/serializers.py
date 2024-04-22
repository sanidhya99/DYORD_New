from rest_framework import serializers
from .models import *


class PlanSearializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
