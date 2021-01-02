from django.urls import path
from .views import *


urlpatterns = [
    path('', home_page, name="home_url"),
    path('new', new_list, name='new_list_url'),
    path('<int:list_id>/', view_list, name='view_list'),
    path('<int:list_id>/add_item', add_item, name='add_item'),
]
