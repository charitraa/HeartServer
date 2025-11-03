from django.urls import include, path
from .views import CreateUserView , LoginView, UserMeView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('me/', UserMeView.as_view(), name='user_me'),
]
