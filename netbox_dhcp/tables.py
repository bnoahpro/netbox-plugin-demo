import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_dhcp.models import DHCPServer, DHCPReservation


class DHCPServerTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = DHCPServer
        fields = ('name', 'api_token', 'api_url')


class DHCPReservationTable(NetBoxTable):
    ip_address = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = DHCPReservation
        fields = ('ip_address', 'mac_address', 'status')
