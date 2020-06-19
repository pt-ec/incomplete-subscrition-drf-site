import re

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """ Creates and saves a new user """
        email = self.normalize_email(email)
        first_name = first_name.strip().title()
        last_name = last_name.strip().title()

        txt = f'{first_name} {last_name}'
        if re.search('[^a-zA-Z\s.]', txt):
            raise ValueError(
                'First and last name can only comprised of letters')

        user = self.model(email=email, first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """ Creates and saves a new staff user """
        user = self.create_user(email, first_name,
                                last_name, password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """ Creates and saves a new superuser """
        user = self.create_user(email, first_name,
                                last_name, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    def get_full_name(self):
        """ Retrive user's full name """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """ Retrive user's first_name """
        return self.first_name

    def __str__(self):
        return self.email
