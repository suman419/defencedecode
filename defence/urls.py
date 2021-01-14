
from django.urls import path, include
from defence import views

urlpatterns = [
    path('', views.post_list,name='post_list'),
    path('latest', views.latest_news,name='latest'),
    path('asia', views.asian_country_post,name='asian_country_post'),
    path('europe', views.europe_country_post,name='europe_country_post'),
    path('aboutus', views.about_us,name='aboutus'),
    path('contact_us', views.contact_us,name='contact_us'),
    path('contact', views.contact_form,name='contact'),
    path('broadcast', views.broadcast_video,name='broadcast'),
    path('post_detail/<int:pk>',  views.post_detail,name='post_detail'),
    path('like', views.like_post,name='like_post'),
    
]

app_name = 'defence'