from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import normalize_rut, validate_rut


class CustomUser(AbstractUser):
    """Custom user that stores extended profile information."""

    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    rut = models.CharField('RUT', max_length=12, unique=True, validators=[validate_rut])
    maternal_last_name = models.CharField('Apellido materno', max_length=150, blank=True)
    age = models.PositiveIntegerField(
        'Edad',
        null=True,
        blank=True,
        validators=[MinValueValidator(14), MaxValueValidator(120)],
    )
    occupation = models.CharField('Ocupación', max_length=150, blank=True)
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, blank=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    city = models.CharField('Comuna / Ciudad', max_length=120, blank=True)

    class Meta:
        ordering = ['username']

    def save(self, *args, **kwargs):
        if self.rut:
            self.rut = normalize_rut(self.rut)
        super().save(*args, **kwargs)

    @property
    def full_name(self) -> str:
        names = [self.first_name, self.last_name, self.maternal_last_name]
        clean_names = [name for name in names if name]
        return ' '.join(clean_names) if clean_names else self.username

    def profile_completed(self) -> bool:
        required_fields = [self.first_name, self.last_name, self.maternal_last_name, self.rut, self.sex]
        return all(required_fields)

    def __str__(self) -> str:
        return f'{self.username} ({self.rut})'
