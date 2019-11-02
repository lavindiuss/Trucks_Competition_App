from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.response import Response

router = DefaultRouter()

router.register('CompetitionsList', views.CompetitionsList,
                base_name='CompetitionsList')

urlpatterns = [
    path('UserView/', views.UserViews.as_view(), name='user-view'),
    path('UserLogIn/', views.LogInView.as_view(), name='user-view'),
    path('CompetitionView/', views.CompetitionView.as_view(), name='user-view'),
    path('TripView/', views.TripView.as_view(), name='TripView'),
    path('DeleteTripView/<int:pk>/',
         views.DeleteTripView.as_view(), name='DeleteTripView'),
    path('GpsLogView/', views.GpsLogView.as_view(), name='GpsLogView'),
    path('SubmitTripResult/', views.SubmitTripResult.as_view(),
         name='SubmitTripResult'),

    path('', include(router.urls)),

]
