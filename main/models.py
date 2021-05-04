from django.db import models
from account.models import User
# Create your models here.

sex = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)


class Personal_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=15, choices=sex, null=False, default='None')
    profession = models.CharField(max_length=150)
    birth_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    tag_line = models.CharField(max_length=400,null=True,blank=True)
    facebook = models.URLField(blank=True, null=True)
    insta = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + ' | ' + 'personal_info'


class Documents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    id_front = models.FileField(
        upload_to="id_images/", null=True, blank=True)
    id_back = models.FileField(
        upload_to="id_images/", null=True, blank=True)
    profile = models.FileField(
        upload_to="profile_images/",  default='default.jpg', null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' | ' + 'documents'


class Skills(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    area = models.CharField(max_length=130, null=True)
    experience = models.IntegerField(default=0, null=True)
    hard_skills = models.CharField(max_length=130, null=True)
    soft_skills = models.CharField(max_length=130, null=True)
    interests = models.CharField(max_length=130, null=True)

    def __str__(self):
        return str(self.user) + ' | ' + 'skills'


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    notify = models.TextField()
    read = models.BooleanField(default=False)
