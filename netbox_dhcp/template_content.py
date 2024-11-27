from netbox.plugins.templates import PluginTemplateExtension


class ReservationInfo(PluginTemplateExtension):
    model = 'ipam.ipaddress'

    def buttons(self):
        return self.render('netbox_dhcp/dhcpreservation_recreate_button.html')

    def right_page(self):
        return (
            self.render('netbox_dhcp/dhcpreservation.html')
        )

class DHCPSync(PluginTemplateExtension):
    model = 'netbox-dhcp.dhcpserver'

    def buttons(self):
        return self.render('netbox_dhcp/synchronize_dhcp_button.html')

template_extensions = [ReservationInfo, DHCPSync]