from django.urls import path
from .views import UserHistoryAPIView, LeaderboardAPIView, UserScoreAPIView

urlpatterns = [
    path('history/', UserHistoryAPIView.as_view(), name='user-history'),
    path('score/', UserScoreAPIView.as_view(), name='user-score'),
    path('leaderboard/<str:level>/', LeaderboardAPIView.as_view(), name='leaderboard-level'),
]
