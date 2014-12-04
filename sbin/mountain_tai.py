#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "docker_scheduler.lib.dockerconfig.setting")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import pika
import uuid
import multiprocessing
import threading
import simplejson as json
from docker_scheduler.lib import schedulerapi

MQ_HOST = '192.168.8.8'
MQ_PORT = 5672
QUEUE_DOCKER_SCHEDULER = 'docker_scheduler'
QUEUE_DOCKER_TASK = 'docker_task'

WORKERS = 8
PROCESS_PER_WORKER = 300


class Send(object):
    """控制中心类"""
    _instance = None
    connection = None
    channel = None

    def __init__(self):

        # 定义接收返回消息的队列
        self.channel.basic_consume(self.on_response,
                                   no_ack=False,
                                   queue=self.callback_queue)
        self.response = {}
        pass

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(Send, self).__new__(
                self, *args, **kwargs)

            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=MQ_HOST))

            self.channel = self.connection.channel()

            # 定义接收返回消息的队列
            result = self.channel.queue_declare(exclusive=True)
            self.callback_queue = result.method.queue

        return self._instance

    # 定义接收到返回消息的处理方法
    def on_response(self, channel, method, props, body):
        print 'message from frazy: ', body
        self.response[props.correlation_id] = body

    def request(self, body):
        corr_id = str(uuid.uuid4())
        self.response[corr_id] = None

        # 发送计算请求，并设定返回队列和correlation_id
        self.channel.basic_publish(exchange='',
                                   routing_key=QUEUE_DOCKER_TASK,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=corr_id,
                                   ),
                                   body=body)

        while self.response[corr_id] is None:
            self.connection.process_data_events()
        return self.response[corr_id]


class Center(object):
    """控制中心类"""
    _instance = None
    connection = None
    channel = None

    def __init__(self):

        # 定义接收返回消息的队列
        self.channel.queue_declare(queue=QUEUE_DOCKER_SCHEDULER,
                                   durable=True)
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(self.on_response,
                                   no_ack=False,
                                   queue=QUEUE_DOCKER_SCHEDULER)

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(Center, self).__new__(
                self, *args, **kwargs)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=MQ_HOST))

            self.channel = self.connection.channel()

        return self._instance

    def start(self):
        self.channel.start_consuming()

    # 定义接收到返回消息的处理方法
    def on_response(self, ch, method, props, body):
        """
            1. 先给 docker_task 发送消息
            2. 然后给docker_scheduler返回消息
        """
        send = Send()
        (status, msgs, resultdic) = schedulerapi.scheduler_docker(body)
        # print status, msgs, results
        response = send.request(json.dumps(resultdic))
        # response = send.request(body)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id,
                         ),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print '---------------\n'


class MyThread(threading.Thread):
    """自定义线程类，继承threading.Thread"""

    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func()


if __name__ == "__main__":

    def run():
        center = Center()
        center.start()

        # threads = []
        # for i in range(PROCESS_PER_WORKER):
        #     mythread = MyThread(center.start)
        #     print 'Process: ', os.getpid(), 'thread = ', mythread
        #     threads.append(mythread)
        # for thread in threads:
        #     thread.start()
        # for thread in threads:
        #     thread.join()

    for i in range(WORKERS):

        p = multiprocessing.Process(target=run)
        p.start()
        print 'i = ', i, '   process id = ', p.pid
    # center.channel.start_consuming()