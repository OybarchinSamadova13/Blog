from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home_view, post_details, post_update, post_delete, post_create, post_author, about

urlpatterns = [
    path('', home_view, name='home_view'),
    path('about/', about, name='about'),
    path('post/<int:pk>/', post_details, name='post_details'),
    path('post_author/<int:pk>/', post_author, name='post_author'),
    path('post/<int:pk>/update', post_update, name='post_update'),
    path('post/<int:pk>/delete', post_delete, name='post_delete'),
    path('post/create', post_create, name='post_create'),

]
