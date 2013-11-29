from django.shortcuts import render
from rest_framework import viewsets
from models import Image, Host, Container
from serializers import ImageSerializer
from serializers import HostSerializer
from serializers import ContainerSerializer

# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
