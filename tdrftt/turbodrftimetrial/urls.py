from django.urls import path, include
from turbodrf.router import TurboDRFRouter

router = TurboDRFRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
