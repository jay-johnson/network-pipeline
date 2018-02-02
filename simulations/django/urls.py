from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from project_name import views
import registration


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.index, name="emptyindex"),
    path('index/', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('accounts/',
         include('registration.backends.simple.urls')),
    path('accounts/profile/', views.profile, name="profile"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
