from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', unique=True)
    connected_to = models.ForeignKey('Router', on_delete=models.CASCADE, null=True, blank=True, related_name="devices")

    def __str__(self):
        return self.name

class Router(models.Model):
    name = models.CharField(max_length=100)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', unique=True)
    connected_routers = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.name
