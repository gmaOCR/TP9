from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket

@receiver(pre_save, sender=Ticket)
def delete_image_on_ticket_update(sender, instance, **kwargs):
    if instance.pk:
        old_image = Ticket.objects.get(pk=instance.pk).image
        new_image = instance.image
        if old_image and (
            not new_image
            or old_image.url != new_image.url
        ):
            old_image.delete(save=False)