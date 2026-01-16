from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from events.models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created and instance.user.email:
        send_mail(
            subject=f"RSVP Confirmation for {instance.event.name}",
            message=f"Hi {instance.user.username}, You have RSVP'd for {instance.event.name}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.user.email]
        )