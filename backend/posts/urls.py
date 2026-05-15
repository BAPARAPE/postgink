from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostScheduleView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/schedule/', PostScheduleView.as_view(), name='post-schedule'),
]