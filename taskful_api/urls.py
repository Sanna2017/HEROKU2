"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from users import router as users_api_router #see router.py file 
from house import router as house_api_router
from task import router as task_api_router

#auth_api_urls = [
    #path('', include('rest_framework_social_oauth2.urls')),
#]
#if settings.DEBUG: #if true #########################################################################
	#auth_api_urls.append(path('verify/', include('rest_framework.urls'))) ##########################################


api_url_patterns = [
    path('accounts/', include(users_api_router.router.urls)),
    #path('auth/', include(auth_api_urls)),
    path('house/', include(house_api_router.router.urls)),
    path('task/', include(task_api_router.router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns)),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
####################  MY WAY ##############################################
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_house/', include('house.urls')),
    path('api_accounts/', include('users.urls')),
    path('api_task/', include('task.urls')),
]


