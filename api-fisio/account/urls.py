from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from account.views import UserViewSet, UserMeRetrieveAPIView

urlpatterns = [
	path('accounts/me', UserMeRetrieveAPIView.as_view()),
	path('accounts', UserViewSet.as_view({
		'get' : 'list', 
		'post': 'create'
    })),
	
	
]

if settings.DEBUG: 
	urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)