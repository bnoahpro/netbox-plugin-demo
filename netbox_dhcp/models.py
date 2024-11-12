from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from ipam.models import IPAddress, Prefix

class MacAddress(NetBoxModel):
    mac_address = models.CharField(
        max_length=17,
        unique=True
    )
    ip_address = models.OneToOneField(
        to=IPAddress,
        verbose_name='IP Address',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.mac_address

    def get_absolute_url(self):
        return self.ip_address.get_absolute_url()

class DHCPReservation(NetBoxModel):
    ip_address = models.OneToOneField(
        to=IPAddress,
        verbose_name='IP Address',
        on_delete=models.CASCADE,
    )
    mac_address = models.OneToOneField(
        to=MacAddress,
        verbose_name='MAC Address',
        on_delete=models.CASCADE,
    )
    is_reserved = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ('ip_address', 'mac_address')

    def __str__(self):
        return f'{self.ip_address}:{self.mac_address}'

class DHCPServer(NetBoxModel):
    name = models.CharField(
        unique=True,
    )
    api_token = models.CharField()
    api_url = models.URLField()

    def __str__(self):
        return f'{self.name}'