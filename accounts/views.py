from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfileForm


class SignUpView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro completado. Ya puedes crear modelos.')
            return redirect('models_core:model_list')
        messages.error(request, 'Verifica el formulario e inténtalo nuevamente.')
        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'


class UserLogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Sesión finalizada correctamente.')
        return redirect('accounts:login')

    def get(self, request):
        return self.post(request)


class ForgotPasswordView(TemplateView):
    template_name = 'accounts/forgot_password.html'


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('accounts:profile')
        messages.error(request, 'No se pudo actualizar el perfil.')
        return render(request, self.template_name, {'form': form})
