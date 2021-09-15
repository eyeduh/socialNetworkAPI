from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from users.validators import MinAgeValidator
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    bio = models.TextField(default='', blank=True)
    date_of_birth = models.DateField(validators=[MinAgeValidator])
    avatar = models.ImageField(blank=True, upload_to='media/avatars')
    location = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True, blank=True)

    GENDERS = (
        (1, 'Female'),
        (2, 'Male'),
        (3, 'Rather Not Say')
    )
    gender = models.IntegerField(choices=GENDERS, default=1)
    
    def __str__(self):
        return f'{self.first_name}'