# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Sum, Q

from HeartServer.permission import LoginRequiredPermission
from .models import GameHistory
from .serializers import GameHistorySerializer

class UserHistoryAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        user = request.user
        histories = GameHistory.objects.filter(user=user).order_by('-date_played')
        serializer = GameHistorySerializer(histories, many=True)
        return Response(serializer.data)


class LeaderboardAPIView(APIView):
    """
    Returns leaderboard optionally filtered by level.
    If no level is passed, return global total score leaderboard.
    """
    permission_classes = [LoginRequiredPermission]

    def get(self, request, level=None):
        if level:
            users = User.objects.annotate(
                total_score=Sum('gamehistory__score', filter=Q(gamehistory__level=level))
            ).order_by('-total_score')
        else:
            users = User.objects.annotate(
                total_score=Sum('gamehistory__score')
            ).order_by('-total_score')

        data = [
            {
                "id": u.id,
                "username": u.username,
                "total_score": u.total_score or 0
            }
            for u in users
        ]
        return Response(data)
