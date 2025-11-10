from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
from rest_framework import status

from HeartServer.permission import LoginRequiredPermission
from .models import GameHistory
from .serializers import GameHistorySerializer

User = get_user_model()

class UserHistoryAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        user = request.user
        histories = GameHistory.objects.filter(user=user).order_by('-date_played')
        serializer = GameHistorySerializer(histories, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK)
    
class UserScoreAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        """
        Save a new game result for the logged-in user.
        Expected JSON:
        {
            "level": "easy",
            "score": 120,
            "time_taken": 10
        }
        """
        data = request.data.copy()
        data["user"] = request.user.id  # ensure it’s linked to the logged-in user

        serializer = GameHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response( serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardAPIView(APIView):
    """
    Returns leaderboard optionally filtered by level.
    If no level is passed, return global total score leaderboard.
    """
    permission_classes = [LoginRequiredPermission]

    def get(self, request, level=None):
        if level:
            users = User.objects.annotate(
                total_score=Sum('histories__score', filter=Q(histories__level=level))
            ).order_by('-total_score')
        else:
            users = User.objects.annotate(
                total_score=Sum('histories__score')
            ).order_by('-total_score')

        data = [
            {
                "id": u.id,
                "username": u.username,
                "total_score": u.total_score or 0
            }
            for u in users
        ]
        return Response(data, status=status.HTTP_200_OK)
