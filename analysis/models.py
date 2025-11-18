from decimal import Decimal

from django.db import models


class AnalysisResult(models.Model):
    construction_model = models.OneToOneField(
        'models_core.ConstructionModel',
        related_name='analysis_result',
        on_delete=models.CASCADE,
    )
    generated_image = models.ImageField(upload_to='results/', blank=True, null=True)
    square_meters = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    materials = models.TextField()
    timeline = models.CharField(max_length=120)
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mock_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Análisis modelo #{self.construction_model_id}'
