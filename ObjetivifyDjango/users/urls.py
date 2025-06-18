from rest_framework import routers
from .viewsets import UserViewSet, GroupViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = router.urls