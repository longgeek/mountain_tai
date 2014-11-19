#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from docker_scheduler import container
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting")
import models
from docker import Client
import pdb
hostlist = models.Host.objects.all()
for host in hostlist:
    cli = Client(base_url="tcp://" + host.ip + ":" + host.port)
    try:
        containers = cli.containers(all=True, size=True)
        if not host.status:
            host.status = True
            host.save()
        dbcon = models.Container.objects.filter(host=host).order_by("created")
        dbcontainers = [{u'Status': container.status, u'Created': int(container.created), u'Image': container.image.repository + ":" + container.image.tag, u'Ports': container.ports.split(), u'Command': container.command, u'Names': container.name.split(), u'SizeRw': int(container.size), u'SizeRootFs': 0, u'Id': container.cid} for container in dbcon]
        for dbc in dbcontainers:
            if dbc in containers:
                containers.remove(dbc)
            else:
                dbcobject = models.Container.objects.get(cid=dbc['Id'])
                dbcobject.delete()
        for container in containers:
            imageinfo = container['Image'].split(":")
            imageobject = models.Image.objects.get(repository=imageinfo[0], tag=imageinfo[1])
            containernew = models.Container(cid=container['Id'],
                                            size=container['SizeRw'],
                                            flavor_id='1',
                                            image=imageobject,
                                            user_id='1',
                                            host=host,
                                            name=' '.join(container['Names']),
                                            command=container['Command'],
                                            created=container['Created'],
                                            status=container['Status'],
                                            ports=' '.join(container['Ports']),
                                            hostname='localhost')
            containernew.save()

    except Exception, e:
        host.status = False
        host.save()
