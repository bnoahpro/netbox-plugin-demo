from psycopg.types.net import ip_address
from logging import getLogger
from ipam.models import IPAddress, Prefix
from .models import DHCPReservation, DHCPServer
from django_rq import job
from requests import post, put, delete

logger = getLogger('netbox_dhcp')

def get_dhcp(prefix: Prefix):
    if prefix.custom_field_data.get("netbox_dhcp_dhcp_server"):
        return DHCPServer.objects.get(id=prefix.custom_field_data.get("netbox_dhcp_dhcp_server"))
    if prefix.get_parents().count() > 0:
        return get_dhcp(prefix.get_parents().last())
    return None

@job
def create_or_update_reservation(ip_address: IPAddress):
    if hasattr(ip_address, 'dhcpreservation'):
        dhcpreservation = ip_address.dhcpreservation
    else:
        dhcpreservation = DHCPReservation(ip_address=ip_address, mac_address=ip_address.macaddress)
        dhcpreservation.save()
    ip_prefix = Prefix.objects.get(prefix=str(ip_address.address.cidr))
    dhcp_server = get_dhcp(ip_prefix)
    ssl_verify = False #To variabilize
    reservation_conf = {'sot_id': ip_address.id,'mac': f'{str(ip_address.macaddress)}', 'ip': f'{str(ip_address)}', 'hostname_fqdn': ip_address.dns_name}
    if dhcpreservation.is_reserved:
        response = put(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                       headers={'Authorization': f"Token {dhcp_server.api_token}"},
                       json=reservation_conf,
                       verify=ssl_verify)
    else:
        response = post(f'{dhcp_server.api_url}/api/reservation/',
                    headers={'Authorization': f"Token {dhcp_server.api_token}"},
                    json=reservation_conf,
                    verify=ssl_verify)
    if not response.ok:
        logger.debug(f"response.json: {response}")
    logger.debug(f"data_results: {response}")
    dhcpreservation.is_reserved = True
    dhcpreservation.save()
    return True

@job
def delete_reservation(ip_address: IPAddress):
    ip_prefix = Prefix.objects.get(prefix=str(ip_address.address.cidr))
    dhcp_server = get_dhcp(ip_prefix)
    ssl_verify = False #To variabilize
    response = delete(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                      headers={'Authorization': f"Token {dhcp_server.api_token}"},
                      verify=ssl_verify)
    if not response.ok:
        logger.debug(f"response.json: {response}")
    status_code = response.status_code
    logger.debug(f"data_results: {status_code}")
    return status_code

@job
def delete_reservation_in_dhcp(ids_to_delete: list(), dhcp_server: DHCPServer):
    ssl_verify = False
    for id in ids_to_delete:
        response = delete(f'{dhcp_server.api_url}/api/reservation/{id}/',
                          headers={'Authorization': f"Token {dhcp_server.api_token}"},
                          verify=ssl_verify)