from django.urls import path
from .views import UserHistoryAPIView, LeaderboardAPIView

urlpatterns = [
    path('history/', UserHistoryAPIView.as_view(), name='user-history'),
    path('leaderboard/<str:level>/', LeaderboardAPIView.as_view(), name='leaderboard'),
]
