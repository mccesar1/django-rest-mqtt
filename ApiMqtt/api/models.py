from django.db import models

# Create your models here.


class MQTTMessage(models.Model):
    topic = models.CharField(max_length=100)
    payload = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje en {self.topic} a las {self.timestamp}"
