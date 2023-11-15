from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback, name="feedback"),
    path('<int:article_id>/', views.reply, name='reply'),
	path('<int:article_id>/delete', views.delete, name='delete'),
    path('<int:article_id>/update', views.update, name='update'),
    path('<int:article_id>/like', views.like, name='like'),
    path('api/articles/<int:article_id>/like', views.api_like),
    #path("<str:room_name>/", views.room, name="room"),
]