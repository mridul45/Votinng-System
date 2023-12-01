from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:

        model = Candidate
        fields = "__all__"


class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:

        model = Candidate
        fields = "__all__"


class VoterSerializer(serializers.ModelSerializer):
    class Meta:

        model = Voter
        fields = "__all__"


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:

        model = Election
        fields = "__all__"


class UserSignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(max_length=255)


class VotedSerializer(serializers.ModelSerializer):
    class Meta:

        model = Voted
        fields = "__all__"



class ShareSerializer(serializers.ModelSerializer):
    class Meta:

        model = Shares
        fields = "__all__"


class ShareUploadSerializer(serializers.Serializer):
    uploaded_share1_link = serializers.FileField()

    def validate_uploaded_share1_link(self, value):
        return value