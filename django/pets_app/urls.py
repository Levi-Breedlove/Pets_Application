from django.urls import path
from pets_app import views

urlpatterns = [
    path("", views.listPets, name="petsList"),
    path("index/", views.listPets, name="index"),
    path("pet/<str:pet_id>", views.pet, name="pet"),
    path("visit/<str:pet_id>", views.visit, name="visit"),
]
