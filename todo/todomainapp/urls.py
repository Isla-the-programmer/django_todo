from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoItemViewSet, UserView, LoginView

router = DefaultRouter()
router.register(r'todos', TodoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name = 'login')
]
