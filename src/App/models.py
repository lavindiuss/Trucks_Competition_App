from django.db import models
from unique_upload import unique_upload
from django.contrib.auth.models import User

##


def file_upload(instance, filename):  # zaki's unique upload function
    return unique_upload(instance, filename)
##


class AppUser(User):
    picture = models.ImageField(upload_to=file_upload, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Competition(models.Model):

    title = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    logo = models.ImageField(upload_to=file_upload)
    cover = models.ImageField(upload_to=file_upload)
    subscribers = models.ManyToManyField(
        'AppUser', related_name='subscribers', blank=True, null=True)

    reward_points = models.IntegerField(default=0)
    distance_max_limit = models.IntegerField(default=0)
    distance_minimum_limit = models.IntegerField(default=0)

    max_limit = models.IntegerField(default=0)
    speed_limit = models.IntegerField(default=0)
    road = models.CharField(max_length=300)
    end_point = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class GpsLog(models.Model):
    lat = models.CharField(max_length=250)
    lng = models.CharField(max_length=250)
    road = models.CharField(max_length=500)
    current_speed = models.IntegerField(default=0)
    accuracy = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=250, blank=True, null=True)
    acceleration = models.CharField(max_length=250, blank=True, null=True)
    competition = models.ForeignKey('Competition', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        'AppUser', on_delete=models.DO_NOTHING, related_name='user')
    trip = models.ForeignKey(
        'Trip', related_name='trip', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Trip(models.Model):
    road = models.TextField()
    direction = models.CharField(max_length=250)
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)
    end = models.BooleanField(default=False)
    total_distance = models.IntegerField(default=0)

    def __str__(self):
        return self.road
