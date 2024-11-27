from django.db.models.signals import post_init, post_save, post_delete
from django.dispatch import receiver
from netbox_dhcp.models import DHCPReservation
from netbox_dhcp.background_tasks import create_or_update_reservation, delete_reservation

@receiver(post_save, sender=DHCPReservation)
def trigger_create_or_update_reservation(instance: DHCPReservation, **_kwargs):
    ip_address = instance.ip_address
    create_or_update_reservation.delay(
        ip_address=ip_address
    )

@receiver(post_delete, sender=DHCPReservation)
def trigger_delete_reservation(instance: DHCPReservation, **_kwargs):
    ip_address = instance.ip_address
    if ip_address.dhcpreservation.status == 'active':
        delete_reservation.delay(
            ip_address=ip_address
        )
