from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from models_core.models import ConstructionModel

User = get_user_model()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'adminpanel/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(rut__icontains=query),
            )
        return queryset


class UserDetailView(StaffRequiredMixin, DetailView):
    model = User
    template_name = 'adminpanel/user_detail.html'
    context_object_name = 'user_object'


class UserModelsView(StaffRequiredMixin, View):
    template_name = 'adminpanel/user_models.html'

    def get(self, request, pk):
        user_object = get_object_or_404(User, pk=pk)
        models = ConstructionModel.objects.filter(user=user_object).prefetch_related('attachments')
        return render(request, self.template_name, {'user_object': user_object, 'models': models})


class UserDeleteView(StaffRequiredMixin, View):
    template_name = 'adminpanel/user_confirm_delete.html'

    def get(self, request, pk):
        user_object = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'user_object': user_object})

    def post(self, request, pk):
        user_object = get_object_or_404(User, pk=pk)
        user_object.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect(reverse_lazy('adminpanel:user_list'))
