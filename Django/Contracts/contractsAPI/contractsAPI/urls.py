from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView,  SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contractsApp.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
