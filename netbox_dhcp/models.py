from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from ipam.models import IPAddress, Prefix

class DHCPServer(NetBoxModel):
    name = models.CharField(
        unique=True,
    )
    api_token = models.CharField()
    api_url = models.URLField()
    ssl_verify = models.BooleanField(
        verbose_name='SSL Verify',
        default=True
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_dhcp:dhcpserver', args=[self.pk])

class DHCPReservation(NetBoxModel):
    ip_address = models.OneToOneField(
        to=IPAddress,
        verbose_name='IP Address',
        on_delete=models.CASCADE,
    )
    mac_address = models.CharField(
        max_length=17,
        unique=True
    )
    status = models.CharField(
        max_length=17,
        default='inactive',
    )
    dhcpserver = models.ForeignKey(
        to=DHCPServer,
        verbose_name='DHCP Server',
        on_delete=models.CASCADE,
    )
    class Meta:
        ordering = ('ip_address', 'mac_address')

    def __str__(self):
        return f'{self.ip_address} {self.mac_address}'

