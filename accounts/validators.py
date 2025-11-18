import re

from django.core.exceptions import ValidationError


def _rut_digit(value: str) -> str:
    value = value.upper()
    return 'K' if value == 'K' else str(value)


def validate_rut(value: str) -> None:
    """Validate Chilean RUT with modulus 11 check."""
    rut = re.sub(r'[^0-9kK]', '', value or '').upper()
    if len(rut) < 2:
        raise ValidationError('El RUT debe tener al menos 2 caracteres.')

    body, dv = rut[:-1], rut[-1]
    if not body.isdigit():
        raise ValidationError('El RUT solo debe contener números antes del guion.')

    reversed_digits = map(int, reversed(body))
    factors = [2, 3, 4, 5, 6, 7]
    total = 0
    factor_index = 0
    for digit in reversed_digits:
        total += digit * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)
    remainder = 11 - (total % 11)
    expected = '0' if remainder == 11 else 'K' if remainder == 10 else str(remainder)

    if _rut_digit(dv) != expected:
        raise ValidationError('El RUT ingresado no es válido.')


def normalize_rut(value: str) -> str:
    """Normalize RUT by removing separators and using the standard format ########-X."""
    rut = re.sub(r'[^0-9kK]', '', value or '').upper()
    if len(rut) < 2:
        return value
    body, dv = rut[:-1], rut[-1]
    return f'{int(body)}-{dv}'
