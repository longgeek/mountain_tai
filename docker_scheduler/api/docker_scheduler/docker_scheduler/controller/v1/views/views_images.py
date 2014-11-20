#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.http import Http404

from docker_scheduler.apphome.models import Image

from serializers import ImageSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ImageView(APIView):
    """列出所有镜像，或者根据 url 参数进行过滤,
       重新定义 get 请求

    路径:
       GET /images/ HTTP/1.1
       Content-Type: application/json
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


class ImageCreateView(APIView):
    """创建一个镜像, 重新定义 post 请求

    路径:
       POST /images/create HTTP/1.1
       Content-Type: application/json
    """

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUpdateView(APIView):
    """更新一个镜像, 重新定义 put 请求

    路径:
       PUT /images/(pk)/update HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteView(APIView):
    """删除一个镜像, 重新定义 delete 请求

    路径:
       DELETE /images/(pk)/delete HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetailView(APIView):
    """根据 pk 获取镜像, 重新定义 get 请求

    路径:
       get /images/(pk)/ HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
