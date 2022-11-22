from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lookup.urls')),  # this includes the urls file from the lookup directory
]
