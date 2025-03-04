from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant_images')
    location = models.CharField(max_length=100)
    rating = models.FloatField()

    def __str__(self):
        return self.name
    
class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(MainCategory, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(SubCategory, related_name='food_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')
    rating = models.FloatField(default=0.0)  

    def __str__(self):
        return self.name
    

class UserSignup(models.Model):
    Username = models.CharField(max_length=100,default='')
    FirstName = models.CharField(max_length=100,default='')
    LastName = models.CharField(max_length=100,default='')
    Email = models.EmailField(max_length=254,default='')
    Password = models.CharField(max_length=100,default='')
    phone=models.IntegerField(default='')
    dob=models.DateField(default='')
    gender=models.CharField(max_length=10,choices=[('male','Male'),('female','Female'),('others','Other')],default='')
    
    def __str__(self):
        return f"{self.Username}"   
    
    
class Address(models.Model):
    genderChoice=(
        ('Male','Male'),
        ('Female','Female'),
        ('others','others'),
    )
    user = models.ForeignKey(UserSignup, null=True, blank=True, on_delete=models.CASCADE) 
    Name = models.CharField(max_length=100,default='')
    Email = models.EmailField(max_length=254,default='')
    phone=models.IntegerField(default='')
    city=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200,blank=True)
    pincode=models.IntegerField(blank=True,null=True)
    gender=models.CharField(max_length=10)
    address=models.TextField()
    def __str__(self):
        return f'{self.Name} {self.phone}'
    
class Cart(models.Model):
    product = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    custom_user = models.ForeignKey(UserSignup, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.customer:
            return f"{self.customer.username} - {self.product.name}"
        elif self.custom_user:
            return f"{self.custom_user.Username} - {self.product.name}"
        return f"Unknown User - {self.product.name}"

class LikedItem(models.Model):
    product = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    custom_user = models.ForeignKey(UserSignup, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.customer:
            return f"{self.customer.username} - {self.product.name}"
        elif self.custom_user:
            return f"{self.custom_user.Username} - {self.product.name}"
        return f"Unknown User - {self.product.name}"
    
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Order placed', 'Order placed'),
        ('Order cancelled', 'Order cancelled'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    
    customer = models.ForeignKey(UserSignup, on_delete=models.CASCADE)
    orderId = models.CharField(max_length=200, unique=True)
    totalPrice = models.FloatField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)
    items = models.ManyToManyField(FoodItem)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.orderId} by {self.customer.Username}"