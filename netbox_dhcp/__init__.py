from netbox.plugins import PluginConfig

def init_custom_field():
    from extras.models import CustomField
    from core.models import ObjectType
    from .models import DHCPServer, Prefix

    dhcpserver_ot_id = ObjectType.objects.get_for_model(DHCPServer).id
    customfield_name = "netbox_dhcp_dhcp_server"
    defaults = {"type":"object","related_object_type_id":dhcpserver_ot_id,"name":customfield_name,"label":"DHCP Server","unique":False}
    try:
        obj = CustomField.objects.get(name=customfield_name)
        for key, value in defaults.items():
            setattr(obj, key, value)
        obj.object_types.set([ObjectType.objects.get_for_model(Prefix)])
        obj.save()
    except CustomField.DoesNotExist:
        obj = CustomField(**defaults)
        obj.save()
        obj.object_types.set([ObjectType.objects.get_for_model(Prefix)])
        obj.save()

class NetBoxDHCP(PluginConfig):
    name = 'netbox_dhcp'
    verbose_name = 'NetBox DHCP'
    description = 'Manage Dnsmasq DHCP with NetBox'
    version = '0.1'
    base_url = 'netbox-dhcp'

    def ready(self):
        super().ready()
        from . import signals

        init_custom_field()

config = NetBoxDHCP