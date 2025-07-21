from django.shortcuts import render
from .models import Pet, VetVisit
from datetime import datetime

def listPets(request):
    context = {'pets': Pet.objects.all()}
    return render(request, "pets_app/pets.html", context)

def pet(request, pet_id):
    context = {'pet': Pet.objects.filter(id=pet_id).first()}
    return render(request, "pets_app/pet.html", context)
    
def visit(request, pet_id):
    pet = Pet.objects.filter(id=pet_id).first()
    lastvisit = pet.vetvisit_set.last()

    # set vet from last visit or default to unknow
    vet = "unknown"
    if lastvisit:
        vet = pet.vetvisit_set.last().vet

    # add a rabies visit today, unless there was visit today already
    if lastvisit is None or (lastvisit and not lastvisit.is_today):
        newvisit = VetVisit(pet=pet, vet=vet, notes="rabies vaccination")
        newvisit.save()
        pet.card.rabies = datetime.today().strftime('%Y-%m-%d')
        pet.card.save()
    context = {'pet': pet}
    return render(request, "pets_app/pet.html", context)
