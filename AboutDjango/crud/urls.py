from rest_framework import routers
from .api import ProjectViewSet

router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet, 'projects')

urlpatterns = router.urls