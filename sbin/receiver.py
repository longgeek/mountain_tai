#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from kombu import Connection, Exchange, Queue
import dockerapi

from settings import RABBITMQ_URLS

actiontype = 'create_container'
types = {
    'create_container': {
        'queue_name': 'create-container-queue',
        'router_key': 'create.container.router',
        'exchange_name': 'container',
    },
    'start_container': {
        'queue_name': 'start-container-queue',
        'router_key': 'start.container.router',
        'exchange_name': 'container',
    },
    'stop_container': {
        'queue_name': 'stop-container-queue',
        'router_key': 'stop.container.router',
        'exchange_name': 'container',
    },
    'restart_container': {
        'queue_name': 'restart-container-queue',
        'router_key': 'restart.container.router',
        'exchange_name': 'container',
    },
    'delete_container': {
        'queue_name': 'delete-container-queue',
        'router_key': 'delete.container.router',
        'exchange_name': 'container',
    },
}

queue_name = types[actiontype]['queue_name']
router_key = types[actiontype]['router_key']
exchange_name = types[actiontype]['exchange_name']
exchange = Exchange(exchange_name,
                    type='topic',
                    durable=True)
queue = Queue(queue_name,
              exchange=exchange,
              routing_key=router_key)


def action(body, message):

    print body
    user = body.get('user_id')
    imageid = body.get('image')
    flavor = body.get('flavor_id')
    name = body.get('name')
    command = body.get('command')
    hostname = body.get('hostname')
    ports = body.get('ports')
    print dockerapi.create_container(
        user=user,
        image=imageid,
        flavor=flavor,
        name=name,
        ports=ports,
        command=command,
        hostname=hostname
    )
    message.ack()

# connections
with Connection(RABBITMQ_URLS) as conn:
    # consume
    with conn.Consumer(queue, callbacks=[action]) as consumer:
        while True:
            conn.drain_events()
