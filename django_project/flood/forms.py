from django import forms

from .models import Photo

class PostForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('score')

    def clean(self):

        if 'up' in self.data:
            #add 1 to score

        else if 'down' in self.data:
            #minus 1 from score

