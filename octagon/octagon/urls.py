"""
URL configuration for octagon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from backend.views import AIModelViewSet, ProblemViewSet, TypeViewSet, VerifyModel, EvaluateModel, DeployModel
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'aimodels', AIModelViewSet, basename='aimodel')
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'types', TypeViewSet, basename='type')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    # Optional UI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('verify/<int:id>', VerifyModel.as_view(), name='verify-model'),
    path('evaluate/<int:id>', EvaluateModel.as_view(), name='evaluate-model'),
    path('deploy/<int:id>', DeployModel.as_view(), name='deploy-model'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)