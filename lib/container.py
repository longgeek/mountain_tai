#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from host import connect_host


def get_containers(host_ip, host_port, quiet=False, all=False, size=False):
    """ 获取 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号
        quiet:     bool; 是否只显示容器 ID 号
        all:       bool; 是否显示所有的容器，包括stop
        size：     bool; 是否显示容器的大小

    Return:
        (status,
         msgs,
         results) # results: 返回一台 Docker 主机上所有的容器列表
    """
    host_object = connect_host(host_ip, host_port)
    if host_object[0]:
        containers = host_object[2].containers(quiet, all, size)
        return (1, '', containers)
    else:
        return (0, host_object[1], '')


def create_containers():
    """ 获取 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results)
    """
    pass
