from rest_framework import serializers

from .models import SampleResource

class SampleResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleResource
        fields = ('text', 'figure')