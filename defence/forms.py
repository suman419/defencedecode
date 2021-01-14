from django import forms
from .models import User,Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField( widget=forms.Textarea(attrs={'rows': 4, 'cols': 30}))
    class Meta:
        model=Comment
        fields=('name','email','body')

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']

