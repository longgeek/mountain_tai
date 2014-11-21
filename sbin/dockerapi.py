#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import django
django.setup()
import models


def create_container(user,
                     image,
                     flavor,
                     name,
                     ports=None,
                     command=None,
                     hostname=None):
    image = models.Image.objects.get(id=int(image))
    hostlist = models.Host.objects.all()
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
            if image.tag and image.repository:
                image_name = image.repository + ':' + image.tag
            else:
                image_name = image.iid
            docker_conn = docker.Client(
                base_url="tcp://" + hostip + ":" + host.port)
            newcontainer = docker_conn.create_container(
                name=name,
                image=image_name,
                ports=ports,
                command=command,
                tty=True,
                detach=True,
                stdin_open=True,
            )
            try:
                docker_conn.start(container=newcontainer['Id'])
            except Exception, msgs:
                return (1, msgs, '')
            # container_db = models.Container(cid=newcontainer['Id'][:12],
            #                                 flavor=flavor,
            #                                 image=image,
            #                                 user=user,
            #                                 host_ip=hostip,
            #                                 name=name
            #                                 ports=port,
            #                                 hostname=hostname,
            #                                 created=str_created,
            #                                 status=status,
            #                                 command=command,
            #                                 size=size)
            # container_db.save()
            return (0, '', 'create success')

        else:
            continue
    return (1, 'All host full', '')


def delete_container(deleteid=None):
    if deleteid:
        try:
            containerobject = models.Container.objects.get(id=int(deleteid))
            containerid = containerobject.cid
            host = containerobject.host
            cli = docker.Client(
                base_url="tcp://" + host.ip + ":" + host.port)
            cli.stop(containerid)
            cli.remove_container(containerid)
            containerobject.delete()
            return (0, 'delete success', '')
        except:
            return (2, 'the container is not existed or is invalid!', '')
    else:
        return (1, 'please gave the id of container to delete', '')

if __name__ == "__main__":
    image = models.Image.objects.all()[0]
    print create_container(user='1',
                           image=image,
                           flavor='1',
                           name="frazy2",
                           command='/bin/bash')
