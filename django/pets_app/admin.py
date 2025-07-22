# pets_app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Breed, VaccinationCard, Pet, VetVisit


# ────────────────────────────────
# Simple models
# ────────────────────────────────
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display  = ("name", "weight", "height")
    search_fields = ("name",)
    ordering      = ("name",)


@admin.register(VaccinationCard)
class VaccinationCardAdmin(admin.ModelAdmin):
    list_display  = ("id", "rabies", "hepatitis", "borrelia", "distemper", "linked_pet")
    date_hierarchy = "rabies"

    def linked_pet(self, obj):
        # follow reverse relation pet -> card
        pet = getattr(obj, "pet", None)
        return pet.name if pet else "—"
    linked_pet.short_description = "Pet"


# ────────────────────────────────
# Inlines
# (only Vet Visits, because VaccinationCard has no FK to Pet)
# ────────────────────────────────
class VetVisitInline(admin.TabularInline):
    model = VetVisit
    extra = 0
    show_change_link = True


# ────────────────────────────────
# Pet – main object
# ────────────────────────────────
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display  = ("name", "gender", "owner", "birth", "primary_breed", "card_link", "picture_thumb")
    list_filter   = ("gender", "breed")
    search_fields = ("name", "owner")
    inlines       = [VetVisitInline]

    def primary_breed(self, obj):
        return ", ".join(b.name for b in obj.breed.all()[:3]) or "—"
    primary_breed.short_description = "Breed(s)"

    def card_link(self, obj):
        if obj.card_id:
            url = f"/admin/pets_app/vaccinationcard/{obj.card_id}/change/"
            return format_html('<a href="{}">View card</a>', url)
        return "—"
    card_link.short_description = "Vaccination Card"
    card_link.allow_tags = True

    def picture_thumb(self, obj):
        if obj.picture:
            return format_html("<img src='{}' style='height:40px;'/>", obj.picture.url)
        return "—"
    picture_thumb.short_description = "Pic"


# ────────────────────────────────
# Vet Visits
# ────────────────────────────────
@admin.register(VetVisit)
class VetVisitAdmin(admin.ModelAdmin):
    list_display  = ("pet", "vet", "date", "is_today")
    list_filter   = ("vet", "date")
    search_fields = ("pet__name", "vet")
    date_hierarchy = "date"
