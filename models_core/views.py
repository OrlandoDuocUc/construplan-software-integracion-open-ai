from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ConstructionModelForm, ModelSearchForm
from .models import ConstructionModel, ModelAttachment


class ModelListView(LoginRequiredMixin, ListView):
    template_name = 'models_core/model_list.html'
    context_object_name = 'models'
    paginate_by = 10

    def get_queryset(self):
        queryset = ConstructionModel.objects.select_related('user').prefetch_related('attachments')
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        query = self.request.GET.get('query') or self.request.GET.get('q')
        status = self.request.GET.get('status')
        if query:
            queryset = queryset.filter(name__icontains=query)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ModelSearchForm(self.request.GET or None)
        return context


class ModelCreateView(LoginRequiredMixin, View):
    template_name = 'models_core/model_form.html'

    def get(self, request):
        form = ConstructionModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ConstructionModelForm(request.POST, request.FILES)
        if form.is_valid():
            construction_model = form.save(commit=False)
            construction_model.user = request.user
            construction_model.save()

            upload_type = form.cleaned_data.get('upload_type')
            for file in getattr(form, 'cleaned_files', []):
                ModelAttachment.objects.create(
                    model=construction_model,
                    file=file,
                    is_plan=upload_type == 'plan',
                )

            messages.success(request, 'Modelo registrado correctamente.')
            return redirect(construction_model.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ModelDetailView(LoginRequiredMixin, DetailView):
    model = ConstructionModel
    template_name = 'models_core/model_detail.html'
    context_object_name = 'construction_model'

    def get_queryset(self):
        queryset = (
            ConstructionModel.objects.select_related('user')
            .prefetch_related('attachments')
            .all()
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analysis_result'] = getattr(self.object, 'analysis_result', None)
        return context


class ModelDeleteView(LoginRequiredMixin, View):
    template_name = 'models_core/model_confirm_delete.html'

    def get_object(self, pk):
        model = get_object_or_404(ConstructionModel, pk=pk)
        if not model.can_user_access(self.request.user):
            raise Http404
        return model

    def get(self, request, pk):
        model = self.get_object(pk)
        return render(request, self.template_name, {'construction_model': model})

    def post(self, request, pk):
        model = self.get_object(pk)
        model.delete()
        messages.success(request, 'Modelo eliminado correctamente.')
        return redirect(reverse_lazy('models_core:model_list'))
