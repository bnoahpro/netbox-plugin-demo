from netbox.forms import NetBoxModelForm
from netbox_dhcp.models import MacAddress



class MacAddressEditForm(NetBoxModelForm):
    class Meta:
        model = MacAddress
        fields = ['mac_address', 'ip_address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ip_address'].disabled = True #To fix

