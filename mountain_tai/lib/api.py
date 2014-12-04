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
                         'hostobject': host,
                         'hostport': hostport,
                         'image_name': image_name,
                         'image': image,
                         'flavor': newflavor}
            return (0, '', resultdic)
        else:
            continue
    return (1, 'Error: All of the Docker host is not idle resources!', '')


def create_container(body):
    flavor = body.get('flavor_id')
    image = body.get('image')
    hostdic = scheduler_host(
        flavor=flavor,
        image=image,
    )
    if hostdic[0] == 0:
        hostdic = hostdic[2]
    else:
        return hostdic
    containerobject = models.Container(
        flavor_id=flavor,
        image=hostdic.get("image"),
        user_id=body.get('user_id'),
        host=hostdic.get('hostobject'),
    )
    containerobject.save()
    body.pop('image')
    body.pop('host')
    body.pop('flavor_id')

    hostdic.pop('image')
    hostdic.pop('hostobject')

    hostdic['id'] = containerobject.id
    resultdic = dict(body.items() + hostdic.items())
    return (0, '', resultdic)


def schedulerdocker(body):
    containerid = body.get("id")
    if containerid:
        try:
            containerobject = models.Container.objects.get(id=int(containerid))
        except:
            return (1,
                    'Error: The id is not exist or have more than one value!',
                    '')

        cid = containerobject.cid
        host = containerobject.host.ip
        port = containerobject.host.port
        rdic = {'cid': cid, 'host': host, 'port': port}
        resultdic = dict(body.items() + rdic.items())
        return (0, '', resultdic)
    else:
        return (1, 'Error: Please point the container id!', '')


def scheduler_docker(body):
    body = json.loads(body)
    action = body.get('message_type')

    if action == "create_container":
        return create_container(body)
    elif action:
        return schedulerdocker(body)
    else:
        return (1, 'Error: Please point the message_type!', '')


def updatedockerdb(body):
    print body
    status, msgs, result = json.loads(body)
    if status == 0:
        action = result.get('message_type')
        containerid = result.get('id')
        containerobject = models.Container.objects.get(id=int(containerid))
        if action == "create_container":
            containerobject.cid = result.get('cid')
            containerobject.size = result.get('size')
            containerobject.name = result.get('name')
            containerobject.command = result.get('command')
            containerobject.created = result.get('created')
            containerobject.status = result.get('status')
            containerobject.ports = result.get('ports')
            containerobject.hostname = result.get('hostname')
            containerobject.create_status = True
            containerobject.save()
        elif action == "delete_container":
            containerobject.delete()
        else:
            containerobject.status = result.get('status')
            containerobject.save()
        return (0, '', result)
    else:
        action = msgs.get('message_type')
        if action == "create_container":
            containerid = msgs.get('id')
            containerobject = models.Container.objects.get(id=int(containerid))
            containerobject.delete()
        return status, msgs.get('error'), result
