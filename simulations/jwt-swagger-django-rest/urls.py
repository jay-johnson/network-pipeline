from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import permissions
from project_name.api_user import UserViewSet


schema_view = get_swagger_view(title="DRF Swagger with JWT")


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('swagger/', schema_view),
    path('', include(router.urls)),
    path('accounts/', include('rest_registration.api.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
