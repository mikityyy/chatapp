from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    
    thumbnail = models.ImageField(upload_to='img/', null=True, blank=True)
    class Meta:
        verbose_name_plural='CustomUser'
        
    def __str__(self):
        return  self.username 


class Message(models.Model):
    to_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reciever', null=True, blank=True)
    from_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default = timezone.now)
    
    class Meta:
        ordering=('created_at',)


    def __str__(self):
        return '<Message:id=' + str(self.id) + ', To: ' + str(self.to_name) + ', From: ' + str(self.from_name) + '>'
