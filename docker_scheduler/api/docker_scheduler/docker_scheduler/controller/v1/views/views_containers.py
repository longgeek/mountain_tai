#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.http import Http404

from docker_scheduler.apphome.models import Container

from serializers import ContainerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ContainerView(APIView):
    """列出所有的主机或, 根据 url 参数过滤出相应的主机;

    路径:
       GET /containers/ HTTP/1.1
       Content-Type: application/json
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


class ContainerCreateView(APIView):
    """创建一个容器, 重新定义 post 请求

    路径:
       POST /containers/create HTTP/1.1
       Content-Type: application/json
    """

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerUpdateView(APIView):
    """更新一个容器, 重新定义 put 请求

    路径:
       PUT /containers/(cid)/update HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerDeleteView(APIView):
    """删除一个容器, 重新定义 delete 请求

    路径:
       DELETE /containers/(cid)/delete HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        container = self.get_object(pk)
        container.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContainerDetailView(APIView):
    """根据 pk 获取主机信息, 重新定义 get 请求

    路径:
       get /containers/(pk)/ HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container)
        return Response(serializer.data)
