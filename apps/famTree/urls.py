from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tree, name='tree'),
    path('tree/save/', views.tree_save, name='tree_save'),
    path('tree/data/', views.tree_data, name='tree_data'),

]
