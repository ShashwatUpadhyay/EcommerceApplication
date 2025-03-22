from django.db import models
from base.base_model import BaseModel
from django.contrib.auth.models import User
# Create your models here.
class UserExtra(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra')
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username
  
    @property
    def full_name(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username

    
    @property
    def email(self):
        return self.user.email

class Address(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='address')
    country = models.CharField(max_length=20, null=True,blank=True)
    state = models.CharField(max_length=30, null=True,blank=True)
    city = models.CharField(max_length=50, null=True,blank=True)
    area = models.CharField(max_length=50, null=True,blank=True)
    landmark = models.CharField(max_length=50, null=True,blank=True)
    pin_code = models.CharField(max_length=20, null=True,blank=True)