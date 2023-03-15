from django.forms import ModelForm, TextInput
from network.models import Post
from django import forms

# Create the form class.
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "What's on your mind?",
                }
            ),
        }
        labels = {
            "content": "",
        }
