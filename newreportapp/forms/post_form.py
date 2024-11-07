# newreportapp/forms/post_form.py

from django import forms
from newreportapp.models.interaction.post_model import PostModel

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['caption', 'content', 'image', 'privacy']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control mb-3',  # Classe para estilização do Bootstrap
                'placeholder': 'Título da postagem'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4,
                'placeholder': 'Escreva algo...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mb-3',
                'onchange': 'previewImage(event)'  # Chama a função de pré-visualização da imagem
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-control mb-3'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # Opcional: Capitaliza labels e adiciona classe 'form-label' para estilização
        for field_name, field in self.fields.items():
            field.label = field.label.capitalize()
            field.widget.attrs['class'] += ' form-label'
        
        # Definindo as opções para o campo 'accept_comments' 
        #self.fields['accept_comments'].choices = [
        #    (True, 'Sim'),
        #    (False, 'Não')
        #]
