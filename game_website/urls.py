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
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('', views.homepage, name='home'),
    path('home', views.homepage, name='home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    # joining, creating, routing to room
    path('<game>/all_rooms/', views.all_rooms, name="all_rooms"),
    path('<game>/all_rooms/actionUrl', views.create_room),
    path('<game>/all_rooms/joinRoom', views.joinRoom),
    path('<game>/all_rooms/game_view/<room_name>/', views.game_view, name='game_view'),
    # simple page routing
    path('gamelogic/', views.gamelogic, name='gamelogic'),
    path('researcher_registration/', views.researcher_registration, name='researcher_registration'),
    path('researcher_login/', auth_views.LoginView.as_view(template_name="researcher_login.html"), name = "researcher_login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='researcher_login'),name='logout'),
    path('data/', views.data, name='research_data'),
    path('conditions/', views.conditions, name='game_conditions'),
    # for creating experiment and conditions from forms in conditions.html
    path('conditions/createExperiment', views.createExperiment),
    path('conditions/createCondition', views.createCondition),
    path('<game>/all_rooms/game_view/<room_name>/', views.game_view, name='game_view'),
    path('post/ajax/gameDone', views.gameComplete, name = "complete_game"),
    path('post/ajax/viewConditions', views.viewConditions, name="view_conditions"),
    path('post/ajax/viewGames', views.viewGames, name="view_games"),
    path('post/ajax/viewChats', views.viewChats, name="view_chats"),
    path('post/ajax/saveMessage', views.saveMessage, name="save_message"),
    # when they put the unique private room key:
 
    # tried with regex but need help
    #re_path(r'^all_rooms/game_view/(?P<room_name>)/$', views.game_view, name='game_view')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
