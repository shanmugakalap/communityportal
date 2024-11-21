from django.urls import path
from .views import LoginCreateView, LoginView, BulkCreate, UserCreateView, UserDetailsView

urlpatterns = [
    path('logincreate/', LoginCreateView.as_view(), name ='login-create'),
    path('login/', LoginView.as_view(), name ='login-user'),
    path('UserCreateView/', UserCreateView.as_view(), name ='user-create'),
    path('user/<int:user_id>/', UserDetailsView.as_view(), name='user-detail'),
]