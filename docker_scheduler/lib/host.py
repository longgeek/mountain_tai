#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from docker import Client


def check_host(ip, port):
    """ 检测 Docker Host 是否开启
    Params:
        ip:   str;    Docker Host IP 地址
        port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results)
    """
    conn = Client(base_url='tcp://%s:%s' % (ip, port),
                  timeout=5,
                  tls=False)
    try:
        return (1, '', (conn.info(), conn.version()))
    except:
        return (0, '', '')


def connect_host(ip, port):
    """ 与 Docker 主机建立连接
    Params:
        ip:   str;  Docker Host IP 地址
        port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results)
    """

    conn = Client(base_url='tcp://%s:%s' % (ip, port),
                  timeout=5,
                  tls=False)

    try:
        conn.info()
        return (1, '', conn)
    except:
        return (0, 'TimeOut', '')
