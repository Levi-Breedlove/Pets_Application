from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_pets, name="pets_list"),
    path("", views.list_pets, name="index"), 
    path("pet/<int:pet_id>/", views.pet_detail, name="pet"),
    path("visit/<int:pet_id>/", views.visit, name="visit_today"),
]