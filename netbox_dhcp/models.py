from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel
from ipam.models import IPAddress, Prefix


class DHCPServer(NetBoxModel):
    name = models.CharField(
        unique=True,
    )
    api_token = models.CharField()
    api_url = models.URLField(
        unique=True,
    )
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
    mac_address = models.CharField( #TO SET UNIQUE INSENSITIVE
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$',
                message=_('Enter a valid MAC Addres like a1:b2:c3:d4:e5:f6.')
            )
        ],
    )
    status = models.CharField(
        max_length=17,
        default='inactive',
    )
    dhcp_server = models.ForeignKey(
        to=DHCPServer,
        verbose_name='DHCP Server',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['mac_address'],
                name='unique_mac_address_case_insensitive',
                condition=models.Q(mac_address__iexact=models.functions.Upper('mac_address'))
            )
        ]
        ordering = ('ip_address', 'mac_address')

    def get_absolute_url(self):
        return self.ip_address.get_absolute_url()

    def __str__(self):
        return f'{self.ip_address} {self.mac_address}'
