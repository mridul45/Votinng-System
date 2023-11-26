from .models import *
from rest_framework import serializers


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:

        model = Candidate
        fields = ["id","candidate_id","party_affiliated","election_type","bio","photo","campaign_slogan"]


class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:

        model = Candidate
        fields = "__all__"


class VoterSerializer(serializers.ModelSerializer):
    class Meta:

        model = Voter
        fields = "__all__"