from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import DHCPReservation
from .background_tasks import delete_reservation

@receiver(post_delete, sender=DHCPReservation)
def trigger_dhcp_delete(instance: DHCPReservation, **_kwargs):
    ip_address = instance.ip_address
    if hasattr(ip_address, 'dhcpreservation') and ip_address.dhcpreservation.is_reserved:
        delete_reservation.delay(
            ip_address=ip_address
        )