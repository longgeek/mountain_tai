#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import models


def scheduler_host(flavor, image):
    hostlist = models.Host.objects.all()
    image = models.Image.objects.get(id=int(image))
    newflavor = models.Flavor[flavor]
    for host in hostlist:
        containerlist = host.container_set.all()
        totalcpu = 0
        totalmem = 0
        totaldisk = 0
        for container in containerlist:
            fla = models.Flavor[container.flavor_id]
            totalcpu += fla['cpu']
            totalmem += fla['mem']
            totaldisk += fla['sys_disk']
        if int(host.total_cpu) - totalcpu >= newflavor['cpu'] and\
                int(host.total_mem) - totalmem >= newflavor['mem'] and\
                int(host.total_sys_disk) - totaldisk >= newflavor['mem']:
            hostip = host.ip
            hostport = host.port
            if image.tag and image.repository:
                image_name = image.repository + ':' + image.tag
            else:
                image_name = image.iid
            resultdic = {'host': hostip,
                         'hostport': hostport,
                         'image_name': image_name,
                         'flavor': newflavor}
            return (0, '', resultdic)
        else:
            continue
    return (1, 'All host full', '')


def create_container(body):
    flavor = body.get('flavor_id')
    image = body.get('image')
    hostdic = scheduler_host(
        flavor=flavor,
        image=image,
    )
    body.pop('image')
    body.pop('flavor_id')
    body.pop('host')
    resultdic = dict(body.items() + hostdic[2].items())
    return (0, '', resultdic)


def schedulerdocker(body):
    print body
    body = json.loads(body)
    containerid = body.get("id")
    if containerid:
        containerobject = models.Container.objects.get(id=int(containerid))
        cid = containerobject.cid
        host = containerobject.host.ip
        port = containerobject.host.port
        rdic = {'containerid': cid, 'host': host, 'port': port}
        body.pop('id')
        resultdic = dict(body.items() + rdic.items())
        return (0, '', resultdic)
    else:
        return (1, 'please point the container id', '')


def scheduler_docker(body):
    body = json.loads(body)
    action = body.get('message_type')
    if action == "create_container":
        return create_container(body)
    elif action:
        return schedulerdocker(body)
    else:
        return (1, 'please point the message_type', '')
