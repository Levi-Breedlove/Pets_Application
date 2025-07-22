from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _

class Breed(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return self.name + " - " + str(self.weight) + " - " + str(self.height)

class VaccinationCard(models.Model):
    rabies = models.DateField(default=datetime.today().strftime('%Y-%m-%d'), null=False, blank=False)
    hepatitis = models.DateField(null=True, blank=True)
    borrelia = models.DateField(null=True, blank=True)
    distemper = models.DateField(null=True, blank=True)

    def __str__(self):
        pet_name = getattr(self, "pet", None)
        return f"{pet_name or 'unlinked card'} – rabies {self.rabies}"

class Gender(models.TextChoices):
        FEMALE = "F", _("Female")
        MALE = "M", _("Male")

class Pet(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.FEMALE)
    birth = models.DateField(default=None, null=True, blank=True)
    owner = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    card = models.OneToOneField(VaccinationCard, on_delete=models.CASCADE, null=True, blank=True)
    breed = models.ManyToManyField(Breed, blank=True)
    picture = models.ImageField(max_length=255, null=True)
    
    def __str__(self):
        return self.name + " - " + self.gender + " - " + str(self.birth.year)

class VetVisit(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    vet = models.CharField(max_length=100)
    date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    notes = models.TextField(null=True, blank=True)
    
    @property
    def is_today(self):
        return self.date == datetime.today().date()
    
    def __str__(self):
        return self.pet.name + " - " + self.vet + " - " + str(self.date) + " - " + self.notes
