from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'candidates',CandidateViewSet,basename='candidate')
router.register(r'voters',VoterViewset,basename='voter')
router.register(r'elections',ElectionViewSet,basename='elections')
router.register(r'signup',UserSignupViewSet,basename='signup')
router.register(r'votes',VotedViewset,basename='voted'),
router.register(r'voted',VotedViewset,basename='voted')
router.register(r'shares',ShareViewset,basename='shares')
router.register(r'verification',ShareUploadViewSet,name="verification")

urlpatterns = [
    path('',include(router.urls))
]