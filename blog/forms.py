from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control input-mf',
                    'placeholder': 'Name *'
                }),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control input-mf',
                    'placeholder': "Email *"
                }),

            'body': forms.Textarea(
                attrs={
                    'class': 'form-control input-mf',
                    'cols': 45,
                    'rows':8,
                    'placeholder': "Comment *"
                }),
        }

class SearchForm(forms.Form):
    query = forms.CharField(label='Qidirmoq', max_length=100)
