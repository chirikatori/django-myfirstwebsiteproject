from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    title = models.TextField(max_length=1000,blank=True, null=True)
    content = models.TextField(max_length=10000,blank=True, null=True)
    link_img = models.TextField(max_length=10000,blank=True, null=True)
    url = models.TextField(max_length=10000,blank=True, null=True)
    sign = models.CharField()

    class Meta:
        #managed = False
        db_table = 'admin'

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15, blank=True)
    phone = models.CharField('Contact Phone', max_length=10, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Adress', blank=True)

    def __str__(self):
        return self.name

class MyWebUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyWebUser, blank=True)

    def __str__(self):
        return self.name