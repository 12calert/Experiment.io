"""game_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include #, re_path
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('', views.homepage, name='home'),
    path('home', views.homepage, name='home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('researcher_login/', views.researcher_login, name='researcher_login'),
    path('all_rooms/', views.all_rooms, name="all_rooms"),
    path('all_rooms/actionUrl', views.create_room),
    path('all_rooms/game_view/<room_name>/', views.game_view, name='game_view'),
    path('researcher_registration/', views.researcher_registration, name='researcher_registration'),
    # when they put the unique private room key:
 
    # tried with regex but need help
    #re_path(r'^all_rooms/game_view/(?P<room_name>)/$', views.game_view, name='game_view')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
