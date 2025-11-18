from django.shortcuts import redirect, render

from models_core.models import ConstructionModel


def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    latest_models = ConstructionModel.objects.select_related('user')[:3]
    context = {
        'latest_models': latest_models,
        'features': [
            {'title': 'Modelos inteligentes', 'text': 'Carga planos o imágenes y obtén propuestas inteligentes.'},
            {'title': 'Resultados en PDF', 'text': 'Descarga reportes profesionales en segundos.'},
            {'title': 'Panel administrativo', 'text': 'Gestiona usuarios, modelos y reportes desde un solo lugar.'},
        ],
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def tutorial(request):
    steps = [
        {'title': '1. Regístrate', 'detail': 'Crea tu cuenta y completa tu perfil para habilitar los modelos.'},
        {'title': '2. Sube tus archivos', 'detail': 'Puedes subir hasta 3 imágenes o 1 plano (PDF/PNG).'},
        {'title': '3. Procesa con IA', 'detail': 'Haz clic en “Procesar con IA” para obtener una propuesta mock.'},
        {'title': '4. Descarga en PDF', 'detail': 'Genera un informe en PDF con la ficha técnica.'},
    ]
    return render(request, 'pages/tutorial.html', {'steps': steps})
