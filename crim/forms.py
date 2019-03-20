from django import forms


class ForumPostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    body = forms.CharField(label="Body")
