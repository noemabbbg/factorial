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
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null= True)
    function = models.IntegerField(default=0)
    par_1 = models.IntegerField(default=0)
    par_2 = models.IntegerField(default=0)
    result = models.IntegerField(default=0) 
    status = models.CharField(max_length=100)
    calc_date = models.DateTimeField(auto_now_add=True)
    exec_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Calculation {self.id} -  number: {self.number}, par_1: {self.par_1}, par_2: {self.par_2}, Result: {self.result}, calc_date: {self.calc_date}"
    


class History(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, default=1, on_delete=models.CASCADE)
    add_date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)  # default value is set here
    calculation_result = models.IntegerField(default=0)  # default value is set here

    def __str__(self):
        return f"History {self.id} - User ID: {self.user.id}, Calculation ID: {self.calculation.id}, Calculation Result: {self.calculation_result}"




