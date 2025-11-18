import base64
import json
import os
from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from openai import OpenAI, OpenAIError

_client: Optional[OpenAI] = None


class OpenAIIntegrationError(Exception):
    """Wrapper exception to homogeneously tratar errores del SDK."""


def get_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise OpenAIIntegrationError('OPENAI_API_KEY no configurada en .env.')
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def generate_image(prompt: str, size: str = '1024x1024') -> str:
    try:
        response = get_client().images.generate(
            model='gpt-image-1',
            prompt=prompt,
            size=size,
        )
        data = response.data[0].b64_json
        if not data:
            raise OpenAIIntegrationError('La respuesta no contiene imagen.')
        return data
    except OpenAIError as exc:
        raise OpenAIIntegrationError(str(exc)) from exc


def _encode_local_image(path: str) -> Optional[Tuple[str, str]]:
    """
    Devuelve (base64, mime) si el archivo es imagen soportada.
    Ignora PDF/otros porque la API espera imagen.
    """
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    mime = None
    if ext in ['.png']:
        mime = 'image/png'
    elif ext in ['.jpg', '.jpeg']:
        mime = 'image/jpeg'
    else:
        return None

    with open(path, 'rb') as handler:
        return base64.b64encode(handler.read()).decode(), mime


def _extract_json_block(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1 or end < start:
        return {}
    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {}


def generate_design_brief(description: str, attachment_path: Optional[str] = None) -> Dict[str, Any]:
    user_content = [
        {
            'type': 'text',
            'text': (
                'Descripción del modelo: '
                f'{description or "Sin detalles"}. '
                'Responde ÚNICAMENTE en formato JSON con los campos: '
                'square_meters (numero aproximado), '
                'materials (lista de 3 a 5 strings), '
                'timeline (string corta) y '
                'recommendations (string detallada).'
            ),
        }
    ]

    encoded_image = _encode_local_image(attachment_path) if attachment_path else None
    if encoded_image:
        b64_data, mime = encoded_image
        user_content.append(
            {
                'type': 'image_url',
                'image_url': {
                    'url': f'data:{mime};base64,{b64_data}',
                },
            }
        )

    try:
        response = get_client().chat.completions.create(
            model='gpt-4o-mini',
            temperature=0.4,
            messages=[
                {
                    'role': 'system',
                    'content': 'Eres un arquitecto que propone fichas técnicas claras y concisas.',
                },
                {
                    'role': 'user',
                    'content': user_content,
                },
            ],
        )
        content = response.choices[0].message.content
        if isinstance(content, list):
            text = ''.join(part.get('text', '') for part in content)
        else:
            text = content or ''
        data = _extract_json_block(text)
        if not data:
            raise OpenAIIntegrationError('No se pudo interpretar la respuesta JSON.')
        return data
    except OpenAIError as exc:
        raise OpenAIIntegrationError(str(exc)) from exc
