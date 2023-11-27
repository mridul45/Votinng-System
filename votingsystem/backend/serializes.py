from .models import *
from rest_framework import serializers


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