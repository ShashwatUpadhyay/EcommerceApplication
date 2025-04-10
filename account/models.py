from django.db import models
from base.base_model import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.
class UserExtra(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra')
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)
    forgot_password_token_created_at = models.DateTimeField(null=True, blank=True)
    change_password_token = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    

    @property
    def full_name(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username

    def __str__(self):
        return self.full_name.upper()
    
    @property
    def email(self):
        return self.user.email

class Address(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True,blank=True)
    email = models.CharField(max_length=50, null=True,blank=True)
    phone = models.CharField(max_length=50, null=True,blank=True)
    country = models.CharField(max_length=50, null=True,blank=True)
    state = models.CharField(max_length=30, null=True,blank=True)
    city = models.CharField(max_length=50, null=True,blank=True)
    address = models.CharField(max_length=50, null=True,blank=True)
    pin_code = models.CharField(max_length=20, null=True,blank=True)
    selected = models.BooleanField(default=True)
    
@receiver(post_save , sender = User)
def createUserExtra(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            user_extra, created = UserExtra.objects.get_or_create(user=instance)