import math
import random
from io import BytesIO

from django.apps import apps
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont


def _generate_placeholder_image(model_name: str) -> ContentFile:
    width, height = 960, 540
    palette = ['#1D3557', '#457B9D', '#E63946', '#2A9D8F', '#5D576B']
    background = random.choice(palette)
    image = Image.new('RGB', (width, height), background)
    draw = ImageDraw.Draw(image)
    accent = '#F1FAEE'
    draw.rectangle([(40, 40), (width - 40, height - 40)], outline=accent, width=4)
    font = ImageFont.load_default()
    header = 'CONSTRUPLAN MOCK'
    draw.text((60, 60), header, fill=accent, font=font)
    body_text = f'Modelo: {model_name[:24]}'
    draw.text((60, height / 2), body_text, fill=accent, font=font)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name='resultado_mock.png')


def _mock_materials(description_length: int) -> str:
    catalog = [
        'Hormigon reforzado',
        'Acero estructural',
        'Aislacion termica',
        'Revestimiento madera',
        'Paneles solares',
    ]
    selected = random.sample(catalog, k=min(3, len(catalog)))
    return ', '.join(selected) + f'. Detalle basado en {description_length} caracteres.'


def generate_mock_analysis(construction_model):
    AnalysisResult = apps.get_model('analysis', 'AnalysisResult')
    ConstructionModel = apps.get_model('models_core', 'ConstructionModel')

    result, _ = AnalysisResult.objects.get_or_create(construction_model=construction_model)
    description_length = len(construction_model.description)

    base_area = max(50, min(450, description_length * 1.5))
    random_delta = random.uniform(0.85, 1.15)
    result.square_meters = math.floor(base_area * random_delta)
    result.materials = _mock_materials(description_length)
    result.timeline = f"{random.randint(2, 8)} meses estimados"
    result.recommendations = (
        'Optimizar la orientacion para aprovechar luz natural. '
        'Considerar ventilacion cruzada y materiales sustentables.'
    )

    image_file = _generate_placeholder_image(construction_model.name)
    result.generated_image.save(image_file.name, image_file, save=False)
    result.mock_payload = {
        'processed_at': timezone.now().isoformat(),
        'duration_seconds': random.randint(1, 3),
    }
    result.save()

    construction_model.status = ConstructionModel.Status.PROCESSED
    construction_model.save(update_fields=['status'])
    return result
