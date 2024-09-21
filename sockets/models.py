from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f'{self.sender} in {self.room} at {self.timestamp.strftime("%H:%M")}'