from docker_scheduler.apphome.models import Host
from docker_scheduler.apphome.models import Image
from docker_scheduler.apphome.models import Container
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('iid',
                  'tag',
                  'created',
                  'os_type',
                  'os_version',
                  'repository',
                  'virtual_size',)


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('ip',
                  'port',
                  'image',
                  'status',
                  'total_cpu',
                  'total_mem',
                  'total_volume',
                  'total_sys_disk',
                  'total_bandwidth',)


class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ('cid',
                  'size',
                  'host',
                  'name',
                  'image',
                  'ports',
                  'status',
                  'user_id',
                  'command',
                  'created',
                  'hostname',
                  'flavor_id',)