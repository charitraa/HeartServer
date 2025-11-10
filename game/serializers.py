from rest_framework import serializers
from .models import GameHistory
from django.contrib.auth import get_user_model

User = get_user_model()

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = ['id', 'level', 'score', 'time_taken', 'date_played']

class LeaderboardSerializer(serializers.ModelSerializer):
    total_score = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['id', 'username', 'total_score']
