from django.urls import path
from .views import *


urlpatterns = [
    path('', home_page, name="home_url"),
    path('lists/single_list/', view_list, name='view_list_url')
]
