from psycopg.types.net import ip_address
from logging import getLogger
from ipam.models import IPAddress, Prefix
from netbox_dhcp.models import DHCPReservation, DHCPServer
from django_rq import job
from requests import post, put, delete

logger = getLogger('netbox_dhcp')

@job
def create_or_update_reservation(dhcpreservation: DHCPReservation):
    ip_address = dhcpreservation.ip_address
    dhcp_server = dhcpreservation.dhcpserver
    reservation_conf = {'netbox_id': ip_address.id,'mac': dhcpreservation.macaddress, 'ip': {str(ip_address)}, 'hostname_fqdn': ip_address.dns_name}
    if dhcpreservation == "active":
        response = put(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                       headers={'Authorization': f"Token {dhcp_server.api_token}"},
                       json=reservation_conf,
                       verify=dhcp_server.ssl_verify)
    else:
        response = post(f'{dhcp_server.api_url}/api/reservation/',
                    headers={'Authorization': f"Token {dhcp_server.api_token}"},
                    json=reservation_conf,
                    verify=dhcp_server.ssl_verify)
    if not response.ok:
        logger.debug(f"response.json: {response}")
    logger.debug(f"data_results: {response}")
    return True

@job
def delete_reservation(dhcpreservation: DHCPReservation):
    ip_prefix = dhcpreservation.ip_address
    dhcp_server = dhcpreservation.dhcpserver
    response = delete(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                      headers={'Authorization': f"Token {dhcp_server.api_token}"},
                      verify=dhcp_server.ssl_verify)
    if not response.ok:
        logger.debug(f"response.json: {response}")
    status_code = response.status_code
    logger.debug(f"data_results: {status_code}")
    return status_code

@job
def delete_reservation_in_dhcp(ids_to_delete: list(), dhcp_server: DHCPServer):
    for id in ids_to_delete:
        response = delete(f'{dhcp_server.api_url}/api/reservation/{id}/',
                          headers={'Authorization': f"Token {dhcp_server.api_token}"},
                          verify=dhcp_server.ssl_verify)