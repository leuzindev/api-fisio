from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from professional.views import ProfessionalViewSet

urlpatterns = [
	path('professional/', ProfessionalViewSet.as_view({'get': 'list'}), name='professional'),
	
]

if settings.DEBUG: 
	urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)