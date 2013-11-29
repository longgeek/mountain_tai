from models import Image, Host, Container
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('iid', 'tag', 'created', 'repository', 'virtual_size', 'os_type', 'os_version')


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('ip', 'port', 'image', 'status', 'total_cpu', 'total_mem', 'total_sys_disk', 'total_volume', 'total_bandwidth')


class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        exclude = ()
