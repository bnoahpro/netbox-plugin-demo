from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

dhcpserver_buttons = [
    PluginMenuButton(
        link='plugins:netbox_dhcp:dhcpserver_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_dhcp:dhcpserver_list',
        link_text='DHCP Servers',
        buttons=dhcpserver_buttons
    ),
)

menu = PluginMenu(
    label='DHCP',
    groups=(
        ('DHCP Servers',menu_items),
    ),
    icon_class='mdi mdi-router'
)