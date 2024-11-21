from django.db import models
from django.contrib.auth.hashers import make_password
from cloudinary.models import CloudinaryField


class LoginModel(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if not self.password.startswith('pbkdf2_sha256$'):  # Avoid rehashing
            self.password = make_password(self.password)
        super(LoginModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150)
    occupation = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    pin_code = models.BigIntegerField()
    mobile_number = models.BigIntegerField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    pan_card = models.CharField(unique=True)
    aadhar_card = models.BigIntegerField(unique=True)
    family_details = models.TextField()
    martial_status = models.CharField(max_length=150)
    star = models.CharField(max_length=150)
    raasi = models.CharField(max_length=150)
    kootram = models.CharField(max_length=150)
    last_timestamp = models.DateTimeField(auto_now=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # Optional fields
    kuladeivam = models.TextField(blank=True, null=True)
    photo = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return str(self.user_id)




