from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'candidates',CandidateViewSet,basename='candidate')
router.register(r'voters',VoterViewset,basename='voter')
router.register(r'elections',ElectionViewSet,basename='elections')
router.register(r'signup',UserSignupViewSet,basename='signup')

urlpatterns = [
    path('',include(router.urls))
]