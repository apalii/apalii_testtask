from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class CardUserManager(BaseUserManager):
    def create_user(self, number, password=None):
        if not number:
            raise ValueError('Card must have a number')
        user = self.model(number=number)
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, number, password):
        user = self.create_user(number, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Card(AbstractBaseUser, PermissionsMixin):
    number = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    objects = CardUserManager()
    
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = []  
    
    class Meta():
        db_table = 'cards'  

    def get_full_name(self):
        # The user is identified by their email address
        return self.number

    def get_short_name(self):
        # The user is identified by their email address
        return self.number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view the app `app_label`?
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def __unicode__(self):
        return "{} | balance: {} | active: {}".format(self.number, self.balance, self.is_active)   
    
    
class Operations(models.Model):
    prev_balance = models.IntegerField()
    cur_balance = models.IntegerField()
    diff = models.IntegerField()
    operation_code = models.IntegerField(default=10000000000)
    timestamp = models.DateTimeField(auto_now_add=True)
    operation_card = models.ForeignKey(Card)
    
    class Meta():
        db_table = 'operations'
        ordering = ['timestamp']
        
    def __unicode__(self):
        return "{} : {}/{}".format(
            self.operation_code, self.timestamp, self.diff) 