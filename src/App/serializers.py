from rest_framework import serializers
from App import models


class SignUpUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AppUser
        fields = '__all__'
        # exclude = ('picture', )

    def create(self, validated_data):
        user = super(SignUpUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Competition
        fields = '__all__'
        depth = 1


class OneUserCompetitionSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Competition
        exclude = ('subscribers',)


class GpsLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GpsLog
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = "__all__"
