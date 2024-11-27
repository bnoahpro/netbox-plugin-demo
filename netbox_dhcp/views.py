from requests import get
from netbox.views.generic import ObjectEditView, ObjectDeleteView, ObjectView, ObjectListView
from ipam.models import IPAddress, Prefix
from netbox_dhcp.forms import DHCPReservationEditForm, DHCPServerEditForm
from netbox_dhcp.models import DHCPReservation, DHCPServer
from netbox_dhcp.background_tasks import create_or_update_reservation, delete_reservation, delete_reservation_in_dhcp
from netbox_dhcp.utils import get_dhcp
from netbox_dhcp.tables import DHCPServerTable, DHCPReservationTable
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from logging import getLogger

logger = getLogger('netbox_dhcp')

# ---------------------------- #
#       DHCPReservation
# ---------------------------- #
class DHCPReservationView(ObjectView):
    queryset = DHCPReservation.objects.all()

class DHCPReservationCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()
    form = DHCPReservationEditForm

    @property
    def model_form(self):
        return self.form

class DHCPReservationEditView(DHCPReservationCreateView):
    permission_required = 'ipam.change_ipaddress'

class DHCPReservationDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()

    def delete(self, request, ip_address_id):
        ip_address = get_object_or_404(IPAddress, pk=ip_address_id)
        if hasattr(ip_address, 'dhcpreservation') and ip_address.dhcpreservation.is_reserved:
            delete_reservation.delay(
                ip_address=ip_address
            )
        return redirect(ip_address.get_absolute_url())

class DHCPReservationRecreateView(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'

    def post(self, request, ip_address_id):
        ip_address = get_object_or_404(IPAddress, pk=ip_address_id)
        create_or_update_reservation.delay(
            ip_address=ip_address
        )
        return redirect('ipam:ipaddress', pk=ip_address_id)


# ---------------------------- #
#         DHCPServer
# ---------------------------- #

class DHCPServerView(ObjectView):
    queryset = DHCPServer.objects.all()

    def get_extra_context(self, request, instance):
        table = DHCPReservationTable(instance.dhcpreservation_set.all())
        table.configure(request)

        return {
            'dhcpreservation_table': table,
        }

    def get_absolute_url(self):
        return reverse('plugins:netbox_dhcp:dhcpserver', args=[self.pk])

class DHCPServerListView(ObjectListView):
    queryset = DHCPServer.objects.all()
    table = DHCPServerTable

class DHCPServerEditView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPServer.objects.all()
    form = DHCPServerEditForm

    # @property
    # def model_form(self):
    #     return self.form

class DHCPServerDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPServer.objects.all()


# ---------------------------- #
#       Synchronization
# ---------------------------- #

class SynchronizeDHCP(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'

    def post(self, request, prefix_id):
        prefix = get_object_or_404(Prefix, pk=prefix_id)
        all_ips = prefix.get_child_ips()
        for ip_address in all_ips:
            if hasattr(ip_address, 'macaddress'):
                create_or_update_reservation.delay(
                    ip_address=ip_address
                )
        dhcp_server = DHCPServer.objects.get(id=prefix.custom_field_data['netbox_dhcp_dhcp_server'])
        ssl_verify = False
        response_all_reservations = get(f'{dhcp_server.api_url}/api/reservation/',
                                        headers={'Authorization': f"Token {dhcp_server.api_token}"},
                                        verify=ssl_verify)
        if response_all_reservations.ok:
            data_all_reservations = response_all_reservations.json()
            all_reservations_ids = [ reservation['netbox_id'] for reservation in data_all_reservations ]
            reservations_ids_to_delete = [ id for id in all_reservations_ids if id not in all_ips.values_list(flat=True) ]
            delete_reservation_in_dhcp.delay(
                ids_to_delete=reservations_ids_to_delete,
                dhcp_server=dhcp_server
            )
        return redirect('ipam:prefix', pk=prefix_id)