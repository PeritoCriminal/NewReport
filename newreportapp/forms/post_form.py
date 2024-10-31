# newreportapp/forms/post_form.py
from django import forms
from newreportapp.models.post_model import PostModel

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['caption', 'content', 'image', 'privacy']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control mb-3',  # Classe para estilização do Bootstrap
                'placeholder': 'Título da postagem'  # Placeholder opcional
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control mb-3',  # Classe para estilização do Bootstrap
                'rows': 4,
                'placeholder': 'Escreva algo...'  # Placeholder opcional
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mb-3',  # Classe para estilização do Bootstrap
                'onchange': 'previewImage(event)'  # Chama a função de pré-visualização da imagem
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-control mb-3'  # Classe para estilização do Bootstrap
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Aplique a classe 'form-label' aos labels
        for field in self.fields.values():
            field.label = field.label.capitalize()  # Capitaliza o label se necessário
