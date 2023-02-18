from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.PositiveIntegerField()
    email=models.EmailField()
    remarks=models.TextField()
    gender=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    remarks=models.TextField()
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    location=models.TextField()
    password=models.CharField(max_length=10)
    profile_pic=models.ImageField(upload_to="profile_pic")

    def __str__(self) -> str:
        return self.fname+" "+self.lname