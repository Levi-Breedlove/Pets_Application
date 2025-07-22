from datetime import date
from django.shortcuts import get_object_or_404, render
from .models import Pet, VetVisit, VaccinationCard


def list_pets(request):
    return render(request, "pets_app/pets.html", {"pets": Pet.objects.all()})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    return render(request, "pets_app/pet.html", {"pet": pet})


def visit(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)

    # ensure card exists
    card, _ = VaccinationCard.objects.get_or_create(pet=pet)

    # create visit if none today
    last_visit = pet.vetvisit_set.last()
    if last_visit is None or not last_visit.is_today:
        vet_name = last_visit.vet if last_visit else "Unknown"
        VetVisit.objects.create(pet=pet, vet=vet_name, notes="rabies vaccination")

        if card.rabies is None:
            card.rabies = date.today()
            card.save(update_fields=["rabies"])

    return render(request, "pets_app/pet.html", {"pet": pet})
