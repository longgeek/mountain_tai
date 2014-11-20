#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from kombu import Connection, Exchange, Queue
import dockerapi


actiontype = 'create_container'
types = {
    'create_container': {
        'queue_name': 'create_container_queue',
        'router_key': 'create_container_router',
        'exchange_name': 'create_container_exchange',
    },
    'start_container': {
        'queue_name': 'start_container_queue',
        'router_key': 'start_container_router',
        'exchange_name': 'start_container_exchange',
    },
    'stop_container': {
        'queue_name': 'stop_container_queue',
        'router_key': 'stop_container_router',
        'exchange_name': 'stop_container_exchange',
    },
    'restart_container': {
        'queue_name': 'restart_container_queue',
        'router_key': 'restart_container_router',
        'exchange_name': 'restart_container_exchange',
    },
    'delete_container': {
        'queue_name': 'delete_container_queue',
        'router_key': 'delete_container_router',
        'exchange_name': 'delete_container_exchange',
    },
}


queue_name = types[actiontype]['queue_name']
print queue_name
router_key = types[actiontype]['router_key']
exchange_name = types[actiontype]['exchange_name']
exchange = Exchange(exchange_name,
                    'direct',
                    durable=True)
queue = Queue(queue_name,
              exchange=exchange,
              routing_key=router_key)


def process_media(body, message):

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

    # print body
    message.ack()

# connections
with Connection('amqp://guest:guest@192.168.8.239:5672//') as conn:
    # consume
    with conn.Consumer(queue, callbacks=[process_media]) as consumer:
        while True:
            conn.drain_events()
