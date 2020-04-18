from rest_framework import serializers
from apiWords.models import MandarinWord


class MandarinWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MandarinWord
        fields = "__all__"


