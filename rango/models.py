from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify, title
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "subcategories"

    def __str__(self):
        return self.name


class Page(models.Model):
    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    slug=models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        




class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.username
        

class Review (models.Model):
    BriefDescription_Max_Length = 128
    ReviewText_Max_Length = 300
    Stars = models.IntegerField(range(1,5),null=False)
    BriefDescription = models.TextField(max_length=BriefDescription_Max_Length,null=False)
    ReviewText= models.TextField(max_length=ReviewText_Max_Length)
    Page = models.ForeignKey(Page, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "review of page: " + self.Page + " by User: " + self.UserProfile 

class LikedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

