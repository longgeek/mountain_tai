from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Image(models.Model):
    OS_TYPES = (
        ('ubuntu', 'Ubuntu'),
        ('centos', 'Centos'),
    )
    iid = models.CharField(max_length=80)
    tag = models.CharField(max_length=20)
    created = models.CharField(max_length=40)
    repository = models.CharField(max_length=20)
    virtual_size = models.CharField(max_length=20)
    os_type = models.CharField(max_length=25, choices=OS_TYPES)
    os_version = models.CharField(max_length=20)

    class Meta:
        app_label = "apphome"


class Flavor(models.Model):
    name = models.CharField(max_length=20)
    cpu = models.IntegerField()
    mem = models.IntegerField()    # MB
    sys_disk = models.IntegerField()    # MB
    volume = models.IntegerField()     # MB
    bandwidth = models.IntegerField()  # KB

    class Meta:
        app_label = "apphome"


class HOST(models.Model):
    ip = models.CharField(max_length=150)
    port = models.CharField(max_length=20)
    image = models.ManyToManyField(Image)
    status = models.BooleanField(_("Status"), default=True)
    total_cpu = models.IntegerField()   # Cores
    total_mem = models.IntegerField()   # GB
    total_sys_disk = models.IntegerField()  # GB
    total_volume = models.IntegerField()    # GB
    total_bandwidth = models.IntegerField()    # MB

    class Meta:
        app_label = "apphome"


class Container(models.Model):
    cid = models.CharField(max_length=80)
    flavor = models.ForeignKey(Flavor)
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    host_ip = models.ForeignKey(HOST)

    class Meta:
        app_label = "apphome"
