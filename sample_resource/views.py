from django.shortcuts import render
from rest_framework import viewsets


# Create your views here.

from .models import SampleResource
from .serializers import SampleResourceSerializer

class SampleViewSet(viewsets.ModelViewSet):

    queryset = SampleResource.objects.all()
    serializer_class = SampleResourceSerializer