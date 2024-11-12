from netbox.plugins.templates import PluginTemplateExtension


class ReservationInfo(PluginTemplateExtension):
    model = 'ipam.ipaddress'

    def buttons(self):
        return self.render('netbox_dhcp/reservation_recreate_button.html')

    def right_page(self):
        return (
            self.render('netbox_dhcp/mac_address.html')
        )

class DHCPInfo(PluginTemplateExtension):
    model = 'ipam.prefix'

    def buttons(self):
        return self.render('netbox_dhcp/synchronize_dhcp_button.html')


template_extensions = [ReservationInfo, DHCPInfo]