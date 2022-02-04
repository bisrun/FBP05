from django.urls import path
from redis_geo import views


app_name = 'redis_geo'
urlpatterns = [
    path('', views.index, name='index'),      # /redis_geo/
    path('<int:question_id>/', views.detail, name='detail'),       # /redis_geo/5/
    path('<int:question_id>/results/', views.results, name='results'),     # /redis_geo/5/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),      # /redis_geo/5/vote/
]
