from django.urls import path, include
from rest_framework_nested import routers

from users.views import (
    UserViewSet, UserProfileView
)

router = routers.SimpleRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/profile/',
         UserProfileView.as_view(), name='user-profile'),
]