from django.db import models
import datetime
# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class Users(AbstractUser):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=False)
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.login

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = True
        db_table = 'users'



class FactorialRequest(models.Model):
    number = models.IntegerField()
    result = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number}! = {self.result}"



class Calculation(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    a = models.IntegerField(default=0)
    b = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calculation {self.id} -  number: {self.number}, a: {self.a}, b: {self.b}, Result: {self.result}, Timestamp: {self.timestamp}"




class History(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    calculation_id = models.ForeignKey(Calculation, on_delete=models.CASCADE)
    add_date = models.DateField(default=datetime.date.today, null=True)



    class Meta:
        managed = True
        db_table = 'history'