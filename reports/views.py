import os
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from models_core.models import ConstructionModel


class ResultPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        model = get_object_or_404(ConstructionModel, pk=pk)
        if not model.can_user_access(request.user):
            raise Http404

        result = getattr(model, 'analysis_result', None)
        if not result:
            messages.error(request, 'Este modelo aún no tiene resultado.')
            return redirect(model.get_absolute_url())

        image_path = None
        if result.generated_image and result.generated_image.name:
            try:
                candidate = result.generated_image.path
                if os.path.exists(candidate):
                    image_path = candidate
            except ValueError:
                image_path = None

        template = get_template('reports/result_pdf.html')
        html = template.render({'model': model, 'result': result, 'image_path': image_path})
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF.')
            return redirect(model.get_absolute_url())

        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=construplan_modelo_{model.pk}.pdf'
        return response
