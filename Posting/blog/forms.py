from django import forms
from .models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'img',
            'content',
        ]


class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    img = forms.ImageField()
    content = forms.CharField(max_length=10000)


class CommentCreateForm(forms.Form):
    comment = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'cols': 55, 'rows': 2}))
