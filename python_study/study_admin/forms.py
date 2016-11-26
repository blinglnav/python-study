from django import forms

class ArticleForm(forms.Form):
    chapter = forms.CharField(max_length=8)  # e.g. 1.10
    title = forms.CharField(max_length=128)
    content = forms.CharField()
