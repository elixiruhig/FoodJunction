import uuid
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from django.utils.timezone import now
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase




class UserManager(BaseUserManager):

    def create_user(self,username,name,password=None):
        if not username:
            raise ValueError("Please enter an username")

        user = self.model(
            username = username
        )
        user.set_password(password)
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self,username,name,password):
        user = self.create_user(username,name, password=password)
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=False)
    username = models.CharField(max_length=255, blank=False, unique=True)
    user_id = models.UUIDField(unique=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.BigIntegerField(blank=True,null=True)
    category = models.CharField(max_length=255, default='Customer')
    sector = models.IntegerField(blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_customer(self):
        return self.category.lower() == 'customer'

    @property
    def is_vendor(self):
        return self.category.lower() == 'vendor'

    @property
    def is_delivery_agent(self):
        return self.category.lower() == 'delivery'

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

class Hotel(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False, null=False)
    sector = models.IntegerField()
    photo = models.ImageField(upload_to='hotel_photos',null=True)

    def __str__(self):
        return self.name

class Dish(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    dish_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    veg = models.BooleanField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='dish_photos', null=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='customer')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    status = models.CharField(null=True, max_length=255)
    delivery = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    busy = models.BooleanField(default=False)
    order = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True, related_name='+')