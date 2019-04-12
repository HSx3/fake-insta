from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/edit/', views.update, name='update'),
    # path('<int:post_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
]