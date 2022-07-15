from django import forms

class newpostform(forms.Form):
    message = forms.CharField(widget=forms.Textarea, strip=True, label="New Post")