from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from account.views import UserViewSet

urlpatterns = [
	path('users', UserViewSet.as_view({
		'get' : 'list', 
		'post': 'create'
    }), name='user'),
	
]

if settings.DEBUG: 
	urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)