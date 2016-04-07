from django import forms
from models import Photo

class PhotoForm(forms.ModelForm):

    class meta:
        model = Photo