from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    
    thumbnail = models.ImageField(upload_to='img/', default = "https://www.google.com/url?sa=i&url=https%3A%2F%2Feverydayicons.jp%2Ficons%2Ftag%2F%25E3%2582%25A2%25E3%2583%2590%25E3%2582%25BF%25E3%2583%25BC%2F&psig=AOvVaw2r0V2i9L_kTnQ_COeNy_EY&ust=1711626088288000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKDbw5mulIUDFQAAAAAdAAAAABAE")

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
