#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import models
from mountain_tai.config import rediscon
import hashlib


def scheduler_host(flavor, image):
    """ scheduler host

    Base on falvor_id and image_dbid to return the information about
    flavor, image and the docker host to create container

    Author: Frazy Lee
    Author Email: frazy@thstack.com

    Params:
        flavor: int # flavor_id that define in models
        image: int # image dbid

    Return:( # 返回值
        status: INT, # execute status 0/Success, -1/other-Fault
        msgs: STRING, # the error message, when excecute fault
        results: DICT, # excecute result

    )

    Results Format:{
        'hostobject': <Host: Host object>, # Host object
        'image': <Image: Image object>, # Image object
        'image_name':  u'ubuntu:latest', # The name of iamge
        'host': u'127.0.0.1', # the docker host which will used to create new
                                container
        'port': u'2375', # the port of docker server
        'flavor':{
            'name': 'tiny',
            'mem': 128,
            'volume': 0,
            'bandwidth': 512,
            'sys_disk': 5120,
            'cpu': 1
        } # the detail info about flavor
    }
    """

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
    """ return info about container to create

    get data from body and return information that will used to create
    container

    Author: Frazy Lee
    Author Email: frazy@thstack.com

    Params:
        body: DICT # the data receive from mq

    Return:( # 返回值
        status: INT, # execute status 0/Success, -1/other-Fault
        msgs: STRING, # the error message, when excecute fault
        results: DICT, # excecute result

    )

    Results Format:{
        'status': u'', # the container status, when the container create
                         successful,this field will update
        'user_id': '2', # the user id who create this container
        'name': u'', # the name of the container, when the container create
                       successful,this field will update
        'created': u'', # the created of the new container, when the container
                          create successful,this field will update
        'hostname': u'', # the hostname of the new container, when the
                           container create successful,this field will update
        'image_name': u'ubuntu:latest', # the name of image that used to create
                                          the new container
        'id': 10L, # the new container db note, but the status is False
        'host': u'127.0.0.1', # the docker server ip
        'cid': u'', # the new container id, when the container create
                      successful,this field will update
        'command': u'', # the command of the new container
        'hostport': u'2375', # the docker server port
        'flavor':{
            'name': 'tiny',
            'mem': 128,
            'volume': 0,
            'bandwidth': 512,
            'sys_disk': 5120,
            'cpu': 1
        } # the detail info about flavor
    }
    """

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
    """ scheduler the container docker

    Get the docker host and port via the continer dbid

    Author: Frazy Lee
    Author Email: frazy@thstack.com

    Params:
        body: DICT # the data receive from mq, comprise with message_type
                     and container id

    Return:( # 返回值
        status: INT, # execute status 0/Success, -1/other-Fault
        msgs: STRING, # the error message, when excecute fault
        results: DICT, # excecute result
    )

    Results Format:{
        'host': u'127.0.0.1', # docker server ip
        'port': u'2375', # docker server port
        'cid': u'fbb29d13f350e19cc8ee246f11295...', # container id
        'message_type': 'restart_container', # operate type
        'id': '9' # container db id
    }
    """

    containerid = body.get("id")
    if containerid:
        try:
            containerobject = models.Container.objects.get(id=int(containerid))
        except:
            return (1,
                    'Error: The id is not exist or have more than one value!',
                    '')

        cid = containerobject.cid
        user_id = containerobject.user_id
        host = containerobject.host.ip
        port = containerobject.host.port
        rdic = {'cid': cid, 'host': host, 'port': port, 'user_id': user_id}
        resultdic = dict(body.items() + rdic.items())
        return (0, '', resultdic)
    else:
        return (1, 'Error: Please point the container id!', '')


def scheduler_docker(body):
    """ scheduler docker main function

    base on message_type to return create_container function or other
    message_type function

    Author: Frazy Lee
    Author Email: frazy@thstack.com

    Params:
        body: DICT # the data receive from mq, comprise with message_type
                     and container id

    Return:( # 返回值
        status: INT, # execute status 0/Success, -1/other-Fault
        msgs: STRING, # the error message, when excecute fault
        results: DICT, # excecute result
    )

    Results Format:
       base on function create_container and schedulerdocker
    """

    body = json.loads(body)
    action = body.get('message_type')

    if action == "create_container":
        return create_container(body)
    elif action:
        return schedulerdocker(body)
    else:
        return (1, 'Error: Please point the message_type!', '')


def updatedockerdb(body, protocol, server_name):
    """ update docker db

    update docker db via the container operation result

    Author: Frazy Lee
    Author Email: frazy@thstack.com

    Params:
        body: DICT # the data receive from mq, the container operation result

    Return:( # 返回值
        status: INT, # execute status 0/Success, -1/other-Fault
        msgs: STRING, # the error message, when excecute fault
        results: DICT, # excecute result
    )

    Results Format:
        the operation result
    """

    status, msgs, result = json.loads(body)
    if status == 0:
        action = result.get('message_type')
        containerid = result.get('id')
        containerobject = models.Container.objects.get(id=int(containerid))
        if action == "create_container":
            containerobject.cid = result.get('cid')
            containerobject.size = result.get('size')
            containerobject.name = result.get('name')
            containerobject.container_name = result.get('container_name')
            containerobject.command = result.get('command')
            containerobject.created = result.get('created')
            containerobject.status = result.get('status')
            containerobject.ports = result.get('ports')
            containerobject.hostname = result.get('hostname')
            containerobject.json_extra = result.get('json_extra')
            containerobject.create_status = True
            containerobject.save()
            url = protocol + result.get('username') + '.' + server_name
            urlvalue = result.get('host') + ":" + result.get('www_port')
            rediscon.set(url, urlvalue)
        elif action == "start_container":
            url = protocol + result.get('username') + '.' + server_name
            urlvalue = result.get('host') + ":" + result.get('www_port')
            rediscon.set(url, urlvalue)
        elif action == "delete_container":
            containerobject.delete()
            cid = result.get('cid')
            keyslist = rediscon.keys(cid[0:12] + '*')
            if keyslist:
                rediscon.delete(*keyslist)
        elif action == "stop_container" or action == "restart_container":
            containerobject.status = result.get('status')
            containerobject.save()
            cid = result.get('cid')
            keyslist = rediscon.keys(protocol+cid[0:12] + '*')
            if keyslist:
                rediscon.delete(*keyslist)
        elif action == "console_container":
            username = result.get("username")
            cid = result.get('cid')
            host = result.get("host")
            console = result.get('console')
            for key, value in console.items():
                rawstr = username + cid + key
                md5rawstr = protocol+cid[0:12] +\
                    hashlib.md5(rawstr).hexdigest()[0:12] + '.' + server_name
                rediscon.set(md5rawstr, host+":" + str(value["public_port"]))
                result['console'][key]['url'] = md5rawstr
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
