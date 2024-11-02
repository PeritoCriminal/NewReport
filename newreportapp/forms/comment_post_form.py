# myreportapp.forms.comment_post_form.py

from django import forms
from newreportapp.models.comment_post_model import ComentPostModel

class CommentForm(forms.ModelForm):
    class Meta:
        model = ComentPostModel
        fields = ['content']  # Apenas o campo de conteúdo é necessário
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escreva seu comentário...', 'rows': 3}),
        }
