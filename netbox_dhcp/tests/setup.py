from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from netaddr import IPNetwork
from netbox_dhcp.models import *

class SetupDHCPServerCommon(TestCase):

    def setUp(self):
        self.dhcp_server = DHCPServer.objects.create(
            name='Test Server',
            api_token='testtoken123',
            api_url='https://example.com/api',
            ssl_verify=True
        )

    def test_create_dhcp_server(self):
        dhcp_server = DHCPServer.objects.create(
            name='Test Create',
            api_token='testtoken123',
            api_url='https://testcreate.com/api',
            ssl_verify=False
        )

        self.assertEqual(dhcp_server.name, 'Test Create')
        self.assertEqual(dhcp_server.api_token, 'testtoken123')
        self.assertEqual(dhcp_server.api_url, 'https://testcreate.com/api')
        self.assertFalse(dhcp_server.ssl_verify)

    def test_unique_name(self):
        DHCPServer.objects.create(
            name='Test Name',
            api_token='testtoken123',
            api_url='https://testname.com/api',
            ssl_verify=True
        )

        with self.assertRaises(IntegrityError):
            DHCPServer.objects.create(
                name='Test Name',
                api_token='newtoken123',
                api_url='https://anotherapi.com/api',
                ssl_verify=False
            )

    def test_unique_api_url(self):
        DHCPServer.objects.create(
            name='Test URL',
            api_token='testtoken123',
            api_url='https://testurl.com/api',
            ssl_verify=True
        )

        with self.assertRaises(IntegrityError):

            DHCPServer.objects.create(
                name='Test URL 2',
                api_token='newtoken',
                api_url='https://testurl.com/api',
                ssl_verify=False
            )

    def test_default_ssl_verify(self):
        dhcp_server = DHCPServer.objects.create(
            name='Test SSL Verify',
            api_token='testtoken123',
            api_url='https://testsslverify.com/api'
        )

        self.assertTrue(dhcp_server.ssl_verify)


class SetupDHCPReservationCommon(SetupDHCPServerCommon):

    def setUp(self):
        super().setUp()
        address = IPNetwork(addr="192.168.1.10/24")
        self.ip_address = IPAddress.objects.create(address=address,dns_name="toto.test.com")
        self.dhcp_reservation = DHCPReservation.objects.create(
            ip_address=self.ip_address,
            mac_address="aa:bb:cc:dd:ee:ff",
            dhcp_server=self.dhcp_server,
        )

    def test_create_dhcp_reservation(self):
        reservation = self.dhcp_reservation
        self.assertEqual(reservation.ip_address, self.ip_address)
        self.assertEqual(reservation.mac_address, "aa:bb:cc:dd:ee:ff")
        self.assertEqual(reservation.status, "inactive")
        self.assertEqual(reservation.dhcp_server, self.dhcp_server)

    def test_mac_address_validation_invalid(self):
        invalid_mac_list = [
            "a1:b2:c3:d4:e5",
            "a1-b2-c3-d4-e5-f6",
            "ag:bg:cg:dg:eg:fg"
            ]
        for invalid_mac in invalid_mac_list:
            reservation = DHCPReservation(
                ip_address=self.ip_address,
                mac_address=invalid_mac,
                status="inactive",
                dhcp_server=self.dhcp_server
            )
            with self.assertRaises(ValidationError):
                reservation.full_clean()

    def test_unique_mac_address(self):
        reservation = self.dhcp_reservation
        address2 = IPNetwork(addr="192.168.1.11/24")
        ip_address2 = IPAddress.objects.create(address=address2, dns_name="toto2.test.com")
        reservation2 = DHCPReservation(
            ip_address=ip_address2,
            mac_address=self.dhcp_reservation.mac_address,
            status="inactive",

            dhcp_server=self.dhcp_server
        )

        with self.assertRaises(IntegrityError):
            reservation2.save()

    def test_default_status(self):
        reservation = self.dhcp_reservation
        self.assertEqual(reservation.status, "inactive")

    def test_delete_ip_address_should_delete_reservation(self):
        reservation = self.dhcp_reservation
        self.ip_address.delete()

        with self.assertRaises(DHCPReservation.DoesNotExist):
            DHCPReservation.objects.get(id=reservation.id)

    def test_delete_dhcp_server_should_delete_reservation(self):
        reservation = self.dhcp_reservation
        self.dhcp_server.delete()

        with self.assertRaises(DHCPReservation.DoesNotExist):
            DHCPReservation.objects.get(id=reservation.id)

