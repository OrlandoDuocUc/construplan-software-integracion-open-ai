from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View

from models_core.models import ConstructionModel

from .models import AnalysisResult
from .services import generate_analysis
from .services.ai_client import OpenAIIntegrationError, generate_image


class ProcessModelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        model = get_object_or_404(ConstructionModel, pk=pk)
        if not model.can_user_access(request.user):
            raise Http404

        result = generate_analysis(model)
        messages.success(request, 'Análisis generado correctamente.')
        return redirect('analysis:analysis_detail', pk=result.pk)


class AnalysisDetailView(LoginRequiredMixin, DetailView):
    model = AnalysisResult
    template_name = 'analysis/analysis_detail.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        queryset = AnalysisResult.objects.select_related('construction_model', 'construction_model__user')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(construction_model__user=self.request.user)


def test_ai(request):
    if not settings.OPENAI_API_KEY:
        return HttpResponse('Configura OPENAI_API_KEY en tu archivo .env', status=400)

    try:
        generate_image('Casa moderna blanca con techo plano')
        return HttpResponse('IA funcionando correctamente ✔️')
    except OpenAIIntegrationError as exc:
        return HttpResponse(f'Error: {exc}', status=500)
    except Exception as exc:  # noqa: BLE001
        return HttpResponse(f'Error inesperado: {exc}', status=500)
