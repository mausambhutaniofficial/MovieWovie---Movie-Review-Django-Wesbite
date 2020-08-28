from django import forms
from . models import *

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'director', 'cast', 'description', 'release_date', 'image', 'trailer_link')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'rating')
        