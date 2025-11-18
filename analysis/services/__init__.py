import base64
import logging
from decimal import Decimal, InvalidOperation
from typing import Any

from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile

from .ai_client import OpenAIIntegrationError, generate_design_brief, generate_image
from .mock import generate_mock_analysis

logger = logging.getLogger(__name__)


def _ensure_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal('0')


def _get_analysis_result(construction_model):
    AnalysisResult = apps.get_model('analysis', 'AnalysisResult')
    result, _ = AnalysisResult.objects.get_or_create(construction_model=construction_model)
    return result


def _get_attachment_path(construction_model) -> str | None:
    attachment = construction_model.attachments.first()
    if attachment and attachment.file:
        try:
            return attachment.file.path
        except ValueError:
            return None
    return None


def generate_analysis(construction_model):
    if not settings.OPENAI_API_KEY:
        return generate_mock_analysis(construction_model)

    ConstructionModel = apps.get_model('models_core', 'ConstructionModel')
    result = _get_analysis_result(construction_model)

    prompt = (
        f"Render arquitectonico realista para el modelo '{construction_model.name}'. "
        f"Descripcion del cliente: {construction_model.description}"
    )
    attachment_path = _get_attachment_path(construction_model)

    image_ok = False
    brief = {}

    # Generamos imagen primero; si falla, seguimos intentando la ficha y solo caemos al mock si todo falla.
    try:
        image_b64 = generate_image(prompt)
        if image_b64:
            image_content = ContentFile(
                base64.b64decode(image_b64),
                name=f'model_{construction_model.pk}_ia.png',
            )
            result.generated_image.save(image_content.name, image_content, save=False)
            image_ok = True
    except OpenAIIntegrationError as exc:
        logger.warning('Fallo al generar imagen con OpenAI: %s', exc)
    except Exception as exc:  # noqa: BLE001
        logger.exception('Error inesperado generando imagen IA', exc_info=exc)

    try:
        brief = generate_design_brief(construction_model.description, attachment_path)
    except OpenAIIntegrationError as exc:
        logger.warning('Fallo al generar brief con OpenAI: %s', exc)
        brief = {}
    except Exception as exc:  # noqa: BLE001
        logger.exception('Error inesperado generando brief IA', exc_info=exc)
        brief = {}

    if not image_ok and not brief:
        return generate_mock_analysis(construction_model)

    result.square_meters = _ensure_decimal((brief or {}).get('square_meters', 0))
    materials = (brief or {}).get('materials') or []
    if isinstance(materials, list):
        result.materials = ', '.join(materials) if materials else 'Materiales a definir.'
    else:
        result.materials = str(materials) or 'Materiales a definir.'
    result.timeline = (brief or {}).get('timeline') or 'Cronograma estimado disponible en informe.'
    result.recommendations = (brief or {}).get('recommendations') or 'Sin recomendaciones adicionales.'
    result.mock_payload = {
        'provider': 'openai' if image_ok else 'openai-partial',
        'brief': brief,
    }
    result.save()

    construction_model.status = ConstructionModel.Status.PROCESSED
    construction_model.save(update_fields=['status'])
    return result


__all__ = ['generate_analysis', 'generate_mock_analysis']
