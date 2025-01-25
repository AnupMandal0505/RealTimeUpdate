from django.db import models

# Create your models here.

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.name} - {self.status}"

    class Meta:
        ordering = ['-created_at']
