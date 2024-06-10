from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.
class Item(models.Model):
    def __str__(self) -> str:
        return self.item_name
    
    user_name=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    item_name=models.CharField(max_length=200)
    item_desc=models.CharField(max_length=200)
    item_price=models.IntegerField()
    item_image=models.CharField(max_length=500,default="https://assets.epicurious.com/photos/568eb0bf7dc604b44b5355ee/16:9/w_2560%2Cc_limit/rice.jpg")
    time_stamp=models.DateTimeField(default=timezone.now)
    def get_absolute_url(self):
        return reverse('food:detail',kwargs={'pk':self.pk})