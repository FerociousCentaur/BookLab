from django import forms
from .models import Book, ImageBook

class BookForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    isbn = forms.CharField(max_length=30, label="ISBN number")
    location = forms.CharField(max_length=60,widget = forms.HiddenInput())

    class Meta:
        model = Book
        fields = ('name', 'isbn', 'location')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    caption = forms.CharField(max_length=255)

    class Meta:
        model = ImageBook
        fields = ('image', 'caption',)