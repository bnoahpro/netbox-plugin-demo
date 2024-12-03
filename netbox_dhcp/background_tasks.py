from logging import getLogger
from ipam.models import IPAddress
from netbox_dhcp.models import DHCPReservation, DHCPServer
from django_rq import job
from requests import post, put, delete

logger = getLogger('netbox_dhcp')


@job
def create_or_update_reservation(dhcp_reservation: DHCPReservation):
    ip_address = dhcp_reservation.ip_address
    dhcp_server = dhcp_reservation.dhcp_server
    reservation_conf = {'netbox_id': ip_address.id, 'mac': dhcp_reservation.mac_address, 'ip': str(ip_address),
                        'hostname_fqdn': ip_address.dns_name}
    if dhcp_reservation == "active":
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
def delete_reservation(dhcp_reservation: DHCPReservation):
    ip_address = dhcp_reservation.ip_address
    dhcp_server = dhcp_reservation.dhcp_server
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
    """
    Function that delete all reservations in DHCP server if their netbox_id is not in Netbox

    ids_to_delete: list of reservations to delete in DHCP server
    dhcp_server: DHCPServer object to target
    """
    for id in ids_to_delete:
        response = delete(f'{dhcp_server.api_url}/api/reservation/{id}/',
                          headers={'Authorization': f"Token {dhcp_server.api_token}"},
                          verify=dhcp_server.ssl_verify)
