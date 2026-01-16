from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="events")
    image = models.ImageField(
        upload_to='events',
        default='events/default_image.jpg',
        blank=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='events',through='RSVP',
        blank=True
    )

    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name=models.CharField(max_length=150)
#     email=models.EmailField(unique=True)
#     event=models.ManyToManyField(Event,related_name="Participants", blank=True)

#     def __str__(self):
#         return self.name

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')  
    

