from requests import get
from netbox.views.generic import ObjectEditView, ObjectDeleteView,ObjectView
from ipam.models import IPAddress, Prefix
from .forms import MacAddressEditForm
from .models import MacAddress, DHCPReservation, DHCPServer
from .background_tasks import create_or_update_reservation, delete_reservation, delete_reservation_in_dhcp
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin
from logging import getLogger

logger = getLogger('netbox_dhcp')

class MacAddressObjectMixin:
    def get_object(self, *args, **kwargs):
        if 'ip_address_id' not in kwargs:
            raise Http404
        ip_address = get_object_or_404(IPAddress, pk=kwargs['ip_address_id'])
        if 'pk' in kwargs:
            return get_object_or_404(MacAddress, ip_address=ip_address, pk=kwargs['pk'])
        return MacAddress(ip_address=ip_address)

class MacAddressView(ObjectView):
    queryset = MacAddress.objects.all()

class MacAddressCreateView(PermissionRequiredMixin, ObjectEditView, MacAddressObjectMixin):
    permission_required = 'netbox_dhcp.add_macaddress'
    queryset = MacAddress.objects.all()
    form = MacAddressEditForm
    @property
    def model_form(self):
        return self.form

class MacAddressEditView(MacAddressCreateView):
    permission_required = 'netbox_dhcp.change_macaddress'

class MacAddressDeleteView(PermissionRequiredMixin, ObjectDeleteView, MacAddressObjectMixin):
    permission_required = 'netbox_dhcp.delete_macaddress'
    queryset = MacAddress.objects.all()

    def delete(self, request, ip_address_id):
        ip_address = get_object_or_404(IPAddress, pk=ip_address_id)
        if hasattr(ip_address, 'dhcpreservation') and ip_address.dhcpreservation.is_reserved:
            delete_reservation.delay(
                ip_address=ip_address
            )
        return redirect(ip_address.get_absolute_url())

class MacAddressDeleteView(PermissionRequiredMixin, ObjectDeleteView, MacAddressObjectMixin):
    permission_required = 'netbox_dhcp.delete_macaddress'
    queryset = MacAddress.objects.all()

class DHCPReservationRecreateView(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'

    def post(self, request, ip_address_id):
        ip_address = get_object_or_404(IPAddress, pk=ip_address_id)
        try:
            create_or_update_reservation.delay(
                ip_address=ip_address
            )
        except Exception as e:
            logger.exception(e)
        return redirect('ipam:ipaddress', pk=ip_address_id)

class SynchronizeDHCP(PermissionRequiredMixin, View):
    permission_required = 'netbox_dhcp.delete_dhcpserver'

    def post(self, request, prefix_id):
        prefix = get_object_or_404(Prefix, pk=prefix_id)
        all_ips = prefix.get_child_ips()
        for ip_address in all_ips:
            if hasattr(ip_address, 'macaddress'):
                try:
                    create_or_update_reservation.delay(
                        ip_address=ip_address
                    )
                except Exception as e:
                    logger.exception(e)
        dhcp_server = DHCPServer.objects.get(id=prefix.custom_field_data['netbox_dhcp_dhcp_server'])
        ssl_verify = False
        response_all_reservations = get(f'{dhcp_server.api_url}/api/reservation/',
                                        headers={'Authorization': f"Token {dhcp_server.api_token}"},
                                        verify=ssl_verify)
        if response_all_reservations.ok:
            data_all_reservations = response_all_reservations.json()
            all_reservations_ids = [ reservation['sot_id'] for reservation in data_all_reservations ]
            reservations_ids_to_delete = [ id for id in all_reservations_ids if id not in all_ips.values_list(flat=True) ]
            try:
                delete_reservation_in_dhcp.delay(
                    ids_to_delete=reservations_ids_to_delete,
                    dhcp_server=dhcp_server
                )
            except Exception as e:
                logger.exception(e)
        return redirect('ipam:prefix', pk=prefix_id)