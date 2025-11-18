from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class ConstructionModel(models.Model):
    class Status(models.TextChoices):
        PROCESSABLE = 'procesable', 'Procesable'
        PROCESSING = 'en_proceso', 'En proceso'
        PROCESSED = 'procesado', 'Procesado'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='construction_models',
    )
    name = models.CharField('Nombre del modelo', max_length=150)
    description = models.TextField('Descripción')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} ({self.user.username})'

    def get_absolute_url(self):
        return reverse('models_core:model_detail', args=[self.pk])

    def can_user_access(self, user) -> bool:
        return user.is_staff or user == self.user

    @property
    def is_processable(self) -> bool:
        return self.status in {self.Status.PROCESSABLE, self.Status.PROCESSING}


def model_attachment_upload_path(instance, filename):
    model_id = instance.model_id or 'new'
    return f'uploads/model_{model_id}/{filename}'


class ModelAttachment(models.Model):
    model = models.ForeignKey(
        ConstructionModel,
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    file = models.FileField(
        'Archivo',
        upload_to=model_attachment_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'pdf'],
            )
        ],
    )
    is_plan = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self) -> str:
        return f'Adjunto {self.file.name}'
