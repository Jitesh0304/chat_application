from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, otp, profile_picture=None, password= None, password2= None):

        if not email:
            raise ValueError("User must have email")
        
        user = self.model(email= self.normalize_email(email),
                          username= username,
                          first_name= first_name,
                          last_name= last_name,
                          profile_picture= profile_picture
                          )     # otp= otp
        
        user.set_password(password)
        user.save(using= self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, otp, password= None):

        user = self.create_user(email,
                                password= password,
                                username= username,
                                first_name= first_name,
                                last_name= last_name,
                                otp= otp,
                                profile_picture=None)
        user.is_admin =True
        user.is_verified = True
        user.save(using= self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(max_length=200, verbose_name="Email", unique=True)
    username = models.CharField(max_length=70, verbose_name="Full Name")
    first_name = models.CharField(max_length=70, verbose_name="First Name")
    last_name = models.CharField(max_length=70, verbose_name="Last Name")
    profile_picture = models.ImageField(upload_to ='uploads/',blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','otp','first_name','last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm, obj= None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin