from django import forms

from .models import ConstructionModel


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ConstructionModelForm(forms.ModelForm):
    upload_type = forms.ChoiceField(
        label='Tipo de archivo',
        choices=[('images', 'Imágenes (hasta 3)'), ('plan', 'Plano (1 archivo PDF/PNG)')],
        initial='images',
    )
    attachments = forms.Field(
        label='Adjuntos',
        required=False,
        widget=MultiFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = ConstructionModel
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        upload_type = cleaned_data.get('upload_type')
        files = self.files.getlist('attachments') if hasattr(self, 'files') else []

        if not files:
            raise forms.ValidationError('Debes adjuntar al menos un archivo.')

        limit = 20 * 1024 * 1024
        if upload_type == 'images':
            if len(files) > 3:
                raise forms.ValidationError('Solo puedes subir hasta 3 imágenes.')
            for file in files:
                if file.content_type not in ('image/png', 'image/jpeg', 'image/jpg'):
                    raise forms.ValidationError('Solo se permiten imágenes PNG o JPG.')
                if file.size > limit:
                    raise forms.ValidationError('Cada imagen debe pesar menos de 20 MB.')
        else:
            if len(files) != 1:
                raise forms.ValidationError('Solo puedes subir un plano a la vez.')
            file = files[0]
            if file.content_type not in ('application/pdf', 'image/png'):
                raise forms.ValidationError('El plano debe ser PDF o PNG.')
            if file.size > limit:
                raise forms.ValidationError('El archivo excede los 20 MB.')

        self.cleaned_files = files
        return cleaned_data


class ModelSearchForm(forms.Form):
    query = forms.CharField(label='Buscar', required=False)
    status = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=[('', 'Todos')] + list(ConstructionModel.Status.choices),
    )
