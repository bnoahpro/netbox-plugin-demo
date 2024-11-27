from netbox.forms import NetBoxModelForm
from netbox_dhcp.models import DHCPReservation, DHCPServer

class DHCPReservationEditForm(NetBoxModelForm):
    class Meta:
        model = DHCPReservation
        fields = ['mac_address', 'ip_address', 'dhcpserver']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DHCPServerEditForm(NetBoxModelForm):
    class Meta:
        model = DHCPServer
        fields = ['name', 'api_token', 'api_url', 'ssl_verify']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

