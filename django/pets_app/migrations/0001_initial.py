# Generated by Django 5.2 on 2025-04-15 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VaccinationCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rabies', models.DateField(default='2025-04-15')),
                ('hepatitis', models.DateField(blank=True, null=True)),
                ('borrelia', models.DateField(blank=True, null=True)),
                ('distemper', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], default='F', max_length=6)),
                ('birth', models.DateField(blank=True, default=None, null=True)),
                ('owner', models.CharField(max_length=100)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('breed', models.ManyToManyField(blank=True, to='pets_app.breed')),
                ('card', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pets_app.vaccinationcard')),
            ],
        ),
        migrations.CreateModel(
            name='VetVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vet', models.CharField(max_length=100)),
                ('date', models.DateField(default='2025-04-15')),
                ('notes', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets_app.pet')),
            ],
        ),
    ]
