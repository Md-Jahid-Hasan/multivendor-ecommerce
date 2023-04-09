from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("User must have a email")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLE = [
        ("C", "CUSTOMER"), ("O", "SHOP_OWNER")
    ]
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=USER_ROLE, default="C")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email) + " - " + str(self.role)


class UserAddress(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_address")
    address_details = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=25)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user_id


class UserPaymentDetails(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_payment")
    payment_type = models.CharField(max_length=50)
    provider = models.CharField(max_length=30)
    expiry_date = models.DateTimeField()
    account_no = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id


def get_upload_path(instance, filename):
    return f"{filename}"


class FileSerializer(models.Model):
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user_id
