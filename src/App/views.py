from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from App import serializers
from App import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from App import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from geopy.exc import GeocoderTimedOut
import json
# geocode api
from geopy.geocoders import Nominatim
Geo = Nominatim(user_agent="Nada")


class UserViews(APIView):
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        request = self.request
        serializer = serializers.SignUpUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            return Response(
                {"status": "created successfully",
                    "token": Token.objects.create(user=user).key
                 },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        usr = self.request.user
        serializer = serializers.SignUpUserSerializer(
            usr, data=self.request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"status": "Updated successfully"},
                status=200
            )
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=200)


class CompetitionsList(viewsets.ViewSet):
    # RETURNS ALL AVAILABLE COMPETITIONS
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        queryset = models.Competition.objects.all()
        serializer = serializers.CompetitionSerializer(queryset, many=True)
        return Response(serializer.data)


class CompetitionView(APIView):
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)
    # SUBSCRIBE USER TO A COMPETITION HERE
    def post(self, request):

        user = self.request.user
        user = models.User.objects.filter(id=user.id)

        competition_id = self.request.data.get('competition_id', '')
        if competition_id == '':
            return Response({'error': 'competition id  is required'}, status=400)

        # if competition dosent exist
        try:
            competition = models.Competition.objects.get(id=competition_id)
        except ObjectDoesNotExist:
            return Response({'error': 'competition not found '}, status=404)
        # if user already subscribed in this competition
        try:
            already_in = competition.subscribers.get(id=user[0].id)
        except Exception as e:
            already_in = False
        # if user[0].id  already_in_ids:
        if already_in:
            return Response({'error': 'You are already subscribed in this competition'}, status=400)

        if competition.subscribers.count() < competition.max_limit:
            competition = competition.subscribers.add(user[0].appuser)
        else:
            return Response({"error": 'this competition completed or have enough subscribers'}, status=400)

        competitions = models.Competition.objects.filter(subscribers__in=user)
        serializer = serializers.OneUserCompetitionSerializer(
            competitions, many=True)

        return Response({'data': serializer.data, 'status': 'success'}, status=200)

    # THIS ENDPOINT RETURN ALL SPECIFIC USER COMPETITIONS
    def get(self, request):

        user = self.request.user
        user = models.User.objects.filter(id=user.id)
        competitions = models.Competition.objects.filter(subscribers__in=user)

        serializer = serializers.OneUserCompetitionSerializer(
            competitions, many=True)

        return Response({"data": serializer.data}, status=200)


# this function takes lat and lng and return street

def GetLoc(LatAndLng):
    try:

        location = Geo.reverse(LatAndLng, timeout=10)
    except GeocoderTimedOut:
        return Response({"error": "connection error try again"}, status=400)

    if location != None:
        return location.address
    else:
        return 'NotFound'


class GpsLogView(APIView):
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user = request.user

        for obj in request.data:

            lat = obj['lat']
            lng = obj['lng']
            LatAndLng = lat+","+lng

            try:
                road = GetLoc(LatAndLng)
            except Exception as e:
                road = 'NotFound'
            # adding user and road name to serializer
            # for obj in request.data:
            obj['user'] = user
            obj['road'] = road

        serializer = serializers.GpsLogSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Log Created Successfully"}, status=201)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class TripView(APIView):

    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    # trip creation
    def post(self, request):

        data = request.data
        # print(data)
        lat = data['lat']
        lng = data['lng']
        LatAndLng = lat+","+lng
        road = 'NotFound'
        # competition
        competition_id = request.data['competition']

        try:
            road = GetLoc(LatAndLng)
        except Exception as e:
            print(e)

        if road == "NotFound":
            return Response({"status": "Sorry we didn't detect your road try again"}, status=400)

        direction = data['direction']
        ##
        data = {'user': request.user, 'road': str(
            road), 'direction': str(direction), "competition": competition_id}

        # return trip if exist
        try:
            trip = models.Trip.objects.filter(road=road, user=request.user, direction=str(
                direction), competition=competition_id)
            if trip[0]:
                return Response({"status": "you already have trip in this competition you can delete it if you want"}, status=400)
        except Exception as e:
            print(e)

        serializer = serializers.TripSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Trip Created Successfully"}, status=201)

        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        usr = request.user
        data = models.Trip.objects.all()
        serializer = serializers.TripSerializer(data, many=True)

        return Response({"data": serializer.data}, status=200)


class DeleteTripView(APIView):

    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def delete(self, request, pk):
        trip = models.Trip.objects.get(id=pk, user=request.user)
        trip.delete()
        return Response({"status": "trip deleted successfully"}, status=200)


class SubmitTripResult(APIView):
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):

        usr = request.user
        comp_trip = request.GET['trip_id']

        try:
            trip = models.Trip.objects.get(user=usr, id=int(comp_trip))
        except ObjectDoesNotExist:
            return Response({"status": "No trip with this id "}, status=400)

        comp_rules = models.Competition.objects.get(id=trip.competition.id)
        all_gps_logs = len(models.GpsLog.objects.filter(
            user=usr, trip=trip, competition=comp_rules))

        good_gps_logs = len(models.GpsLog.objects.filter(
            user=usr,
            trip=trip,
            competition=comp_rules,
            current_speed__lte=int(comp_rules.speed_limit),
            road=comp_rules.road,
        ))

        distance_result = False
        if trip.total_distance <= comp_rules.distance_max_limit and trip.total_distance >= comp_rules.distance_minimum_limit:
            distance_result = True

        gps_logs_result = int((good_gps_logs/all_gps_logs)*100)
        if gps_logs_result >= 60 and distance_result == True:
            usr.appuser.points += int(comp_rules.reward_points)
            usr.appuser.save()

            return Response({"status": "congrats you are a winner and you got " + str(comp_rules.reward_points)+" points"}, status=200)

        else:
            return Response({"status": "You have to develop some of your skills to win the points.. your success percentage was %s" % (str(gps_logs_result)+'%')}, status=400)
