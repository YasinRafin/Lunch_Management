from django.db import models
from django.contrib.auth.models import User
from food.models import Item

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='profilepic.jpg',upload_to='profile_pictures')
    location=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"
    
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name} (Order {self.order.id})"
        

