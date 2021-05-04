from django.db import models
from account.models import User
from main.models import *
from ckeditor.fields import RichTextField
# Create your models here.
from django.core.exceptions import ValidationError


def validate_file_size(value):

    try:
        filesize= value.size
        
        if filesize > 1485760:
            raise ValidationError("Too large File")
        else:
            return value
    except:
        pass

class Gallery_Images(models.Model):
    image = models.FileField(
        upload_to="gallery/%Y/%m/%d/", null=True, blank=True,validators=[validate_file_size])
    def __str__(self):
        return str(self.image.url)    


class Gallery(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = RichTextField(null=True, blank=True)
    date = models.DateField(auto_now=True, null=True)
    enable = models.BooleanField(default=False)
    photo = models.ManyToManyField(
        Gallery_Images, blank=True)

    def __str__(self):
        return str(self.title) + ' | ' + str(self.id)

    @property
    def get_image(self):
        try:
            return self.photo.all()[:4]
        except:
            try:
                return self.photo.all()[:3]
            except:
                try:
                    return self.photo.all()[:2]
                except:
                    return self.photo.all()

    @property
    def get_all(self):
        return self.photo.all()

    @property
    def get_one(self):
        return self.photo.all()[0]


class About_Us(models.Model):
    highlight_line = RichTextField(null=True, blank=True)
    vision = RichTextField(null=True, blank=True)
    mission = RichTextField(null=True, blank=True)
    aim = RichTextField(null=True, blank=True)
    description1 = RichTextField(null=True, blank=True)
    description2 = RichTextField(null=True, blank=True)



class Blog(models.Model):
    title = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    highlight_line = RichTextField()
    photo =  models.FileField(
        upload_to="blogs/", default='background.jpeg',validators=[validate_file_size])
    content = RichTextField()
    enable = models.BooleanField(default=False)


    @property
    def get_one(self):
        return self.photo.url

    @property
    def author(self):
        try:
            return str(self.user.first_name) + ' ' + str(self.user.last_name)  
        except:
            return 'Admin'  

    @property
    def author_profile(self):
       return Documents.objects.get(user = self.user).profile.url


          
class Blog_Comments(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    text = RichTextField()


class Banner(models.Model):
    image = models.FileField(
        upload_to="Banner/",null=True)
    enable =  models.BooleanField(default=True)

    @property
    def status():
        if self.enable:
            return 'Enabled'
        else:
            return 'Disabled'  

    @property 
    def getfirst():
        return Banner.objects.filter(enable=True)[0].image.url

    @property
    def getother():
        return Banner.objects.filter(enable=True)[1:]           


class SubPage(models.Model):
    title = models.CharField(max_length=250,unique=True)
    enable = models.BooleanField(default=False)
    position = models.IntegerField()
    content_heading = RichTextField()
    content = RichTextField()
    date = models.DateTimeField(auto_now=True)
    background_image = models.ImageField(upload_to="pages/",default="background.jpeg",validators=[validate_file_size])


   # main = models.ForeignKey(MainPage,on_delete=models.CASCADE)



class MainPage(models.Model):
    title = models.CharField(max_length=250,unique=True)
    enable = models.BooleanField(default=False)
    position = models.IntegerField()
    content_heading = RichTextField()
    content = RichTextField()
    date = models.DateTimeField(auto_now=True)
    sub = models.ManyToManyField(SubPage,null=True)
    background_image = models.ImageField(upload_to="pages/",default="background.jpeg",validators=[validate_file_size])


    @property
    def get_sub(self):
        return self.sub.all().order_by('position','-date')
