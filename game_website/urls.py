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
from .views import CustomLoginView, join_or_create_room

# mysite/urls.py
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
 
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('admin/', admin.site.urls, name="admin"),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('', views.homepage, name='home'),
    path('home', views.homepage, name='home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    # joining, creating, routing to room
    path('<game>/map_task/', views.mapTask, name="map_task"),
    path('<game>/all_rooms/', views.all_rooms, name="all_rooms"),
    path('<game>/all_rooms/actionUrl', views.create_room),
    path('<game>/all_rooms/game_view/<room_name>/', views.game_view, name='game_view'),
    path('<game>/all_rooms/game_view/<room_name>/seeMaps', views.seeMaps, name='see_maps'),
    path('completedGame/', views.compareMaps, name='compare_maps'),
    # simple page routing
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('researcher_registration/', views.researcher_registration, name='researcher_registration'),
    path('researcher_login/', CustomLoginView.as_view(
    template_name="researcher_login.html",
    authentication_form=AuthenticationForm), name="researcher_login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='researcher_login'),name='logout'),
    path('data/', views.data, name='research_data'),
    path('conditions/', views.conditions, name='game_conditions'),
    # for creating experiment and conditions from forms in conditions.html
    path('conditions/createExperiment', views.createExperiment),
    path('conditions/createCondition', views.createCondition),
    # ajax views
    path('post/ajax/gameDone', views.gameComplete, name = "complete_game"),
    path('post/ajax/viewConditions', views.viewConditions, name="view_conditions"),
    path('post/ajax/viewGames', views.viewGames, name="view_games"),
    path('post/ajax/viewChats', views.viewChats, name="view_chats"),
    path('post/ajax/saveMessage', views.saveMessage, name="save_message"),
    path('post/ajax/accpetTOS', views.acceptTOS, name="acceptTOS"),
    path('post/ajax/initialPlayer', views.initialPlayer, name="initial_player"),
    path('post/ajax/setScreensize', views.setScreensize, name="set_screensize"),
    path('post/ajax/saveMove', views.saveMove, name="save_move"),
    path('post/ajax/downloadJson', views.downloadJson, name="download_json"),
    path('post/ajax/downloadAll', views.downloadAll, name="download_all"),
    path('get/ajax/decrement_users', views.decrementUsers, name="decrement_users"),
    path('get/ajax/toggle_condition', views.toggleCondition, name="toggleCondition"),
    # when they put the unique private room key:
    path('<game>/all_rooms/join_or_create_room', views.join_or_create_room, name='join_or_create_room'),
    path('<game>/all_rooms/join_private_room/', views.join_private_room, name="join_private_room"),
     
    #re_path(r'^all_rooms/game_view/(?P<room_name>)/$', views.game_view, name='game_view')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
