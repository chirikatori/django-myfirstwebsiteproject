from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mytable(models.Model):
    id = models.CharField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    link_img = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    sign = models.CharField()

    class Meta:
        #managed = False
        db_table = 'mytable'
    def __str__(self):
        return self.title
    

class History(models.Model):
    hist_id = models.CharField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_history = models.TextField()