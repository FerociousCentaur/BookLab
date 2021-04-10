from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from math import radians, cos, sin, asin, sqrt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

@csrf_exempt
def distance(request):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    if request.is_ajax and request.method == "POST":
        data = request.POST
        lat1 = float(data.get('lat1', None))
        lon1 = float(data.get('lon1', None))#data['lon1']
        lat2 = float(data.get('lat2', None))#data['lat2']
        lon2 = float(data.get('lon2', None))
        print(lat1,lon1,lat2,lon2)#data['lon2']
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        print(lat1, lon1, lat2, lon2)
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        print(dlon, dlat)
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))
        print(c)

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371
        data = {
            'dist': str(c * r)
        }
        # calculate the result
        #print(JsonResponse(data))
        return JsonResponse(data)
    else:
        return redirect('home')

def store_page(request):
    books = Book.objects.filter(sold=False)
    return render(request, 'ManyBooks.html', {'books': books})

def render_single(request,uid):
    book = Book.objects.filter(uid=uid)
    if book:
        book = book[0]
        return render(request, 'OneBook.html', {'book': book})
    return HttpResponse('Bad Request')


def product_creation_page(request):
    if request.method == 'POST':

        formset = ImageForm(request.POST, request.FILES)
        postForm = BookForm(request.POST)
        # formset = ImageFormSet(request.POST, request.FILES,
        #                        queryset=Images.objects.none())
        if not postForm.is_valid():
            print('invalid 1')
        if not formset.is_valid():
            print('invalid 2')
        if postForm.is_valid() and formset.is_valid():
            name = postForm.cleaned_data['name']
            isbn = postForm.cleaned_data['isbn']
            location = str(postForm.cleaned_data['location'])
            #print(eval(location))
            book = Book(seller=request.user, name=name, isbn=isbn, location=location)
            book.save()

            # for form in formset.cleaned_data:
            #     # this helps to not crash if the user
            #     # do not upload all the photos
            #     if form:
            image = formset.cleaned_data['image']
            caption = formset.cleaned_data['caption']
            photo = ImageBook(book=book, image=image, caption=caption)
            photo.save()
            # use django messages framework
            # messages.success(request,
            #                  "Yeeew, check it out on the home page!")
            return redirect("store")

    else:
        postForm = BookForm()
        formset = ImageForm()
    return render(request, 'list_book.html',
                  {'postForm': postForm, 'formset': formset})
