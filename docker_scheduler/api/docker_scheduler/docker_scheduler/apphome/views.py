#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.http import Http404

from models import Image, Host, Container

from serializers import HostSerializer
from serializers import ImageSerializer
from serializers import ContainerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ImageView(APIView):
    """创建一个镜像;
       列出所有的镜像或, 根据 Image db 字段过滤出相应的镜像;

    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            images = Image.objects.all()
            kwargs = request.GET.dict()
            images = images.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not images:
                raise Http404

        # 没有 url 参数，就返回所有的 Image
        else:
            images = Image.objects.all()

        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    # 创建一个镜像
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(APIView):
    """根据 pk 获取镜像"""

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    # 获取镜像
    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    # 更新镜像
    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除镜像
    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HostView(APIView):
    """创建一个主机;
       列出所有的主机或, 根据 Host db 字段过滤出相应的主机;

    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            hosts = Host.objects.all()
            kwargs = request.GET.dict()
            hosts = hosts.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not hosts:
                raise Http404

        # 没有 url 参数，就返回所有的 host
        else:
            hosts = Host.objects.all()

        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)

    # 添加一台主机
    def post(self, request, format=None):
        serializer = HostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostDetailView(APIView):
    """根据 pk 获取主机信息"""

    def get_object(self, pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            raise Http404

    # 获取主机信息
    def get(self, request, pk, format=None):
        host = self.get_object(pk)
        serializer = HostSerializer(host)
        return Response(serializer.data)

    # 更新主机信息
    def put(self, request, pk, format=None):
        host = self.get_object(pk)
        serializer = HostSerializer(host, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除主机
    def delete(self, request, pk, format=None):
        host = self.get_object(pk)
        host.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContainerView(APIView):
    """创建一个主机;
       列出所有的主机或, 根据 Container db 字段过滤出相应的主机;

    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            containers = Container.objects.all()
            kwargs = request.GET.dict()
            containers = containers.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not containers:
                raise Http404

        # 没有 url 参数，就返回所有的 container
        else:
            containers = Container.objects.all()

        serializer = ContainerSerializer(containers, many=True)
        return Response(serializer.data)

    # 添加一台主机
    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerDetailView(APIView):
    """根据 pk 获取主机信息"""

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise Http404

    # 获取主机信息
    def get(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container)
        return Response(serializer.data)

    # 更新主机信息
    def put(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除主机
    def delete(self, request, pk, format=None):
        container = self.get_object(pk)
        container.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
