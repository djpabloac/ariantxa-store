from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values() :
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']